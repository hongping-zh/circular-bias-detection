import argparse
import json
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, classification_report


def load_dataset(prefix: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    edges = pd.read_csv(f"{prefix}_edges_labeled.csv")
    nodes = pd.read_csv(f"{prefix}_nodes.csv")
    return edges, nodes


def simple_bias_predictor(edges: pd.DataFrame) -> pd.Series:
    """
    A simple heuristic detector for biased edges:
    - Predict biased if citing and cited are in the same biased group (group != -1)
      AND citing_publication_year == cited_publication_year.
    This mirrors the injection mechanism and serves as an upper-bound baseline.
    """
    same_group = edges['citing_paper_id'].map(lambda x: x)  # placeholder for typing
    # Use columns created by generator: years already merged into edges
    pred = (
        (edges['edge_source'].eq('bias')) |
        (
            (edges['citing_publication_year'] == edges['cited_publication_year'])
        )
    )
    # The above includes a trivial oracle using edge_source if present; for a realistic
    # baseline without oracle information, use the version below instead:
    # pred = (
    #     (edges['citing_publication_year'] == edges['cited_publication_year']) &
    #     (edges.get('same_group', pd.Series(False, index=edges.index)))
    # )
    return pred.astype(int)


def evaluate(prefix: str, use_oracle: bool = False) -> dict:
    edges, nodes = load_dataset(prefix)

    # Join group IDs for a baseline without oracle. Optional.
    nodes_grp = nodes[['paper_id', 'biased_group_id']].rename(columns={'paper_id': 'citing_paper_id'})
    edges = edges.merge(nodes_grp, on='citing_paper_id', how='left')
    edges = edges.rename(columns={'biased_group_id': 'citing_group'})
    nodes_grp = nodes[['paper_id', 'biased_group_id']].rename(columns={'paper_id': 'cited_paper_id'})
    edges = edges.merge(nodes_grp, on='cited_paper_id', how='left')
    edges = edges.rename(columns={'biased_group_id': 'cited_group'})
    edges['same_group'] = (edges['citing_group'] != -1) & (edges['citing_group'] == edges['cited_group'])

    if use_oracle:
        y_pred = (edges['edge_source'] == 'bias').astype(int)
    else:
        # Heuristic: same year AND same biased group
        y_pred = ((edges['citing_publication_year'] == edges['cited_publication_year']) & (edges['same_group'])).astype(int)

    y_true = edges['edge_is_biased'].astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', zero_division=0)
    report = classification_report(y_true, y_pred, digits=4, zero_division=0)

    return {
        'prefix': prefix,
        'num_edges': int(len(edges)),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1),
        'classification_report': report,
    }


def main():
    parser = argparse.ArgumentParser(description='Evaluate bias edge detection on synthetic citation datasets.')
    parser.add_argument('--prefix', type=str, default='synthetic_citations_small', help='Output prefix used by generator (without suffix).')
    parser.add_argument('--oracle', action='store_true', help='Use oracle predictor based on edge_source (upper bound).')
    parser.add_argument('--json', type=str, default='', help='Optional path to write JSON summary.')
    args = parser.parse_args()

    res = evaluate(args.prefix, use_oracle=args.oracle)
    print("=== Evaluation Summary ===")
    print(json.dumps({k: v for k, v in res.items() if k != 'classification_report'}, indent=2))
    print("\n=== Classification Report ===\n")
    print(res['classification_report'])

    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

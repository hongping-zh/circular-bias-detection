import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime
import random
import json

def generate_citation_dataset(
    num_papers: int = 1000,
    start_year: int = 2010,
    end_year: int = 2023,
    base_citation_rate: float = 1.5,
    num_biased_groups: int = 5,
    biased_group_size: int = 4,
    bias_intensity: int = 2,
    file_name: str = "synthetic_citations.csv",
    seed: int | None = 42,
    save_labels: bool = True,
    out_prefix: str | None = None,
    base_same_year_rate: float = 0.0,
    bias_cross_group_rate: float = 0.0
):
    """
    生成一个模拟的引文网络数据集，其中包含注入的循环偏见。

    参数:
    - num_papers: 论文总数。
    - start_year, end_year: 论文发表年份范围。
    - base_citation_rate: 平均每篇论文的基础引文数。
    - num_biased_groups: 要创建的循环偏见小团体数量。
    - biased_group_size: 每个小团体的大小。
    - bias_intensity: 小团体内部的循环引用强度（每个成员引用团体中其他成员的数量）。
    - file_name: 输出的CSV文件名（向后兼容）。
    - seed: 随机种子，保证可复现。
    - save_labels: 是否保存带有标签的节点与边文件。
    - out_prefix: 输出文件前缀；若为空，则从 file_name 去掉扩展名得到。
    - base_same_year_rate: 基础网络阶段允许同年引用的概率（0-1，默认0）。
    - bias_cross_group_rate: 偏见注入阶段为每个成员额外创建跨团体同年引用的概率（0-1，默认0）。
    """
    print(f"Generating dataset with {num_papers} papers...")

    # 0. 设定随机种子，保证可复现
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # 1. 创建论文元数据
    papers = pd.DataFrame({
        'paper_id': range(num_papers),
        'publication_year': np.random.randint(start_year, end_year + 1, size=num_papers)
    })
    papers['biased_group_id'] = -1

    # 2. 创建一个有向图作为基础“健康”引文网络（严格使用 citing_year > cited_year）
    G = nx.DiGraph()
    G.add_nodes_from(papers['paper_id'])
    
    citations = []  # list of dicts with labels
    total_base_citations = int(num_papers * base_citation_rate)
    
    # 确保引用都指向更早的论文（默认不允许同年；可按比例允许同年）
    paper_indices = list(range(num_papers))
    for _ in range(total_base_citations):
        citing_idx, cited_idx = random.sample(paper_indices, 2)
        citing_year = papers.loc[citing_idx, 'publication_year']
        cited_year = papers.loc[cited_idx, 'publication_year']
        if citing_year > cited_year:
            citations.append({
                'citing_paper_id': papers.loc[citing_idx, 'paper_id'],
                'cited_paper_id': papers.loc[cited_idx, 'paper_id'],
                'edge_source': 'base',
                'edge_is_biased': 0,
            })
        elif citing_year == cited_year and base_same_year_rate > 0.0:
            if random.random() < base_same_year_rate:
                citations.append({
                    'citing_paper_id': papers.loc[citing_idx, 'paper_id'],
                    'cited_paper_id': papers.loc[cited_idx, 'paper_id'],
                    'edge_source': 'base',
                    'edge_is_biased': 0,
                })

    print(f"Generated {len(citations)} base 'healthy' citations.")

    # 3. 注入循环偏见
    papers_in_biased_groups = set()
    for i in range(num_biased_groups):
        print(f"Injecting bias for group {i+1}/{num_biased_groups}...")
        
        # 随机选择不重复的论文组成小团体
        potential_members = [p for p in paper_indices if p not in papers_in_biased_groups]
        if len(potential_members) < biased_group_size:
            print("Warning: Not enough papers left to form a new biased group.")
            break
        
        group_members = random.sample(potential_members, biased_group_size)
        papers_in_biased_groups.update(group_members)
        for member_id in group_members:
            papers.loc[member_id, 'biased_group_id'] = i

        # 在团体内部创建密集的、可能是循环的引用
        # 为了模拟偏见，我们让它们在同一年发表
        bias_year = np.random.randint(start_year + 2, end_year + 1) # 偏见通常出现在后期
        for member_id in group_members:
            papers.loc[member_id, 'publication_year'] = bias_year

            # 每个成员引用团体内的其他几个成员
            others = [m for m in group_members if m != member_id]
            cited_in_group = random.sample(others, min(bias_intensity, len(others)))
            
            for cited_id in cited_in_group:
                citations.append({
                    'citing_paper_id': papers.loc[member_id, 'paper_id'],
                    'cited_paper_id': papers.loc[cited_id, 'paper_id'],
                    'edge_source': 'bias',
                    'edge_is_biased': 1,
                })

            # 以一定概率添加跨团体同年引用，增加任务难度
            if bias_cross_group_rate > 0.0 and random.random() < bias_cross_group_rate:
                non_group_candidates = [p for p in paper_indices if p not in group_members]
                if non_group_candidates:
                    cross_id = random.choice(non_group_candidates)
                    # 使跨团体目标与团体同年，以制造同年跨团体边
                    papers.loc[cross_id, 'publication_year'] = bias_year
                    citations.append({
                        'citing_paper_id': papers.loc[member_id, 'paper_id'],
                        'cited_paper_id': papers.loc[cross_id, 'paper_id'],
                        'edge_source': 'bias',
                        'edge_is_biased': 1,
                    })

    print(f"Total citations after injecting bias: {len(citations)}")

    # 4. 创建最终的 DataFrame 并保存
    edges_df = pd.DataFrame(citations, columns=['citing_paper_id', 'cited_paper_id', 'edge_source', 'edge_is_biased'])
    
    # 合并年份信息（以最终年份为准）
    edges_df = edges_df.merge(
        papers.rename(columns={'paper_id': 'citing_paper_id', 'publication_year': 'citing_publication_year'}),
        on='citing_paper_id'
    ).merge(
        papers.rename(columns={'paper_id': 'cited_paper_id', 'publication_year': 'cited_publication_year'}),
        on='cited_paper_id'
    )

    # 生成节点表
    nodes_df = papers[['paper_id', 'publication_year', 'biased_group_id']].copy()
    nodes_df['is_biased_member'] = (nodes_df['biased_group_id'] != -1).astype(int)

    # 打乱边顺序（可选）
    edges_df = edges_df.sample(frac=1).reset_index(drop=True)

    # 计算输出前缀
    prefix = out_prefix
    if not prefix:
        prefix = file_name[:-4] if file_name.lower().endswith('.csv') else file_name

    # 保存带标签的数据集
    if save_labels:
        labeled_edges_path = f"{prefix}_edges_labeled.csv"
        nodes_path = f"{prefix}_nodes.csv"
        edges_df.to_csv(labeled_edges_path, index=False)
        nodes_df.to_csv(nodes_path, index=False)
        # 保存参数
        params = {
            'num_papers': num_papers,
            'start_year': start_year,
            'end_year': end_year,
            'base_citation_rate': base_citation_rate,
            'num_biased_groups': num_biased_groups,
            'biased_group_size': biased_group_size,
            'bias_intensity': bias_intensity,
            'seed': seed,
            'timestamp': datetime.now().isoformat(),
            'out_prefix': prefix,
            'base_same_year_rate': base_same_year_rate,
            'bias_cross_group_rate': bias_cross_group_rate,
        }
        with open(f"{prefix}_params.json", 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=2)

    # 兼容保留原始简版边表
    final_df = edges_df[['citing_paper_id', 'cited_paper_id', 'citing_publication_year', 'cited_publication_year']].copy()
    final_df.to_csv(file_name, index=False)
    print(f"Dataset successfully saved to '{file_name}'")


if __name__ == '__main__':
    # --- 场景1: 小型数据集 (用于快速测试和调试) ---
    generate_citation_dataset(
        num_papers=200,
        start_year=2015,
        end_year=2023,
        base_citation_rate=1.2,
        num_biased_groups=3,
        biased_group_size=4,
        bias_intensity=2,  # 每个成员引用团体中2个其他成员，容易形成环
        file_name="synthetic_citations_small.csv"
    )

    print("\n" + "="*50 + "\n")

    # --- 场景2: 中型数据集 (用于更真实的性能和效果测试) ---
    generate_citation_dataset(
        num_papers=5000,
        start_year=2000,
        end_year=2023,
        base_citation_rate=2.0,
        num_biased_groups=20,
        biased_group_size=5,
        bias_intensity=3,
        file_name="synthetic_citations_medium.csv"
    )
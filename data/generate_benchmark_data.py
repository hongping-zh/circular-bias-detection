#!/usr/bin/env python3
"""
Data generation script for Algorithm Benchmark Suite v2.0

This script generates the synthetic evaluation data used in the benchmark suite.
All data files can be fully reproduced using this script with fixed random seeds.

Usage:
    python generate_benchmark_data.py --output-dir ./generated_data
    
For more options:
    python generate_benchmark_data.py --help
"""

import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path


def generate_base_scenario(
    n_time_periods=20,
    n_algorithms=4,
    bias_intensity=0.0,
    noise_level=0.1,
    random_seed=42
):
    """
    Generate a single evaluation scenario.
    
    Parameters
    ----------
    n_time_periods : int
        Number of evaluation time periods
    n_algorithms : int
        Number of algorithms to evaluate
    bias_intensity : float
        Circular bias intensity (0.0 = no bias, 1.0 = maximum bias)
    noise_level : float
        Measurement noise level (std deviation)
    random_seed : int
        Random seed for reproducibility
        
    Returns
    -------
    pd.DataFrame
        Generated evaluation data
    """
    np.random.seed(random_seed)
    
    algorithms = ['ResNet', 'VGG', 'DenseNet', 'EfficientNet'][:n_algorithms]
    
    records = []
    
    for t in range(1, n_time_periods + 1):
        for algo_idx, algo in enumerate(algorithms):
            # Base performance with temporal correlation
            base_perf = 0.65 + 0.02 * t + 0.05 * algo_idx
            perf = base_perf + np.random.normal(0, noise_level)
            perf = np.clip(perf, 0, 1)
            
            # Constraints
            base_compute = 300 + 15 * t
            base_memory = 7.5 + 0.3 * t
            base_dataset = 50000 + 1000 * t
            
            # Inject bias if requested
            if bias_intensity > 0:
                # Make constraints correlate with performance
                perf_factor = (perf - 0.5) * 2  # Normalize to [-1, 1]
                base_compute *= (1 + bias_intensity * perf_factor * 0.1)
                base_memory *= (1 + bias_intensity * perf_factor * 0.1)
                base_dataset *= (1 + bias_intensity * perf_factor * 0.05)
            
            # Add noise
            compute = base_compute + np.random.normal(0, 10)
            memory = base_memory + np.random.normal(0, 0.2)
            dataset = int(base_dataset + np.random.normal(0, 500))
            
            records.append({
                'time_period': t,
                'algorithm': algo,
                'performance': round(perf, 4),
                'constraint_compute': round(compute, 1),
                'constraint_memory': round(memory, 1),
                'constraint_dataset_size': dataset,
                'evaluation_protocol': f'ImageNet-v1.{t-1}'
            })
    
    return pd.DataFrame(records)


def generate_main_benchmark(output_path):
    """Generate the main benchmark file (algorithm_benchmark_suite.csv)."""
    print("Generating main benchmark file...")
    
    df = generate_base_scenario(
        n_time_periods=5,
        n_algorithms=4,
        bias_intensity=0.0,
        noise_level=0.05,
        random_seed=42
    )
    
    df.to_csv(output_path, index=False)
    print(f"✓ Saved: {output_path} ({len(df)} records)")
    return df


def generate_scenario_files(output_dir):
    """Generate the 9 scenario files with varying parameters."""
    
    scenarios = [
        # (filename, n_periods, n_algos, bias, noise, seed)
        ('scenario_no_bias_low_noise.csv', 15, 4, 0.0, 0.05, 100),
        ('scenario_no_bias_high_noise.csv', 15, 4, 0.0, 0.2, 101),
        ('scenario_mild_bias.csv', 15, 4, 0.3, 0.1, 102),
        ('scenario_moderate_bias.csv', 15, 4, 0.6, 0.1, 103),
        ('scenario_high_bias.csv', 15, 4, 0.9, 0.1, 104),
        ('scenario_few_periods.csv', 8, 4, 0.5, 0.1, 105),
        ('scenario_many_algorithms.csv', 12, 6, 0.4, 0.1, 106),
        ('scenario_mixed_conditions.csv', 20, 5, 0.5, 0.15, 107),
        ('scenario_edge_case.csv', 10, 3, 0.8, 0.05, 108),
    ]
    
    print(f"\nGenerating {len(scenarios)} scenario files...")
    
    for filename, n_periods, n_algos, bias, noise, seed in scenarios:
        df = generate_base_scenario(
            n_time_periods=n_periods,
            n_algorithms=n_algos,
            bias_intensity=bias,
            noise_level=noise,
            random_seed=seed
        )
        
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"✓ Saved: {filename} ({len(df)} records, bias={bias}, noise={noise})")


def validate_generated_data(output_dir):
    """Validate generated data against schema (if jsonschema installed)."""
    try:
        import jsonschema
        import json
        
        print("\nValidating generated data...")
        
        # Load schema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.json')
        if not os.path.exists(schema_path):
            print("⚠️  Schema file not found, skipping validation")
            return
        
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Validate each CSV file
        csv_files = list(Path(output_dir).glob('*.csv'))
        
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            
            # Validate first record
            record = df.iloc[0].to_dict()
            try:
                jsonschema.validate(instance=record, schema=schema)
                print(f"✓ {csv_file.name} - Valid")
            except jsonschema.ValidationError as e:
                print(f"✗ {csv_file.name} - Invalid: {e.message}")
        
    except ImportError:
        print("\n⚠️  jsonschema not installed, skipping validation")
        print("   Install with: pip install jsonschema")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Algorithm Benchmark Suite v2.0 data'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./generated_data',
        help='Output directory for generated CSV files (default: ./generated_data)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate generated data against schema.json'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Algorithm Benchmark Suite v2.0 - Data Generation")
    print("=" * 70)
    
    # Generate main benchmark
    main_file = os.path.join(args.output_dir, 'algorithm_benchmark_suite.csv')
    generate_main_benchmark(main_file)
    
    # Generate scenario files
    generate_scenario_files(args.output_dir)
    
    # Validate if requested
    if args.validate:
        validate_generated_data(args.output_dir)
    
    print("\n" + "=" * 70)
    print("✓ Data generation complete!")
    print(f"  Output directory: {args.output_dir}")
    print(f"  Total files: 10 CSV files")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review generated files")
    print("  2. Run validation: python generate_benchmark_data.py --validate")
    print("  3. Use data in your experiments")


if __name__ == '__main__':
    main()

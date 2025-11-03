#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Circular Bias Detection CLI - Main Entry Point

A command-line tool for detecting circular reasoning bias in algorithm evaluation.
"""

import sys
import argparse
import logging
import json
from pathlib import Path
from typing import Optional

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed")
    print("Please run: pip install pandas numpy scipy")
    sys.exit(1)

from .adapters.algorithm_adapter import AlgorithmAdapter
from .utils.zenodo_loader import ZenodoLoader


class CircularBiasCLI:
    """Main CLI application class."""
    
    def __init__(self):
        self.algorithm_adapter = AlgorithmAdapter()
        self.zenodo_loader = ZenodoLoader()
        self.setup_logging()
    
    def setup_logging(self, level: str = 'INFO'):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser."""
        parser = argparse.ArgumentParser(
            prog='circular-bias',
            description='Detect circular reasoning bias in algorithm evaluation',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Detect bias in Zenodo dataset
  circular-bias detect zenodo://17201032
  
  # Use specific scenario
  circular-bias detect zenodo://17201032/scenario_high_bias.csv
  
  # Analyze local file
  circular-bias detect data/my_evaluation.csv
  
  # Run specific algorithm
  circular-bias detect data.csv --algorithm psi --threshold 0.2
  
  # Export results as JSON
  circular-bias detect data.csv --output results.json --format json
  
  # List Zenodo dataset info
  circular-bias info zenodo://17201032

For more information: https://github.com/hongping-zh/circular-bias-detection
            """
        )
        
        parser.add_argument('--version', action='version', version='1.0.0')
        parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Detect command
        detect_parser = subparsers.add_parser('detect', help='Detect bias in data')
        detect_parser.add_argument('data', type=str, help='Data source (zenodo://, file://, or path)')
        detect_parser.add_argument(
            '--algorithm', '-a',
            choices=['psi', 'ccs', 'rho_pc', 'decision'],
            default='decision',
            help='Algorithm to run (default: decision framework)'
        )
        detect_parser.add_argument(
            '--psi-threshold', type=float, default=0.15,
            help='PSI detection threshold (default: 0.15)'
        )
        detect_parser.add_argument(
            '--ccs-threshold', type=float, default=0.85,
            help='CCS detection threshold (default: 0.85)'
        )
        detect_parser.add_argument(
            '--rho-threshold', type=float, default=0.5,
            help='ρ_PC detection threshold (default: 0.5)'
        )
        detect_parser.add_argument(
            '--output', '-o', type=str,
            help='Output file path (default: stdout)'
        )
        detect_parser.add_argument(
            '--format', '-f',
            choices=['text', 'json', 'csv'],
            default='text',
            help='Output format (default: text)'
        )
        
        # Info command
        info_parser = subparsers.add_parser('info', help='Show dataset information')
        info_parser.add_argument('source', type=str, help='Data source (zenodo:// or path)')
        
        # Cache command
        cache_parser = subparsers.add_parser('cache', help='Manage cache')
        cache_subparsers = cache_parser.add_subparsers(dest='cache_action')
        cache_subparsers.add_parser('list', help='List cached datasets')
        cache_clear_parser = cache_subparsers.add_parser('clear', help='Clear cache')
        cache_clear_parser.add_argument('--record-id', type=str, help='Clear specific record')
        
        # List algorithms command
        subparsers.add_parser('list-algorithms', help='List available algorithms')

        # Quality gate command for CI/CD
        gate_parser = subparsers.add_parser('gate', help='Run CI/CD quality gate for circular bias')
        gate_parser.add_argument('--data-path', type=str, required=True, help='Path to local CSV data file')
        gate_parser.add_argument('--psi-threshold', type=float, default=0.15, help='PSI detection threshold (default: 0.15)')
        gate_parser.add_argument('--ccs-threshold', type=float, default=0.85, help='CCS detection threshold (default: 0.85)')
        gate_parser.add_argument('--rho-threshold', type=float, default=0.5, help='ρ_PC detection threshold (default: 0.5)')
        gate_parser.add_argument('--warn-threshold', type=float, default=0.6, help='Warn gate on confidence ≥ this value (default: 0.6)')
        gate_parser.add_argument('--critical-threshold', type=float, default=0.8, help='Fail gate on confidence ≥ this value when bias detected (default: 0.8)')
        gate_parser.add_argument('--output', '-o', type=str, help='Optional output file path')
        gate_parser.add_argument('--format', '-f', choices=['text', 'json', 'csv'], default='json', help='Output format (default: json)')
        
        return parser
    
    def cmd_detect(self, args) -> int:
        """Execute detect command."""
        try:
            # Load data
            self.logger.info(f"Loading data from: {args.data}")
            data = self.zenodo_loader.load(args.data)
            
            self.logger.info(f"Loaded {len(data)} records")
            self.logger.info(f"Columns: {list(data.columns)}")
            
            # Prepare parameters
            params = {
                'threshold': args.psi_threshold if args.algorithm == 'psi' 
                           else args.ccs_threshold if args.algorithm == 'ccs'
                           else args.rho_threshold,
                'psi_threshold': args.psi_threshold,
                'ccs_threshold': args.ccs_threshold,
                'rho_pc_threshold': args.rho_threshold
            }
            
            # Map algorithm names
            algo_map = {
                'psi': 'psi',
                'ccs': 'ccs',
                'rho_pc': 'rho_pc',
                'decision': 'decision_framework'
            }
            algorithm = algo_map[args.algorithm]
            
            # Run detection
            self.logger.info(f"Running {args.algorithm.upper()} algorithm...")
            result = self.algorithm_adapter.run(algorithm, data, params)
            
            # Format output
            if args.format == 'json':
                output = json.dumps(result, indent=2)
            elif args.format == 'csv':
                output = self._format_csv(result)
            else:  # text
                output = self._format_text(result)
            
            # Write output
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"✓ Results written to: {args.output}")
            else:
                print(output)
            
            # Return exit code based on detection
            return 1 if result.get('detected', False) else 0
            
        except Exception as e:
            self.logger.error(f"Detection failed: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 2
    
    def cmd_info(self, args) -> int:
        """Execute info command."""
        try:
            if args.source.startswith('zenodo://'):
                # Get Zenodo metadata
                record_id = args.source.replace('zenodo://', '').split('/')[0]
                info = self.zenodo_loader.get_zenodo_info(record_id)
                
                print("=" * 60)
                print(f"Zenodo Record: {record_id}")
                print("=" * 60)
                print(f"Title: {info['title']}")
                print(f"DOI: {info['doi']}")
                print(f"Version: {info['version']}")
                print(f"Publication Date: {info['publication_date']}")
                print(f"\nCreators:")
                for creator in info['creators']:
                    print(f"  - {creator.get('name')}")
                print(f"\nCSV Files ({len(info['csv_files'])}):")
                for filename in info['csv_files']:
                    file_info = next(f for f in info['files'] if f['filename'] == filename)
                    size_mb = file_info['size'] / (1024 * 1024)
                    print(f"  - {filename} ({size_mb:.2f} MB)")
                print("=" * 60)
            else:
                # Local file info
                data = pd.read_csv(args.source)
                print("=" * 60)
                print(f"File: {args.source}")
                print("=" * 60)
                print(f"Rows: {len(data)}")
                print(f"Columns: {len(data.columns)}")
                print(f"\nColumn Names:")
                for col in data.columns:
                    dtype = data[col].dtype
                    print(f"  - {col} ({dtype})")
                print("=" * 60)
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Info command failed: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 2
    
    def cmd_cache(self, args) -> int:
        """Execute cache command."""
        try:
            if args.cache_action == 'list':
                cached = self.zenodo_loader.list_cached()
                if not cached:
                    print("No cached datasets")
                    return 0
                
                print("=" * 60)
                print(f"Cached Datasets ({len(cached)})")
                print("=" * 60)
                for item in cached:
                    size_mb = item['cache_size'] / (1024 * 1024)
                    print(f"\nRecord: {item['record_id']}")
                    print(f"  URI: {item['uri']}")
                    print(f"  Size: {size_mb:.2f} MB")
                    print(f"  Rows: {item['rows']}")
                print("=" * 60)
                
            elif args.cache_action == 'clear':
                deleted = self.zenodo_loader.clear_cache(args.record_id)
                if args.record_id:
                    print(f"✓ Cleared cache for record {args.record_id} ({deleted} files)")
                else:
                    print(f"✓ Cleared all cache ({deleted} files)")
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Cache command failed: {e}")
            return 2
    
    def cmd_list_algorithms(self) -> int:
        """Execute list-algorithms command."""
        algorithms = self.algorithm_adapter.list_algorithms()
        
        print("=" * 60)
        print("Available Algorithms")
        print("=" * 60)
        for name, info in algorithms.items():
            print(f"\n{name.upper()}")
            print(f"  Description: {info['description']}")
            print(f"  Parameters: {', '.join(info['parameters'])}")
        print("=" * 60)
        
        return 0
    
    def _format_text(self, result: dict) -> str:
        """Format result as human-readable text."""
        lines = []
        lines.append("=" * 60)
        lines.append("CIRCULAR BIAS DETECTION RESULTS")
        lines.append("=" * 60)
        
        if result['algorithm'] == 'Decision Framework':
            # Comprehensive results
            lines.append(f"\nPSI Score:  {result['psi']:.4f}")
            lines.append(f"CCS Score:  {result['ccs']:.4f}")
            lines.append(f"ρ_PC Score: {result['rho_pc']:+.4f}")
            lines.append(f"\nOverall Bias Detected: {'YES ⚠️' if result['detected'] else 'NO ✓'}")
            lines.append(f"Confidence: {result['confidence']:.1%}")
        else:
            # Single algorithm result
            lines.append(f"\nAlgorithm: {result['algorithm']}")
            lines.append(f"Score: {result['score']:.4f}")
            lines.append(f"Threshold: {result['threshold']:.4f}")
            lines.append(f"Bias Detected: {'YES ⚠️' if result['detected'] else 'NO ✓'}")
        
        lines.append(f"\nInterpretation:")
        lines.append(f"{result['interpretation']}")
        
        if 'details' in result:
            lines.append(f"\nDetails:")
            for key, value in result['details'].items():
                lines.append(f"  {key}: {value}")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _format_csv(self, result: dict) -> str:
        """Format result as CSV."""
        if result['algorithm'] == 'Decision Framework':
            header = "psi,ccs,rho_pc,bias_detected,confidence"
            row = f"{result['psi']:.4f},{result['ccs']:.4f},{result['rho_pc']:.4f},{result['detected']},{result['confidence']:.4f}"
        else:
            header = "algorithm,score,threshold,bias_detected"
            row = f"{result['algorithm']},{result['score']:.4f},{result['threshold']:.4f},{result['detected']}"
        
        return f"{header}\n{row}"

    def cmd_gate(self, args) -> int:
        """Execute CI/CD quality gate.
        Exit codes:
          0 = OK (no critical or warning bias)
          1 = Critical bias detected (block deploy)
          2 = Warning (requires manual review)
        """
        try:
            data = pd.read_csv(args.data_path)
            params = {
                'psi_threshold': args.psi_threshold,
                'ccs_threshold': args.ccs_threshold,
                'rho_pc_threshold': args.rho_threshold,
            }
            result = self.algorithm_adapter.run('decision_framework', data, params)

            # Emit output
            if args.format == 'json':
                output = json.dumps(result, indent=2)
            elif args.format == 'csv':
                output = self._format_csv(result)
            else:
                output = self._format_text(result)

            if args.output:
                Path(args.output).write_text(output, encoding='utf-8')
                print(f"✓ Results written to: {args.output}")
            else:
                print(output)

            detected = bool(result.get('detected', False))
            confidence = float(result.get('confidence', 0.0))

            if detected and confidence >= args.critical_threshold:
                return 1
            if detected or confidence >= args.warn_threshold:
                return 2
            return 0
        except Exception as e:
            self.logger.error(f"Quality gate failed: {e}")
            if getattr(args, 'verbose', False):
                import traceback
                traceback.print_exc()
            # Treat runtime failures as warnings to avoid silent passes
            return 2
    
    def run(self, argv=None):
        """Main entry point."""
        parser = self.create_parser()
        args = parser.parse_args(argv)
        
        if not args.command:
            parser.print_help()
            return 0
        
        # Set logging level
        if args.verbose:
            self.setup_logging('DEBUG')
        
        # Route to command handler
        try:
            if args.command == 'detect':
                return self.cmd_detect(args)
            elif args.command == 'info':
                return self.cmd_info(args)
            elif args.command == 'cache':
                return self.cmd_cache(args)
            elif args.command == 'list-algorithms':
                return self.cmd_list_algorithms()
            elif args.command == 'gate':
                return self.cmd_gate(args)
            else:
                print(f"Unknown command: {args.command}")
                parser.print_help()
                return 1
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return 130


def main():
    """Entry point for console script."""
    cli = CircularBiasCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()

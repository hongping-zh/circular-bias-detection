#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for Circular Bias Detection Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Core dependencies
install_requires = [
    'numpy>=1.20.0',
    'pandas>=1.3.0',
    'scipy>=1.7.0',
]

# CLI dependencies
cli_requires = [
    'requests>=2.26.0',
]

# Visualization dependencies
viz_requires = [
    'matplotlib>=3.4.0',
    'seaborn>=0.11.0',
]

# Development dependencies
dev_requires = [
    'pytest>=6.2.0',
    'pytest-cov>=2.12.0',
    'black>=21.0',
    'flake8>=3.9.0',
]

setup(
    name='circular-bias-detector',
    version='1.0.0',
    description='Detect circular reasoning bias in algorithm evaluation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hongping Zhang',
    author_email='yujjam@uest.edu.gr',
    url='https://github.com/hongping-zh/circular-bias-detection',
    project_urls={
        'Documentation': 'https://github.com/hongping-zh/circular-bias-detection#readme',
        'Source': 'https://github.com/hongping-zh/circular-bias-detection',
        'Dataset': 'https://doi.org/10.5281/zenodo.17201032',
        'Bug Tracker': 'https://github.com/hongping-zh/circular-bias-detection/issues',
    },
    packages=find_packages(exclude=['tests*', 'docs*']),
    python_requires='>=3.8',
    install_requires=install_requires,
    extras_require={
        'cli': cli_requires,
        'viz': viz_requires,
        'dev': dev_requires,
        'all': cli_requires + viz_requires,
    },
    entry_points={
        'console_scripts': [
            'circular-bias=circular_bias_cli.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Creative Commons License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='bias-detection algorithm-evaluation fairness machine-learning',
    license='CC-BY-4.0',
)

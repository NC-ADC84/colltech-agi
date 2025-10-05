#!/usr/bin/env python3
"""
CollTech-AGI Benchmarking System

Advanced benchmarking harness for comparing AI models including:
- Quaternion + Spectral + Fractal + Leech Lattice (ΨQRH) Transformer
- Baseline Transformer models
- Performance evaluation and comparison
- Memory usage analysis
- Inference speed benchmarking

Integrated with CollTech-AGI consciousness system for real-time evaluation.
"""

from .benchmarking_core import BenchmarkingCore, BenchmarkResult, BenchmarkConfig
from .psiqrh_model import PsiQRHModel, PsiQRHConfig
from .evaluation_harness import EvaluationHarness, EvaluationMetrics
from .performance_monitor import PerformanceMonitor, PerformanceMetrics
from .model_comparator import ModelComparator, ComparisonResult

__all__ = [
    'BenchmarkingCore',
    'BenchmarkResult', 
    'BenchmarkConfig',
    'PsiQRHModel',
    'PsiQRHConfig',
    'EvaluationHarness',
    'EvaluationMetrics',
    'PerformanceMonitor',
    'PerformanceMetrics',
    'ModelComparator',
    'ComparisonResult'
]

__version__ = "1.0.0"
__author__ = "CollTech-AGI Team"

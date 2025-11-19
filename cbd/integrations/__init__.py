"""Integration hooks for popular evaluation frameworks."""

from .opencompass_hook import OpenCompassHook
from .lm_eval_hook import LMEvaluationHarnessHook
from .recbole_hook import RecBoleHook

__all__ = [
    'OpenCompassHook',
    'LMEvaluationHarnessHook',
    'RecBoleHook'
]

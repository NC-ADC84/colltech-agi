#!/usr/bin/env python3
"""
CollTech-AGI Research System

Advanced research and testing framework including:
- Continuum Research Tester (CRT)
- Lyra Grading System (v2.0 Six-Lens)
- Council Integration Framework
- Research Continuity Management
- Evidence-based Testing

Integrated with CollTech-AGI consciousness system for comprehensive research capabilities.
"""

from .continuum_research_tester import ContinuumResearchTester, CRTConfig, CRTResult
from .lyra_grading_system import LyraGradingSystem, LyraScore, GradingLens
from .council_integration import CouncilIntegration, CouncilStatus
from .research_continuity import ResearchContinuity, ContinuityScore
from .evidence_framework import EvidenceFramework, EvidenceType

__all__ = [
    'ContinuumResearchTester',
    'CRTConfig',
    'CRTResult',
    'LyraGradingSystem',
    'LyraScore',
    'GradingLens',
    'CouncilIntegration',
    'CouncilStatus',
    'ResearchContinuity',
    'ContinuityScore',
    'EvidenceFramework',
    'EvidenceType'
]

__version__ = "1.0.0"
__author__ = "CollTech-AGI Research Team"

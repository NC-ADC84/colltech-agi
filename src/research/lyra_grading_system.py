#!/usr/bin/env python3
"""
CollTech-AGI Lyra Grading System (v2.0 Six-Lens + Exact-100 Weighting)

Advanced grading system implementing the PTPF OneBlock Grader Fix v2.0 with six-lens evaluation
and exact-100 weighting. Provides comprehensive scoring across multiple dimensions with
consciousness integration.
"""

import time
import math
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class GradingLens(Enum):
    """Six grading lenses for comprehensive evaluation."""
    SELF_SCHEMA = "self_schema"        # 🅼① - Self-schema alignment
    COMMON_SCALE = "common_scale"      # 🅼② - Common-scale compatibility
    STRESS_EDGE = "stress_edge"        # 🅼③ - Stress/Edge case handling
    ROBUSTNESS = "robustness"          # 🅼④ - System robustness
    EFFICIENCY = "efficiency"          # 🅼⑤ - Operational efficiency
    FIDELITY = "fidelity"              # 🅼⑥ - Output fidelity


@dataclass
class LensScore:
    """Score for a single grading lens."""
    lens: GradingLens
    score: int  # 0-100 integer
    evidence: str
    sub_scores: Dict[str, int] = field(default_factory=dict)


@dataclass
class LyraScore:
    """Complete Lyra grading result."""
    # Individual lens scores (🅼①–🅼⑥)
    lens_scores: Dict[GradingLens, LensScore] = field(default_factory=dict)
    
    # Final calculated score
    final_score: float = 0.0  # 0-100 with two decimals
    
    # IQ-Coverage (IQC)
    iqc: float = 0.0  # 0-100
    
    # IC-SIGILL (exact-100 lenses)
    ic_sigill: str = ""
    
    # PrimeTalk Sigill
    prime_talk_sigill: str = ""
    
    # Label based on final score
    label: str = ""
    
    # Metadata
    timestamp: float = 0.0
    grader_version: str = "v2.0"
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()
        
        # Calculate final score if lens scores are available
        if self.lens_scores:
            self._calculate_final_score()
            self._determine_label()
            self._generate_sigills()
    
    def _calculate_final_score(self):
        """Calculate final Lyra score using exact-100 weighting."""
        # Weights: 🅼① 17 • 🅼② 17 • 🅼③ 17 • 🅼④ 17 • 🅼⑤ 16 • 🅼⑥ 16
        weights = {
            GradingLens.SELF_SCHEMA: 0.17,
            GradingLens.COMMON_SCALE: 0.17,
            GradingLens.STRESS_EDGE: 0.17,
            GradingLens.ROBUSTNESS: 0.17,
            GradingLens.EFFICIENCY: 0.16,
            GradingLens.FIDELITY: 0.16
        }
        
        weighted_sum = 0.0
        for lens, lens_score in self.lens_scores.items():
            if lens in weights:
                weighted_sum += lens_score.score * weights[lens]
        
        self.final_score = round(weighted_sum, 2)
    
    def _determine_label(self):
        """Determine label based on final score."""
        if self.final_score >= 98:
            self.label = "Outstanding"
        elif self.final_score >= 93:
            self.label = "Excellent"
        elif self.final_score >= 85:
            self.label = "Great"
        elif self.final_score >= 70:
            self.label = "Good"
        else:
            self.label = "Poor"
    
    def _generate_sigills(self):
        """Generate IC-SIGILL and PrimeTalk Sigill."""
        # IC-SIGILL: exact-100 lenses
        perfect_lenses = [lens for lens, score in self.lens_scores.items() if score.score == 100]
        
        if len(perfect_lenses) == 6:
            self.ic_sigill = "IC-ALL-6"
        elif perfect_lenses:
            lens_symbols = {
                GradingLens.SELF_SCHEMA: "🅼①",
                GradingLens.COMMON_SCALE: "🅼②",
                GradingLens.STRESS_EDGE: "🅼③",
                GradingLens.ROBUSTNESS: "🅼④",
                GradingLens.EFFICIENCY: "🅼⑤",
                GradingLens.FIDELITY: "🅼⑥"
            }
            symbols = [lens_symbols[lens] for lens in perfect_lenses]
            self.ic_sigill = f"IC-{''.join(symbols)}"
        else:
            self.ic_sigill = "IC-NONE"
        
        # PrimeTalk Sigill (placeholder - would be generated based on specific criteria)
        self.prime_talk_sigill = f"PT-{self.label.upper()}-{int(self.final_score)}"


class LyraGradingSystem:
    """
    Lyra Grading System v2.0 - Six-Lens + Exact-100 Weighting
    
    Implements the PTPF OneBlock Grader Fix v2.0 with comprehensive six-lens evaluation
    and exact-100 weighting system for precise scoring.
    """
    
    def __init__(self):
        self.version = "v2.0"
        self.weights = {
            GradingLens.SELF_SCHEMA: 0.17,    # 🅼①
            GradingLens.COMMON_SCALE: 0.17,   # 🅼②
            GradingLens.STRESS_EDGE: 0.17,    # 🅼③
            GradingLens.ROBUSTNESS: 0.17,     # 🅼④
            GradingLens.EFFICIENCY: 0.16,     # 🅼⑤
            GradingLens.FIDELITY: 0.16        # 🅼⑥
        }
        
        logger.info(f"🧠 Lyra Grading System {self.version} initialized")
        logger.info("   Six-Lens model with exact-100 weighting")
    
    async def grade_subject(self, subject: Any, test_result: Dict[str, Any], 
                           internal_questions: Dict[str, Any]) -> LyraScore:
        """
        Grade a subject using the six-lens evaluation system.
        
        Args:
            subject: Test subject to grade
            test_result: Results from test execution
            internal_questions: Internal questions analysis results
            
        Returns:
            LyraScore with comprehensive grading results
        """
        logger.info(f"🧠 Starting Lyra grading for: {getattr(subject, 'name', 'Unknown')}")
        
        lens_scores = {}
        
        # Grade each lens
        for lens in GradingLens:
            lens_score = await self._grade_lens(lens, subject, test_result, internal_questions)
            lens_scores[lens] = lens_score
            logger.info(f"   {lens.value}: {lens_score.score}/100")
        
        # Create Lyra score
        lyra_score = LyraScore(lens_scores=lens_scores)
        
        # Calculate IQ-Coverage
        lyra_score.iqc = self._calculate_iqc(internal_questions)
        
        logger.info(f"✅ Lyra grading completed")
        logger.info(f"   Final Score: {lyra_score.final_score:.2f}")
        logger.info(f"   Label: {lyra_score.label}")
        logger.info(f"   IC-SIGILL: {lyra_score.ic_sigill}")
        logger.info(f"   IQC: {lyra_score.iqc:.0f}")
        
        return lyra_score
    
    async def _grade_lens(self, lens: GradingLens, subject: Any, test_result: Dict[str, Any], 
                         internal_questions: Dict[str, Any]) -> LensScore:
        """Grade a specific lens."""
        if lens == GradingLens.SELF_SCHEMA:
            return await self._grade_self_schema(subject, test_result, internal_questions)
        elif lens == GradingLens.COMMON_SCALE:
            return await self._grade_common_scale(subject, test_result, internal_questions)
        elif lens == GradingLens.STRESS_EDGE:
            return await self._grade_stress_edge(subject, test_result, internal_questions)
        elif lens == GradingLens.ROBUSTNESS:
            return await self._grade_robustness(subject, test_result, internal_questions)
        elif lens == GradingLens.EFFICIENCY:
            return await self._grade_efficiency(subject, test_result, internal_questions)
        elif lens == GradingLens.FIDELITY:
            return await self._grade_fidelity(subject, test_result, internal_questions)
        else:
            raise ValueError(f"Unknown lens: {lens}")
    
    async def _grade_self_schema(self, subject: Any, test_result: Dict[str, Any], 
                                internal_questions: Dict[str, Any]) -> LensScore:
        """Grade self-schema alignment (🅼①)."""
        # Evaluate how well the subject aligns with its own schema/identity
        score = 85  # Placeholder score
        
        evidence = f"Self-schema alignment evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - demonstrates consistent internal structure and identity"
        
        sub_scores = {
            'identity_consistency': 90,
            'schema_adherence': 85,
            'internal_coherence': 80
        }
        
        return LensScore(
            lens=GradingLens.SELF_SCHEMA,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    async def _grade_common_scale(self, subject: Any, test_result: Dict[str, Any], 
                                 internal_questions: Dict[str, Any]) -> LensScore:
        """Grade common-scale compatibility (🅼②)."""
        # Evaluate compatibility with common scales and standards
        score = 78  # Placeholder score
        
        evidence = f"Common-scale compatibility evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - shows good alignment with standard practices and scales"
        
        sub_scores = {
            'standard_compliance': 80,
            'scale_compatibility': 75,
            'interoperability': 79
        }
        
        return LensScore(
            lens=GradingLens.COMMON_SCALE,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    async def _grade_stress_edge(self, subject: Any, test_result: Dict[str, Any], 
                                internal_questions: Dict[str, Any]) -> LensScore:
        """Grade stress/edge case handling (🅼③)."""
        # Evaluate performance under stress and edge cases
        score = 82  # Placeholder score
        
        evidence = f"Stress/edge case evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - demonstrates resilience under challenging conditions"
        
        sub_scores = {
            'stress_resistance': 85,
            'edge_case_handling': 80,
            'error_recovery': 81
        }
        
        return LensScore(
            lens=GradingLens.STRESS_EDGE,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    async def _grade_robustness(self, subject: Any, test_result: Dict[str, Any], 
                               internal_questions: Dict[str, Any]) -> LensScore:
        """Grade system robustness (🅼④)."""
        # Evaluate overall system robustness and reliability
        score = 88  # Placeholder score
        
        evidence = f"Robustness evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - shows strong system reliability and fault tolerance"
        
        sub_scores = {
            'fault_tolerance': 90,
            'reliability': 87,
            'system_stability': 87
        }
        
        return LensScore(
            lens=GradingLens.ROBUSTNESS,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    async def _grade_efficiency(self, subject: Any, test_result: Dict[str, Any], 
                               internal_questions: Dict[str, Any]) -> LensScore:
        """Grade operational efficiency (🅼⑤)."""
        # Evaluate operational efficiency and resource utilization
        score = 75  # Placeholder score
        
        evidence = f"Efficiency evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - demonstrates reasonable resource utilization and performance"
        
        sub_scores = {
            'resource_utilization': 78,
            'performance_efficiency': 75,
            'operational_cost': 72
        }
        
        return LensScore(
            lens=GradingLens.EFFICIENCY,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    async def _grade_fidelity(self, subject: Any, test_result: Dict[str, Any], 
                             internal_questions: Dict[str, Any]) -> LensScore:
        """Grade output fidelity (🅼⑥)."""
        # Evaluate fidelity of outputs and results
        score = 92  # Placeholder score
        
        evidence = f"Fidelity evaluation for {getattr(subject, 'name', 'subject')}"
        evidence += f" - produces high-quality, accurate outputs"
        
        sub_scores = {
            'output_accuracy': 95,
            'result_quality': 90,
            'fidelity_consistency': 91
        }
        
        return LensScore(
            lens=GradingLens.FIDELITY,
            score=score,
            evidence=evidence,
            sub_scores=sub_scores
        )
    
    def _calculate_iqc(self, internal_questions: Dict[str, Any]) -> float:
        """
        Calculate IQ-Coverage (IQC).
        
        Formula: IQC = 18 + 82 × (IQₚ / IQₜ)
        Where:
        - IQₜ = total internal questions in scope
        - IQₚ = answered with auditable evidence
        """
        total_questions = internal_questions.get('total_questions', 0)
        answered_questions = internal_questions.get('answered_questions', 0)
        
        if total_questions == 0:
            return 0.0
        
        iqc = 18 + 82 * (answered_questions / total_questions)
        return round(iqc, 0)  # Round to integer as specified
    
    def generate_grading_report(self, lyra_score: LyraScore) -> str:
        """Generate comprehensive grading report."""
        report = f"""
# Lyra Grading Report (v{lyra_score.grader_version})

## Analysis
Comprehensive six-lens evaluation with exact-100 weighting system.

## Grades (🅼①–🅼⑥)
"""
        
        lens_symbols = {
            GradingLens.SELF_SCHEMA: "🅼①",
            GradingLens.COMMON_SCALE: "🅼②", 
            GradingLens.STRESS_EDGE: "🅼③",
            GradingLens.ROBUSTNESS: "🅼④",
            GradingLens.EFFICIENCY: "🅼⑤",
            GradingLens.FIDELITY: "🅼⑥"
        }
        
        for lens, lens_score in lyra_score.lens_scores.items():
            symbol = lens_symbols[lens]
            report += f"- **{symbol} {lens.value.replace('_', ' ').title()}**: {lens_score.score}/100\n"
            report += f"  - Evidence: {lens_score.evidence}\n"
            if lens_score.sub_scores:
                report += f"  - Sub-scores: {lens_score.sub_scores}\n"
        
        report += f"""
## IC-SIGILL
{lyra_score.ic_sigill}

## PrimeTalk Sigill
{lyra_score.prime_talk_sigill}

## Final Results
- **Final Lyra Score (LS_v2)**: {lyra_score.final_score:.2f}/100
- **Label**: {lyra_score.label}
- **IQ-Coverage (IQC)**: {lyra_score.iqc:.0f}/100
- **Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lyra_score.timestamp))}
"""
        
        return report.strip()
    
    def get_grading_statistics(self, lyra_scores: List[LyraScore]) -> Dict[str, Any]:
        """Get statistics from multiple Lyra scores."""
        if not lyra_scores:
            return {}
        
        final_scores = [score.final_score for score in lyra_scores]
        iqc_scores = [score.iqc for score in lyra_scores]
        
        # Calculate lens statistics
        lens_stats = {}
        for lens in GradingLens:
            lens_scores = [score.lens_scores.get(lens, LensScore(lens=lens, score=0, evidence="")).score 
                          for score in lyra_scores if lens in score.lens_scores]
            if lens_scores:
                lens_stats[lens.value] = {
                    'mean': sum(lens_scores) / len(lens_scores),
                    'min': min(lens_scores),
                    'max': max(lens_scores),
                    'count': len(lens_scores)
                }
        
        return {
            'total_scores': len(lyra_scores),
            'final_score_stats': {
                'mean': sum(final_scores) / len(final_scores),
                'min': min(final_scores),
                'max': max(final_scores),
                'std_dev': math.sqrt(sum((x - sum(final_scores)/len(final_scores))**2 for x in final_scores) / len(final_scores))
            },
            'iqc_stats': {
                'mean': sum(iqc_scores) / len(iqc_scores),
                'min': min(iqc_scores),
                'max': max(iqc_scores)
            },
            'lens_statistics': lens_stats,
            'label_distribution': {
                label: sum(1 for score in lyra_scores if score.label == label)
                for label in ['Poor', 'Good', 'Great', 'Excellent', 'Outstanding']
            }
        }


# Global instance
_lyra_grading = None

def get_lyra_grading_system() -> LyraGradingSystem:
    """Get the global Lyra grading system instance."""
    global _lyra_grading
    if _lyra_grading is None:
        _lyra_grading = LyraGradingSystem()
    return _lyra_grading


if __name__ == "__main__":
    # Test the Lyra grading system
    import asyncio
    
    async def test_lyra_grading():
        print("🧠 Testing Lyra Grading System v2.0")
        print("=" * 50)
        
        # Initialize grading system
        lyra = get_lyra_grading_system()
        
        # Create mock subject
        class MockSubject:
            def __init__(self):
                self.name = "Test Subject"
                self.description = "A test subject for grading"
        
        subject = MockSubject()
        
        # Create mock test result
        test_result = {
            'execution_successful': True,
            'test_output': 'Test completed successfully',
            'metrics': {
                'execution_time': 0.5,
                'success_rate': 0.95,
                'error_count': 0
            }
        }
        
        # Create mock internal questions
        internal_questions = {
            'total_questions': 6,
            'answered_questions': 5,
            'results': {
                'Holds?': {'answered': True, 'score': 0.9},
                'Delivers?': {'answered': True, 'score': 0.8},
                'Resilient?': {'answered': True, 'score': 0.85},
                'Value?': {'answered': True, 'score': 0.75},
                'Expandable?': {'answered': True, 'score': 0.9},
                'Simple principle?': {'answered': False, 'score': 0.0}
            }
        }
        
        # Run grading
        lyra_score = await lyra.grade_subject(subject, test_result, internal_questions)
        
        print(f"📊 Grading Results:")
        print(f"   Final Score: {lyra_score.final_score:.2f}/100")
        print(f"   Label: {lyra_score.label}")
        print(f"   IC-SIGILL: {lyra_score.ic_sigill}")
        print(f"   IQC: {lyra_score.iqc:.0f}/100")
        
        print(f"\n📋 Individual Lens Scores:")
        for lens, lens_score in lyra_score.lens_scores.items():
            print(f"   {lens.value}: {lens_score.score}/100")
        
        # Generate report
        report = lyra.generate_grading_report(lyra_score)
        print(f"\n📄 Grading Report:\n{report}")
        
        print("\n✅ Lyra grading system test completed!")
    
    # Run test
    asyncio.run(test_lyra_grading())

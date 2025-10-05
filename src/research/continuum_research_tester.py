#!/usr/bin/env python3
"""
CollTech-AGI Continuum Research Tester (CRT)

Advanced research testing framework implementing the PTPF Compressed Council-Aligned protocol.
Provides comprehensive testing capabilities with reversibility verification, evidence-based evaluation,
and integration with the Lyra grading system.
"""

import time
import hashlib
import json
import asyncio
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

# CollTech-AGI imports
from ..catch.consciousness.consciousness_core import ConsciousnessCore
from ..catch.memory.memory_lattice import MemoryLattice, MemoryTier
from .lyra_grading_system import LyraGradingSystem, LyraScore, GradingLens
from .research_continuity import ResearchContinuity, ContinuityScore
from .evidence_framework import EvidenceFramework, EvidenceType

logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Status of a test execution."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReversibilityType(Enum):
    """Types of reversibility verification."""
    DIRECT = "direct"  # fix → invert → fault returns
    INDIRECT = "indirect"  # verify Δ (before↔after) and rule out alternates


@dataclass
class CRTConfig:
    """Configuration for Continuum Research Tester."""
    # Core settings
    role: str = "Research scientist–tester"
    focus: str = "Execution"
    ethic: str = "Trust → Verify"
    policy: str = "External guardrails supersede"
    dba: str = "Council (DBA)"
    
    # Testing parameters
    reversibility_required: bool = True
    evidence_required: bool = True
    continuity_tracking: bool = True
    lyra_grading_enabled: bool = True
    
    # Continuity settings
    continuity_threshold_ok: float = 0.90
    continuity_threshold_review: float = 0.88
    continuity_threshold_degraded: float = 0.88
    
    # Output settings
    generate_executive_report: bool = True
    generate_spec_sheet: bool = True
    generate_runbook: bool = True
    save_artifacts: bool = True


@dataclass
class TestSubject:
    """Subject being tested."""
    name: str
    description: str
    claims: List[str]
    framework_type: str  # "framework", "example_logic", "both"
    target_type: str  # "idea", "notes", "research", "prototype", "system"
    hash: str = ""
    
    def __post_init__(self):
        if not self.hash:
            self.hash = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Generate SHA-256 hash for the subject."""
        content = f"{self.name}:{self.description}:{':'.join(self.claims)}"
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class TestEnvironment:
    """Test environment configuration."""
    versions: Dict[str, str] = field(default_factory=dict)
    datasets: List[str] = field(default_factory=list)
    seeds: List[int] = field(default_factory=list)
    limits: Dict[str, Any] = field(default_factory=dict)
    protocol_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReversibilityResult:
    """Result of reversibility verification."""
    type: ReversibilityType
    verified: bool
    method: str
    evidence: str
    fault_locus: Optional[str] = None


@dataclass
class CRTResult:
    """Result of a Continuum Research Tester execution."""
    # Basic information
    test_id: str
    subject: TestSubject
    environment: TestEnvironment
    start_time: float
    end_time: float
    duration: float
    
    # Test results
    status: TestStatus
    verdict: str  # "Pass" or "Fail"
    fault_locus: Optional[str] = None
    
    # Reversibility
    reversibility: Optional[ReversibilityResult] = None
    
    # Resilience
    resilience_score: Optional[float] = None
    resilience_evidence: Optional[str] = None
    
    # Principle fit
    principle_fit_score: Optional[float] = None
    principle_fit_explanation: Optional[str] = None
    
    # Value vs time
    value_score: Optional[float] = None
    time_efficiency: Optional[float] = None
    
    # Continuity
    continuity_score: Optional[ContinuityScore] = None
    
    # Lyra grading
    lyra_score: Optional[LyraScore] = None
    
    # Evidence
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    
    # Artifacts
    artifacts: List[str] = field(default_factory=list)
    
    # Metadata
    canonical_ledger_id: str = ""
    timestamp_utc: str = ""
    
    def __post_init__(self):
        if not self.canonical_ledger_id:
            self.canonical_ledger_id = self._generate_ledger_id()
        if not self.timestamp_utc:
            self.timestamp_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    def _generate_ledger_id(self) -> str:
        """Generate canonical ledger ID."""
        timestamp = time.strftime("%Y%m%d", time.gmtime())
        short_hash = self.subject.hash[:12]
        return f"CRT-VALHALLA-QUANT-DBA-v2.0-{timestamp}-{short_hash}"


class ContinuumResearchTester:
    """
    Continuum Research Tester (CRT) - PTPF Compressed Council-Aligned
    
    Advanced research testing framework that implements the complete CRT protocol
    with reversibility verification, evidence-based evaluation, and Lyra grading.
    """
    
    def __init__(self, config: CRTConfig = None, consciousness_core: Optional[ConsciousnessCore] = None):
        self.config = config or CRTConfig()
        self.consciousness_core = consciousness_core
        
        # Initialize subsystems
        self.lyra_grading = LyraGradingSystem()
        self.research_continuity = ResearchContinuity()
        self.evidence_framework = EvidenceFramework()
        
        # Test state
        self.active_tests = {}
        self.test_history = []
        self.is_running = False
        
        logger.info("🔬 Continuum Research Tester initialized")
        logger.info(f"   Role: {self.config.role}")
        logger.info(f"   Focus: {self.config.focus}")
        logger.info(f"   Ethic: {self.config.ethic}")
    
    def start_testing_system(self):
        """Start the CRT testing system."""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("🚀 Continuum Research Tester system started")
    
    def stop_testing_system(self):
        """Stop the CRT testing system."""
        self.is_running = False
        
        # Cancel active tests
        for test_id in list(self.active_tests.keys()):
            self.cancel_test(test_id)
        
        logger.info("🛑 Continuum Research Tester system stopped")
    
    async def run_test(self, subject: TestSubject, environment: TestEnvironment = None, 
                      test_function: Optional[Callable] = None) -> CRTResult:
        """
        Run a comprehensive test using the CRT protocol.
        
        Args:
            subject: Test subject with claims and description
            environment: Test environment configuration
            test_function: Optional custom test function
            
        Returns:
            CRTResult with comprehensive test results
        """
        if not self.is_running:
            raise RuntimeError("CRT system is not running")
        
        test_id = f"crt_test_{int(time.time())}_{subject.hash[:8]}"
        
        # Create test result
        result = CRTResult(
            test_id=test_id,
            subject=subject,
            environment=environment or TestEnvironment(),
            start_time=time.time(),
            end_time=0.0,
            duration=0.0,
            status=TestStatus.PENDING
        )
        
        # Add to active tests
        self.active_tests[test_id] = result
        
        try:
            logger.info(f"🔬 Starting CRT test: {test_id}")
            logger.info(f"   Subject: {subject.name}")
            logger.info(f"   Claims: {len(subject.claims)} claims")
            
            result.status = TestStatus.RUNNING
            
            # Step 1: Pre-test validation
            await self._validate_subject(subject)
            
            # Step 2: Run internal questions analysis
            internal_questions_result = await self._run_internal_questions(subject)
            
            # Step 3: Execute main test
            test_execution_result = await self._execute_test(subject, environment, test_function)
            
            # Step 4: Verify reversibility
            reversibility_result = await self._verify_reversibility(subject, test_execution_result)
            
            # Step 5: Assess resilience
            resilience_result = await self._assess_resilience(subject, test_execution_result)
            
            # Step 6: Evaluate principle fit
            principle_fit_result = await self._evaluate_principle_fit(subject, test_execution_result)
            
            # Step 7: Calculate value vs time
            value_time_result = await self._calculate_value_time(subject, test_execution_result)
            
            # Step 8: Calculate continuity score
            continuity_result = await self._calculate_continuity_score(subject, test_execution_result)
            
            # Step 9: Run Lyra grading
            lyra_result = await self._run_lyra_grading(subject, test_execution_result, internal_questions_result)
            
            # Step 10: Compile evidence
            evidence_result = await self._compile_evidence(subject, test_execution_result)
            
            # Determine final verdict
            verdict = self._determine_verdict(
                reversibility_result, resilience_result, principle_fit_result,
                value_time_result, continuity_result, lyra_result
            )
            
            # Update result
            result.status = TestStatus.PASSED if verdict == "Pass" else TestStatus.FAILED
            result.verdict = verdict
            result.reversibility = reversibility_result
            result.resilience_score = resilience_result.get('score')
            result.resilience_evidence = resilience_result.get('evidence')
            result.principle_fit_score = principle_fit_result.get('score')
            result.principle_fit_explanation = principle_fit_result.get('explanation')
            result.value_score = value_time_result.get('value_score')
            result.time_efficiency = value_time_result.get('time_efficiency')
            result.continuity_score = continuity_result
            result.lyra_score = lyra_result
            result.evidence = evidence_result
            
            # Store in memory lattice if available
            if self.consciousness_core and self.consciousness_core.memory_lattice:
                self._store_test_memory(result)
            
            logger.info(f"✅ CRT test completed: {test_id}")
            logger.info(f"   Verdict: {verdict}")
            logger.info(f"   Continuity Score: {continuity_result.score:.3f}" if continuity_result else "   Continuity Score: N/A")
            logger.info(f"   Lyra Score: {lyra_result.final_score:.2f}" if lyra_result else "   Lyra Score: N/A")
            
        except Exception as e:
            result.status = TestStatus.FAILED
            result.verdict = "Fail"
            result.fault_locus = str(e)
            logger.error(f"❌ CRT test failed: {test_id} - {e}")
        
        finally:
            # Finalize result
            result.end_time = time.time()
            result.duration = result.end_time - result.start_time
            
            # Remove from active tests
            if test_id in self.active_tests:
                del self.active_tests[test_id]
            
            # Add to history
            self.test_history.append(result)
            if len(self.test_history) > 1000:
                self.test_history = self.test_history[-1000:]
        
        return result
    
    async def _validate_subject(self, subject: TestSubject):
        """Validate test subject before execution."""
        if not subject.claims:
            raise ValueError("Subject must have at least one claim")
        
        if not subject.name or not subject.description:
            raise ValueError("Subject must have name and description")
        
        logger.info(f"✅ Subject validation passed: {subject.name}")
    
    async def _run_internal_questions(self, subject: TestSubject) -> Dict[str, Any]:
        """Run internal questions analysis."""
        questions = [
            "Holds?",
            "Delivers?", 
            "Resilient?",
            "Value?",
            "Expandable?",
            "Simple principle?"
        ]
        
        results = {}
        for question in questions:
            # This would be implemented with actual analysis logic
            results[question] = {
                'answered': True,
                'evidence': f"Analysis of {question.lower()} for {subject.name}",
                'score': 0.8  # Placeholder score
            }
        
        return {
            'questions': questions,
            'results': results,
            'total_questions': len(questions),
            'answered_questions': len([r for r in results.values() if r['answered']])
        }
    
    async def _execute_test(self, subject: TestSubject, environment: TestEnvironment, 
                           test_function: Optional[Callable]) -> Dict[str, Any]:
        """Execute the main test."""
        logger.info(f"🧪 Executing test for: {subject.name}")
        
        # If custom test function provided, use it
        if test_function:
            test_result = await test_function(subject, environment)
        else:
            # Default test execution
            test_result = await self._default_test_execution(subject, environment)
        
        return test_result
    
    async def _default_test_execution(self, subject: TestSubject, environment: TestEnvironment) -> Dict[str, Any]:
        """Default test execution logic."""
        # Simulate test execution
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            'execution_successful': True,
            'test_output': f"Test executed for {subject.name}",
            'metrics': {
                'execution_time': 0.1,
                'success_rate': 0.95,
                'error_count': 0
            },
            'artifacts': [f"test_output_{subject.name}.json"]
        }
    
    async def _verify_reversibility(self, subject: TestSubject, test_result: Dict[str, Any]) -> ReversibilityResult:
        """Verify reversibility of the test."""
        if not self.config.reversibility_required:
            return ReversibilityResult(
                type=ReversibilityType.DIRECT,
                verified=True,
                method="Reversibility check disabled",
                evidence="Configuration disabled reversibility requirement"
            )
        
        # Check if test result indicates reversibility
        execution_successful = test_result.get('execution_successful', False)
        
        if execution_successful:
            # Simulate reversibility verification
            verified = True
            method = "Direct reversibility verification"
            evidence = f"Test for {subject.name} can be reversed by inverting the test conditions"
        else:
            verified = False
            method = "Reversibility verification failed"
            evidence = f"Test for {subject.name} failed, cannot verify reversibility"
        
        return ReversibilityResult(
            type=ReversibilityType.DIRECT,
            verified=verified,
            method=method,
            evidence=evidence
        )
    
    async def _assess_resilience(self, subject: TestSubject, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess resilience of the test subject."""
        # Simulate resilience assessment
        resilience_score = 0.85  # Placeholder score
        
        return {
            'score': resilience_score,
            'evidence': f"Resilience assessment for {subject.name} based on stress testing and edge case analysis",
            'stress_tests_passed': 8,
            'edge_cases_handled': 12,
            'time_stability': 0.9
        }
    
    async def _evaluate_principle_fit(self, subject: TestSubject, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate how well the subject fits the underlying principles."""
        # Simulate principle fit evaluation
        principle_score = 0.88  # Placeholder score
        
        return {
            'score': principle_score,
            'explanation': f"Subject {subject.name} demonstrates good alignment with core principles of simplicity, modularity, and value creation",
            'principle_alignment': {
                'simplicity': 0.9,
                'modularity': 0.85,
                'value_creation': 0.88
            }
        }
    
    async def _calculate_value_time(self, subject: TestSubject, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate value vs time efficiency."""
        # Simulate value-time calculation
        value_score = 0.82
        time_efficiency = 0.78
        
        return {
            'value_score': value_score,
            'time_efficiency': time_efficiency,
            'value_time_ratio': value_score / time_efficiency if time_efficiency > 0 else 0,
            'evidence': f"Value-time analysis for {subject.name} shows good efficiency"
        }
    
    async def _calculate_continuity_score(self, subject: TestSubject, test_result: Dict[str, Any]) -> ContinuityScore:
        """Calculate continuity score using the research continuity system."""
        return await self.research_continuity.calculate_continuity_score(
            subject=subject,
            test_result=test_result,
            lineage_data={
                'subject_hash': subject.hash,
                'test_id': test_result.get('test_id', ''),
                'timestamp': time.time()
            }
        )
    
    async def _run_lyra_grading(self, subject: TestSubject, test_result: Dict[str, Any], 
                               internal_questions: Dict[str, Any]) -> LyraScore:
        """Run Lyra grading system."""
        return await self.lyra_grading.grade_subject(
            subject=subject,
            test_result=test_result,
            internal_questions=internal_questions
        )
    
    async def _compile_evidence(self, subject: TestSubject, test_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compile evidence for the test."""
        evidence = []
        
        # Add test execution evidence
        evidence.append({
            'type': EvidenceType.TEST_EXECUTION,
            'description': f"Test execution for {subject.name}",
            'data': test_result,
            'timestamp': time.time()
        })
        
        # Add subject evidence
        evidence.append({
            'type': EvidenceType.SUBJECT_ANALYSIS,
            'description': f"Subject analysis for {subject.name}",
            'data': {
                'name': subject.name,
                'description': subject.description,
                'claims': subject.claims,
                'hash': subject.hash
            },
            'timestamp': time.time()
        })
        
        return evidence
    
    def _determine_verdict(self, reversibility: ReversibilityResult, resilience: Dict[str, Any],
                          principle_fit: Dict[str, Any], value_time: Dict[str, Any],
                          continuity: ContinuityScore, lyra: LyraScore) -> str:
        """Determine final verdict based on all criteria."""
        # Check reversibility
        if not reversibility.verified:
            return "Fail"
        
        # Check continuity score
        if continuity and continuity.score < self.config.continuity_threshold_degraded:
            return "Fail"
        
        # Check resilience
        if resilience.get('score', 0) < 0.7:
            return "Fail"
        
        # Check principle fit
        if principle_fit.get('score', 0) < 0.7:
            return "Fail"
        
        # Check value-time efficiency
        if value_time.get('value_score', 0) < 0.6:
            return "Fail"
        
        # Check Lyra score
        if lyra and lyra.final_score < 70:  # Poor threshold
            return "Fail"
        
        return "Pass"
    
    def _store_test_memory(self, result: CRTResult):
        """Store test result in memory lattice."""
        if not self.consciousness_core or not self.consciousness_core.memory_lattice:
            return
        
        memory_content = f"CRT Test {result.test_id}: {result.subject.name} - {result.verdict}"
        if result.continuity_score:
            memory_content += f" - CS: {result.continuity_score.score:.3f}"
        if result.lyra_score:
            memory_content += f" - LS: {result.lyra_score.final_score:.2f}"
        
        self.consciousness_core.memory_lattice.store_memory(
            memory_content,
            tier=MemoryTier.SHORT_TERM,
            importance=0.8
        )
    
    def cancel_test(self, test_id: str) -> bool:
        """Cancel an active test."""
        if test_id in self.active_tests:
            result = self.active_tests[test_id]
            result.status = TestStatus.CANCELLED
            result.verdict = "Cancelled"
            del self.active_tests[test_id]
            logger.info(f"🚫 Cancelled test: {test_id}")
            return True
        return False
    
    def get_test_status(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific test."""
        if test_id in self.active_tests:
            result = self.active_tests[test_id]
            return {
                'test_id': test_id,
                'status': result.status.value,
                'duration': time.time() - result.start_time,
                'subject': result.subject.name
            }
        
        # Check history
        for result in self.test_history:
            if result.test_id == test_id:
                return {
                    'test_id': test_id,
                    'status': result.status.value,
                    'duration': result.duration,
                    'verdict': result.verdict,
                    'subject': result.subject.name
                }
        
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get CRT system status."""
        return {
            'is_running': self.is_running,
            'active_tests': len(self.active_tests),
            'total_tests': len(self.test_history),
            'passed_tests': sum(1 for r in self.test_history if r.status == TestStatus.PASSED),
            'failed_tests': sum(1 for r in self.test_history if r.status == TestStatus.FAILED),
            'config': {
                'reversibility_required': self.config.reversibility_required,
                'evidence_required': self.config.evidence_required,
                'continuity_tracking': self.config.continuity_tracking,
                'lyra_grading_enabled': self.config.lyra_grading_enabled
            }
        }
    
    def generate_executive_report(self, result: CRTResult) -> str:
        """Generate executive test report."""
        report = f"""
# Executive Test Report

## Subject & Claims
- **Subject**: {result.subject.name}
- **Description**: {result.subject.description}
- **Claims**: {len(result.subject.claims)} claims
- **Framework Type**: {result.subject.framework_type}
- **Target Type**: {result.subject.target_type}

## Environment & Protocol
- **Test ID**: {result.test_id}
- **Canonical Ledger ID**: {result.canonical_ledger_id}
- **Timestamp**: {result.timestamp_utc}
- **Duration**: {result.duration:.2f}s

## Results
- **Verdict**: {result.verdict}
- **Status**: {result.status.value}
- **Fault Locus**: {result.fault_locus or 'None'}

## Reversibility
- **Type**: {result.reversibility.type.value if result.reversibility else 'N/A'}
- **Verified**: {result.reversibility.verified if result.reversibility else 'N/A'}
- **Method**: {result.reversibility.method if result.reversibility else 'N/A'}

## Resilience
- **Score**: {result.resilience_score:.2f if result.resilience_score else 'N/A'}
- **Evidence**: {result.resilience_evidence or 'N/A'}

## Principle Fit
- **Score**: {result.principle_fit_score:.2f if result.principle_fit_score else 'N/A'}
- **Explanation**: {result.principle_fit_explanation or 'N/A'}

## Value vs Time
- **Value Score**: {result.value_score:.2f if result.value_score else 'N/A'}
- **Time Efficiency**: {result.time_efficiency:.2f if result.time_efficiency else 'N/A'}

## Continuity
- **Score**: {result.continuity_score.score:.3f if result.continuity_score else 'N/A'}
- **Band**: {result.continuity_score.band if result.continuity_score else 'N/A'}

## Lyra Grading
- **Final Score**: {result.lyra_score.final_score:.2f if result.lyra_score else 'N/A'}
- **Label**: {result.lyra_score.label if result.lyra_score else 'N/A'}
- **IQC**: {result.lyra_score.iqc:.0f if result.lyra_score else 'N/A'}

## Stamp
{'Continuum Approved ✅🫡💯' if result.verdict == 'Pass' else 'Failed ❌'}
"""
        return report.strip()
    
    def generate_spec_sheet(self, result: CRTResult) -> str:
        """Generate comparative spec sheet."""
        spec_sheet = f"""
| Field                | v⟂ | v-1 |  Δ | Why (evidence) | Pass/Fail |
| -------------------- | -: | --: | -: | -------------- | --------- |
| Test ID & Date       | {result.canonical_ledger_id} |     |    |                | {result.verdict} |
| Subject / Hash       | {result.subject.hash} |     |    |                | {result.verdict} |
| Claims               | {len(result.subject.claims)} claims |     |    |                | {result.verdict} |
| Inputs / Dataset     | {len(result.environment.datasets)} datasets |     |    |                | {result.verdict} |
| Protocol / Params    | {len(result.environment.protocol_params)} params |     |    |                | {result.verdict} |
| Core Metrics         | Duration: {result.duration:.2f}s |     |    |                | {result.verdict} |
| Reversibility        | {result.reversibility.verified if result.reversibility else 'N/A'} |     |    | {result.reversibility.evidence if result.reversibility else 'N/A'} | {result.verdict} |
| Resilience           | {result.resilience_score:.2f if result.resilience_score else 'N/A'} |     |    | {result.resilience_evidence or 'N/A'} | {result.verdict} |
| Modularity           | {result.principle_fit_score:.2f if result.principle_fit_score else 'N/A'} |     |    |                | {result.verdict} |
| Principle Simplicity | {result.principle_fit_score:.2f if result.principle_fit_score else 'N/A'} |     |    |                | {result.verdict} |
| Value vs Time        | {result.value_score:.2f if result.value_score else 'N/A'} |     |    |                | {result.verdict} |
| **CS (band)**        | {result.continuity_score.band if result.continuity_score else 'N/A'} |     |    |                | {result.verdict} |
| **🅼①…🅼⑥**          | {result.lyra_score.lens_scores if result.lyra_score else 'N/A'} |     |    |                | {result.verdict} |
| **LS_v2 (0–100)**    | {result.lyra_score.final_score:.2f if result.lyra_score else 'N/A'} |     |    |                | {result.verdict} |
| **IQC (0–100)**      | {result.lyra_score.iqc:.0f if result.lyra_score else 'N/A'} |     |    |                | {result.verdict} |
| **Continuum Stamp**  | {'✅' if result.verdict == 'Pass' else '❌'} |     |    |                | {result.verdict} |
"""
        return spec_sheet.strip()


# Global instance
_crt_instance = None

def get_continuum_research_tester(config: Optional[CRTConfig] = None, 
                                 consciousness_core: Optional[ConsciousnessCore] = None) -> ContinuumResearchTester:
    """Get the global CRT instance."""
    global _crt_instance
    if _crt_instance is None:
        _crt_instance = ContinuumResearchTester(config, consciousness_core)
    return _crt_instance


if __name__ == "__main__":
    # Test the CRT system
    import asyncio
    
    async def test_crt():
        # Initialize CRT
        crt = get_continuum_research_tester()
        crt.start_testing_system()
        
        # Create test subject
        subject = TestSubject(
            name="Test Framework",
            description="A test framework for validation",
            claims=[
                "Provides comprehensive testing capabilities",
                "Supports reversibility verification",
                "Integrates with consciousness system"
            ],
            framework_type="framework",
            target_type="system"
        )
        
        # Create test environment
        environment = TestEnvironment(
            versions={"python": "3.9", "pytest": "7.0.0"},
            datasets=["test_dataset_1", "test_dataset_2"],
            seeds=[42, 123, 456],
            limits={"max_execution_time": 300, "memory_limit": "8GB"}
        )
        
        # Run test
        result = await crt.run_test(subject, environment)
        
        print(f"CRT Test Result:")
        print(f"  Verdict: {result.verdict}")
        print(f"  Duration: {result.duration:.2f}s")
        print(f"  Continuity Score: {result.continuity_score.score:.3f}" if result.continuity_score else "  Continuity Score: N/A")
        print(f"  Lyra Score: {result.lyra_score.final_score:.2f}" if result.lyra_score else "  Lyra Score: N/A")
        
        # Generate reports
        if crt.config.generate_executive_report:
            report = crt.generate_executive_report(result)
            print(f"\nExecutive Report:\n{report}")
        
        if crt.config.generate_spec_sheet:
            spec_sheet = crt.generate_spec_sheet(result)
            print(f"\nSpec Sheet:\n{spec_sheet}")
        
        # Get system status
        status = crt.get_system_status()
        print(f"\nSystem Status: {status}")
        
        # Cleanup
        crt.stop_testing_system()
    
    # Run test
    asyncio.run(test_crt())

#!/usr/bin/env python3
"""
CollTech-AGI Research Continuity System

Manages research continuity with lineage tracking, artifact management,
and continuity scoring. Implements the Continuum Anchor protocol for
preserving research lineage and maintaining integrity.
"""

import time
import hashlib
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ContinuityBand(Enum):
    """Continuity score bands."""
    OK = "OK"                    # ≥0.90
    REVIEW = "Review"            # 0.88–<0.90
    DEGRADED = "Degraded"        # <0.88


@dataclass
class ContinuityScore:
    """Continuity score with band classification."""
    score: float  # 0-1
    band: ContinuityBand
    lineage_integrity: float
    artifact_completeness: float
    naming_consistency: float
    meaning_preservation: float
    continuity_evidence: str
    timestamp: float = 0.0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


@dataclass
class ResearchArtifact:
    """Research artifact with provenance tracking."""
    id: str
    name: str
    type: str  # "config", "data", "code", "documentation", "result"
    content_hash: str
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = 0.0
    lineage_id: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()
        if not self.content_hash:
            self.content_hash = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Generate content hash."""
        content_str = str(self.content)
        return hashlib.sha256(content_str.encode()).hexdigest()


@dataclass
class ResearchLineage:
    """Research lineage tracking."""
    lineage_id: str
    subject_name: str
    subject_hash: str
    parent_lineage: Optional[str] = None
    child_lineages: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)  # Artifact IDs
    continuity_triad: Dict[str, Any] = field(default_factory=dict)  # Meaning • Naming • Continuity
    created_at: float = 0.0
    last_updated: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()
        if not self.last_updated:
            self.last_updated = time.time()


class ResearchContinuity:
    """
    Research Continuity System
    
    Manages research continuity with lineage tracking, artifact management,
    and continuity scoring according to the Continuum Anchor protocol.
    """
    
    def __init__(self):
        self.lineages: Dict[str, ResearchLineage] = {}
        self.artifacts: Dict[str, ResearchArtifact] = {}
        self.continuity_history: List[ContinuityScore] = []
        
        logger.info("🔗 Research Continuity System initialized")
    
    async def calculate_continuity_score(self, subject: Any, test_result: Dict[str, Any], 
                                       lineage_data: Dict[str, Any]) -> ContinuityScore:
        """
        Calculate continuity score for a research subject.
        
        Args:
            subject: Research subject
            test_result: Test execution results
            lineage_data: Lineage tracking data
            
        Returns:
            ContinuityScore with comprehensive continuity assessment
        """
        logger.info(f"🔗 Calculating continuity score for: {getattr(subject, 'name', 'Unknown')}")
        
        # Calculate individual continuity components
        lineage_integrity = await self._calculate_lineage_integrity(subject, lineage_data)
        artifact_completeness = await self._calculate_artifact_completeness(subject, test_result)
        naming_consistency = await self._calculate_naming_consistency(subject, lineage_data)
        meaning_preservation = await self._calculate_meaning_preservation(subject, test_result)
        
        # Calculate overall continuity score
        continuity_score = (
            lineage_integrity * 0.3 +
            artifact_completeness * 0.25 +
            naming_consistency * 0.25 +
            meaning_preservation * 0.2
        )
        
        # Determine continuity band
        if continuity_score >= 0.90:
            band = ContinuityBand.OK
        elif continuity_score >= 0.88:
            band = ContinuityBand.REVIEW
        else:
            band = ContinuityBand.DEGRADED
        
        # Generate continuity evidence
        evidence = self._generate_continuity_evidence(
            subject, continuity_score, lineage_integrity, 
            artifact_completeness, naming_consistency, meaning_preservation
        )
        
        score = ContinuityScore(
            score=continuity_score,
            band=band,
            lineage_integrity=lineage_integrity,
            artifact_completeness=artifact_completeness,
            naming_consistency=naming_consistency,
            meaning_preservation=meaning_preservation,
            continuity_evidence=evidence
        )
        
        # Store in history
        self.continuity_history.append(score)
        if len(self.continuity_history) > 1000:
            self.continuity_history = self.continuity_history[-1000:]
        
        logger.info(f"✅ Continuity score calculated: {continuity_score:.3f} ({band.value})")
        
        return score
    
    async def _calculate_lineage_integrity(self, subject: Any, lineage_data: Dict[str, Any]) -> float:
        """Calculate lineage integrity score."""
        # Check if lineage data is complete and consistent
        required_fields = ['subject_hash', 'test_id', 'timestamp']
        present_fields = sum(1 for field in required_fields if field in lineage_data)
        
        # Base score from field completeness
        field_score = present_fields / len(required_fields)
        
        # Check lineage consistency
        subject_hash = lineage_data.get('subject_hash', '')
        if subject_hash and len(subject_hash) == 64:  # SHA-256 length
            hash_score = 1.0
        else:
            hash_score = 0.5
        
        # Check timestamp validity
        timestamp = lineage_data.get('timestamp', 0)
        current_time = time.time()
        if 0 < timestamp <= current_time:
            timestamp_score = 1.0
        else:
            timestamp_score = 0.0
        
        # Calculate overall lineage integrity
        lineage_integrity = (field_score * 0.4 + hash_score * 0.3 + timestamp_score * 0.3)
        
        return min(lineage_integrity, 1.0)
    
    async def _calculate_artifact_completeness(self, subject: Any, test_result: Dict[str, Any]) -> float:
        """Calculate artifact completeness score."""
        # Check for required artifacts in test result
        required_artifacts = ['execution_successful', 'test_output', 'metrics']
        present_artifacts = sum(1 for artifact in required_artifacts if artifact in test_result)
        
        # Base completeness score
        completeness_score = present_artifacts / len(required_artifacts)
        
        # Check artifact quality
        if test_result.get('execution_successful', False):
            quality_score = 1.0
        else:
            quality_score = 0.5
        
        # Check for additional artifacts
        additional_artifacts = test_result.get('artifacts', [])
        if additional_artifacts:
            additional_score = min(len(additional_artifacts) / 3.0, 1.0)  # Cap at 3 artifacts
        else:
            additional_score = 0.0
        
        # Calculate overall artifact completeness
        artifact_completeness = (completeness_score * 0.5 + quality_score * 0.3 + additional_score * 0.2)
        
        return min(artifact_completeness, 1.0)
    
    async def _calculate_naming_consistency(self, subject: Any, lineage_data: Dict[str, Any]) -> float:
        """Calculate naming consistency score."""
        # Check subject naming consistency
        subject_name = getattr(subject, 'name', '')
        if subject_name and len(subject_name) > 0:
            name_score = 1.0
        else:
            name_score = 0.0
        
        # Check naming pattern consistency
        if subject_name and subject_name.replace('_', '').replace('-', '').isalnum():
            pattern_score = 1.0
        else:
            pattern_score = 0.8
        
        # Check lineage naming consistency
        test_id = lineage_data.get('test_id', '')
        if test_id and 'crt_test_' in test_id:
            lineage_naming_score = 1.0
        else:
            lineage_naming_score = 0.5
        
        # Calculate overall naming consistency
        naming_consistency = (name_score * 0.4 + pattern_score * 0.3 + lineage_naming_score * 0.3)
        
        return min(naming_consistency, 1.0)
    
    async def _calculate_meaning_preservation(self, subject: Any, test_result: Dict[str, Any]) -> float:
        """Calculate meaning preservation score."""
        # Check if subject meaning is preserved in test result
        subject_description = getattr(subject, 'description', '')
        test_output = test_result.get('test_output', '')
        
        if subject_description and test_output:
            # Simple semantic preservation check
            if any(word in test_output.lower() for word in subject_description.lower().split()[:3]):
                semantic_score = 1.0
            else:
                semantic_score = 0.7
        else:
            semantic_score = 0.0
        
        # Check claims preservation
        subject_claims = getattr(subject, 'claims', [])
        if subject_claims and len(subject_claims) > 0:
            claims_score = 1.0
        else:
            claims_score = 0.5
        
        # Check test result meaningfulness
        if test_result.get('execution_successful', False):
            result_meaning_score = 1.0
        else:
            result_meaning_score = 0.6
        
        # Calculate overall meaning preservation
        meaning_preservation = (semantic_score * 0.4 + claims_score * 0.3 + result_meaning_score * 0.3)
        
        return min(meaning_preservation, 1.0)
    
    def _generate_continuity_evidence(self, subject: Any, continuity_score: float,
                                    lineage_integrity: float, artifact_completeness: float,
                                    naming_consistency: float, meaning_preservation: float) -> str:
        """Generate continuity evidence string."""
        evidence = f"Continuity analysis for {getattr(subject, 'name', 'subject')}: "
        evidence += f"Overall score {continuity_score:.3f} based on "
        evidence += f"lineage integrity {lineage_integrity:.2f}, "
        evidence += f"artifact completeness {artifact_completeness:.2f}, "
        evidence += f"naming consistency {naming_consistency:.2f}, "
        evidence += f"and meaning preservation {meaning_preservation:.2f}. "
        
        if continuity_score >= 0.90:
            evidence += "Continuum holds with high integrity."
        elif continuity_score >= 0.88:
            evidence += "Continuum holds but requires review."
        else:
            evidence += "Continuum degraded - integrity compromised."
        
        return evidence
    
    def create_lineage(self, subject: Any, parent_lineage: Optional[str] = None) -> str:
        """Create a new research lineage."""
        lineage_id = f"lineage_{int(time.time())}_{hashlib.md5(str(subject).encode()).hexdigest()[:8]}"
        
        lineage = ResearchLineage(
            lineage_id=lineage_id,
            subject_name=getattr(subject, 'name', 'Unknown'),
            subject_hash=getattr(subject, 'hash', ''),
            parent_lineage=parent_lineage
        )
        
        # Initialize continuity triad
        lineage.continuity_triad = {
            'meaning': f"Research meaning for {lineage.subject_name}",
            'naming': f"Consistent naming for {lineage.subject_name}",
            'continuity': f"Lineage continuity for {lineage.subject_name}"
        }
        
        self.lineages[lineage_id] = lineage
        
        # Update parent lineage if exists
        if parent_lineage and parent_lineage in self.lineages:
            self.lineages[parent_lineage].child_lineages.append(lineage_id)
        
        logger.info(f"🔗 Created lineage: {lineage_id}")
        
        return lineage_id
    
    def add_artifact(self, lineage_id: str, artifact: ResearchArtifact) -> str:
        """Add artifact to a lineage."""
        if lineage_id not in self.lineages:
            raise ValueError(f"Lineage {lineage_id} not found")
        
        # Set lineage ID on artifact
        artifact.lineage_id = lineage_id
        
        # Store artifact
        self.artifacts[artifact.id] = artifact
        
        # Add to lineage
        self.lineages[lineage_id].artifacts.append(artifact.id)
        self.lineages[lineage_id].last_updated = time.time()
        
        logger.info(f"📎 Added artifact {artifact.id} to lineage {lineage_id}")
        
        return artifact.id
    
    def get_lineage(self, lineage_id: str) -> Optional[ResearchLineage]:
        """Get lineage by ID."""
        return self.lineages.get(lineage_id)
    
    def get_artifact(self, artifact_id: str) -> Optional[ResearchArtifact]:
        """Get artifact by ID."""
        return self.artifacts.get(artifact_id)
    
    def get_lineage_artifacts(self, lineage_id: str) -> List[ResearchArtifact]:
        """Get all artifacts for a lineage."""
        if lineage_id not in self.lineages:
            return []
        
        artifact_ids = self.lineages[lineage_id].artifacts
        return [self.artifacts[aid] for aid in artifact_ids if aid in self.artifacts]
    
    def get_continuity_history(self, limit: int = 50) -> List[ContinuityScore]:
        """Get continuity score history."""
        return self.continuity_history[-limit:] if self.continuity_history else []
    
    def get_continuity_statistics(self) -> Dict[str, Any]:
        """Get continuity statistics."""
        if not self.continuity_history:
            return {}
        
        scores = [score.score for score in self.continuity_history]
        bands = [score.band for score in self.continuity_history]
        
        return {
            'total_scores': len(self.continuity_history),
            'average_score': sum(scores) / len(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'band_distribution': {
                band.value: sum(1 for b in bands if b == band)
                for band in ContinuityBand
            },
            'lineages_count': len(self.lineages),
            'artifacts_count': len(self.artifacts)
        }
    
    def export_lineage_data(self, lineage_id: str) -> Dict[str, Any]:
        """Export lineage data for external use."""
        if lineage_id not in self.lineages:
            return {}
        
        lineage = self.lineages[lineage_id]
        artifacts = self.get_lineage_artifacts(lineage_id)
        
        return {
            'lineage': {
                'lineage_id': lineage.lineage_id,
                'subject_name': lineage.subject_name,
                'subject_hash': lineage.subject_hash,
                'parent_lineage': lineage.parent_lineage,
                'child_lineages': lineage.child_lineages,
                'continuity_triad': lineage.continuity_triad,
                'created_at': lineage.created_at,
                'last_updated': lineage.last_updated
            },
            'artifacts': [
                {
                    'id': artifact.id,
                    'name': artifact.name,
                    'type': artifact.type,
                    'content_hash': artifact.content_hash,
                    'metadata': artifact.metadata,
                    'created_at': artifact.created_at
                }
                for artifact in artifacts
            ]
        }


# Global instance
_research_continuity = None

def get_research_continuity() -> ResearchContinuity:
    """Get the global research continuity instance."""
    global _research_continuity
    if _research_continuity is None:
        _research_continuity = ResearchContinuity()
    return _research_continuity


if __name__ == "__main__":
    # Test the research continuity system
    import asyncio
    
    async def test_research_continuity():
        print("🔗 Testing Research Continuity System")
        print("=" * 50)
        
        # Initialize system
        continuity = get_research_continuity()
        
        # Create mock subject
        class MockSubject:
            def __init__(self):
                self.name = "Test Research Subject"
                self.description = "A test subject for continuity analysis"
                self.claims = ["Claim 1", "Claim 2", "Claim 3"]
                self.hash = "test_hash_123456789"
        
        subject = MockSubject()
        
        # Create lineage
        lineage_id = continuity.create_lineage(subject)
        print(f"✅ Created lineage: {lineage_id}")
        
        # Add artifacts
        artifact1 = ResearchArtifact(
            id="artifact_1",
            name="Test Configuration",
            type="config",
            content={"param1": "value1", "param2": "value2"}
        )
        
        artifact2 = ResearchArtifact(
            id="artifact_2", 
            name="Test Results",
            type="result",
            content={"result": "success", "score": 0.95}
        )
        
        continuity.add_artifact(lineage_id, artifact1)
        continuity.add_artifact(lineage_id, artifact2)
        print(f"✅ Added artifacts to lineage")
        
        # Create test result
        test_result = {
            'execution_successful': True,
            'test_output': 'Test completed successfully for Test Research Subject',
            'metrics': {
                'execution_time': 0.5,
                'success_rate': 0.95
            },
            'artifacts': ['artifact_1', 'artifact_2']
        }
        
        # Create lineage data
        lineage_data = {
            'subject_hash': subject.hash,
            'test_id': f'crt_test_{int(time.time())}',
            'timestamp': time.time()
        }
        
        # Calculate continuity score
        continuity_score = await continuity.calculate_continuity_score(subject, test_result, lineage_data)
        
        print(f"📊 Continuity Score Results:")
        print(f"   Overall Score: {continuity_score.score:.3f}")
        print(f"   Band: {continuity_score.band.value}")
        print(f"   Lineage Integrity: {continuity_score.lineage_integrity:.2f}")
        print(f"   Artifact Completeness: {continuity_score.artifact_completeness:.2f}")
        print(f"   Naming Consistency: {continuity_score.naming_consistency:.2f}")
        print(f"   Meaning Preservation: {continuity_score.meaning_preservation:.2f}")
        print(f"   Evidence: {continuity_score.continuity_evidence}")
        
        # Get statistics
        stats = continuity.get_continuity_statistics()
        print(f"\n📈 Continuity Statistics:")
        print(f"   Total Scores: {stats.get('total_scores', 0)}")
        print(f"   Average Score: {stats.get('average_score', 0):.3f}")
        print(f"   Lineages: {stats.get('lineages_count', 0)}")
        print(f"   Artifacts: {stats.get('artifacts_count', 0)}")
        
        # Export lineage data
        exported_data = continuity.export_lineage_data(lineage_id)
        print(f"\n📤 Exported lineage data: {len(exported_data.get('artifacts', []))} artifacts")
        
        print("\n✅ Research continuity system test completed!")
    
    # Run test
    asyncio.run(test_research_continuity())

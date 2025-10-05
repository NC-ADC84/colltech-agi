#!/usr/bin/env python3
"""
CollTech-AGI Evidence Framework

Comprehensive evidence management system for research and testing.
Provides structured evidence collection, validation, and analysis
with integration to the consciousness system.
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


class EvidenceType(Enum):
    """Types of evidence."""
    TEST_EXECUTION = "test_execution"
    SUBJECT_ANALYSIS = "subject_analysis"
    REVERSIBILITY_VERIFICATION = "reversibility_verification"
    RESILIENCE_ASSESSMENT = "resilience_assessment"
    PRINCIPLE_FIT_EVALUATION = "principle_fit_evaluation"
    VALUE_TIME_ANALYSIS = "value_time_analysis"
    CONTINUITY_ANALYSIS = "continuity_analysis"
    LYRA_GRADING = "lyra_grading"
    PERFORMANCE_METRICS = "performance_metrics"
    SYSTEM_STATE = "system_state"
    CUSTOM = "custom"


class EvidenceQuality(Enum):
    """Evidence quality levels."""
    HIGH = "high"        # Reproducible, verifiable, complete
    MEDIUM = "medium"    # Partially verifiable, some gaps
    LOW = "low"          # Limited verifiability, significant gaps
    INSUFFICIENT = "insufficient"  # Cannot be verified


@dataclass
class Evidence:
    """Evidence item with metadata and validation."""
    id: str
    type: EvidenceType
    description: str
    data: Any
    quality: EvidenceQuality
    timestamp: float
    source: str
    validation_hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)  # IDs of dependent evidence
    
    def __post_init__(self):
        if not self.validation_hash:
            self.validation_hash = self._generate_validation_hash()
    
    def _generate_validation_hash(self) -> str:
        """Generate validation hash for evidence integrity."""
        content = f"{self.type.value}:{self.description}:{str(self.data)}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class EvidenceChain:
    """Chain of related evidence items."""
    id: str
    name: str
    description: str
    evidence_ids: List[str]
    chain_type: str  # "sequential", "parallel", "hierarchical"
    created_at: float
    last_updated: float
    integrity_score: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()
        if not self.last_updated:
            self.last_updated = time.time()


class EvidenceFramework:
    """
    Evidence Framework for Research and Testing
    
    Comprehensive evidence management system that provides structured
    evidence collection, validation, analysis, and chain management.
    """
    
    def __init__(self):
        self.evidence_items: Dict[str, Evidence] = {}
        self.evidence_chains: Dict[str, EvidenceChain] = {}
        self.evidence_history: List[str] = []  # Evidence IDs in chronological order
        
        logger.info("📋 Evidence Framework initialized")
    
    def add_evidence(self, evidence: Evidence) -> str:
        """Add evidence item to the framework."""
        self.evidence_items[evidence.id] = evidence
        self.evidence_history.append(evidence.id)
        
        logger.info(f"📋 Added evidence: {evidence.id} ({evidence.type.value})")
        
        return evidence.id
    
    def create_evidence(self, evidence_type: EvidenceType, description: str, data: Any,
                       quality: EvidenceQuality = EvidenceQuality.MEDIUM,
                       source: str = "system", metadata: Dict[str, Any] = None) -> Evidence:
        """Create a new evidence item."""
        evidence_id = f"evidence_{int(time.time())}_{hashlib.md5(description.encode()).hexdigest()[:8]}"
        
        evidence = Evidence(
            id=evidence_id,
            type=evidence_type,
            description=description,
            data=data,
            quality=quality,
            timestamp=time.time(),
            source=source,
            metadata=metadata or {}
        )
        
        return evidence
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self.evidence_items.get(evidence_id)
    
    def get_evidence_by_type(self, evidence_type: EvidenceType) -> List[Evidence]:
        """Get all evidence of a specific type."""
        return [evidence for evidence in self.evidence_items.values() 
                if evidence.type == evidence_type]
    
    def get_evidence_by_quality(self, quality: EvidenceQuality) -> List[Evidence]:
        """Get all evidence of a specific quality."""
        return [evidence for evidence in self.evidence_items.values() 
                if evidence.quality == quality]
    
    def validate_evidence(self, evidence_id: str) -> Dict[str, Any]:
        """Validate evidence integrity."""
        evidence = self.get_evidence(evidence_id)
        if not evidence:
            return {'valid': False, 'error': 'Evidence not found'}
        
        # Recalculate validation hash
        expected_hash = evidence._generate_validation_hash()
        is_valid = evidence.validation_hash == expected_hash
        
        # Check dependencies
        dependency_validation = {}
        for dep_id in evidence.dependencies:
            dep_evidence = self.get_evidence(dep_id)
            if dep_evidence:
                dep_validation = self.validate_evidence(dep_id)
                dependency_validation[dep_id] = dep_validation['valid']
            else:
                dependency_validation[dep_id] = False
        
        # Overall validation
        all_dependencies_valid = all(dependency_validation.values()) if dependency_validation else True
        overall_valid = is_valid and all_dependencies_valid
        
        return {
            'valid': overall_valid,
            'hash_valid': is_valid,
            'dependencies_valid': dependency_validation,
            'quality': evidence.quality.value,
            'timestamp': evidence.timestamp
        }
    
    def create_evidence_chain(self, name: str, description: str, evidence_ids: List[str],
                             chain_type: str = "sequential") -> str:
        """Create an evidence chain."""
        chain_id = f"chain_{int(time.time())}_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        # Validate all evidence IDs exist
        valid_evidence_ids = [eid for eid in evidence_ids if eid in self.evidence_items]
        
        chain = EvidenceChain(
            id=chain_id,
            name=name,
            description=description,
            evidence_ids=valid_evidence_ids,
            chain_type=chain_type
        )
        
        # Calculate integrity score
        chain.integrity_score = self._calculate_chain_integrity(chain)
        
        self.evidence_chains[chain_id] = chain
        
        logger.info(f"🔗 Created evidence chain: {chain_id} with {len(valid_evidence_ids)} evidence items")
        
        return chain_id
    
    def _calculate_chain_integrity(self, chain: EvidenceChain) -> float:
        """Calculate integrity score for an evidence chain."""
        if not chain.evidence_ids:
            return 0.0
        
        # Validate all evidence in chain
        valid_count = 0
        quality_scores = []
        
        for evidence_id in chain.evidence_ids:
            evidence = self.get_evidence(evidence_id)
            if evidence:
                validation = self.validate_evidence(evidence_id)
                if validation['valid']:
                    valid_count += 1
                
                # Quality score mapping
                quality_score = {
                    EvidenceQuality.HIGH: 1.0,
                    EvidenceQuality.MEDIUM: 0.7,
                    EvidenceQuality.LOW: 0.4,
                    EvidenceQuality.INSUFFICIENT: 0.1
                }.get(evidence.quality, 0.0)
                
                quality_scores.append(quality_score)
        
        # Calculate integrity score
        validity_ratio = valid_count / len(chain.evidence_ids)
        average_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        integrity_score = (validity_ratio * 0.6 + average_quality * 0.4)
        
        return min(integrity_score, 1.0)
    
    def get_evidence_chain(self, chain_id: str) -> Optional[EvidenceChain]:
        """Get evidence chain by ID."""
        return self.evidence_chains.get(chain_id)
    
    def get_chain_evidence(self, chain_id: str) -> List[Evidence]:
        """Get all evidence items in a chain."""
        chain = self.get_evidence_chain(chain_id)
        if not chain:
            return []
        
        return [self.get_evidence(eid) for eid in chain.evidence_ids if self.get_evidence(eid)]
    
    def analyze_evidence_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in evidence collection."""
        if not self.evidence_items:
            return {}
        
        # Type distribution
        type_distribution = {}
        for evidence in self.evidence_items.values():
            type_name = evidence.type.value
            type_distribution[type_name] = type_distribution.get(type_name, 0) + 1
        
        # Quality distribution
        quality_distribution = {}
        for evidence in self.evidence_items.values():
            quality_name = evidence.quality.value
            quality_distribution[quality_name] = quality_distribution.get(quality_name, 0) + 1
        
        # Source distribution
        source_distribution = {}
        for evidence in self.evidence_items.values():
            source = evidence.source
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        # Temporal analysis
        timestamps = [evidence.timestamp for evidence in self.evidence_items.values()]
        if timestamps:
            time_span = max(timestamps) - min(timestamps)
            evidence_rate = len(timestamps) / time_span if time_span > 0 else 0
        else:
            time_span = 0
            evidence_rate = 0
        
        # Chain analysis
        chain_integrity_scores = [chain.integrity_score for chain in self.evidence_chains.values()]
        average_chain_integrity = sum(chain_integrity_scores) / len(chain_integrity_scores) if chain_integrity_scores else 0.0
        
        return {
            'total_evidence': len(self.evidence_items),
            'total_chains': len(self.evidence_chains),
            'type_distribution': type_distribution,
            'quality_distribution': quality_distribution,
            'source_distribution': source_distribution,
            'temporal_analysis': {
                'time_span_seconds': time_span,
                'evidence_rate_per_second': evidence_rate,
                'earliest_evidence': min(timestamps) if timestamps else 0,
                'latest_evidence': max(timestamps) if timestamps else 0
            },
            'chain_analysis': {
                'average_integrity': average_chain_integrity,
                'high_integrity_chains': sum(1 for score in chain_integrity_scores if score >= 0.8),
                'low_integrity_chains': sum(1 for score in chain_integrity_scores if score < 0.5)
            }
        }
    
    def export_evidence(self, evidence_ids: List[str] = None) -> Dict[str, Any]:
        """Export evidence data."""
        if evidence_ids is None:
            evidence_ids = list(self.evidence_items.keys())
        
        exported_evidence = []
        for evidence_id in evidence_ids:
            evidence = self.get_evidence(evidence_id)
            if evidence:
                exported_evidence.append({
                    'id': evidence.id,
                    'type': evidence.type.value,
                    'description': evidence.description,
                    'data': evidence.data,
                    'quality': evidence.quality.value,
                    'timestamp': evidence.timestamp,
                    'source': evidence.source,
                    'validation_hash': evidence.validation_hash,
                    'metadata': evidence.metadata,
                    'dependencies': evidence.dependencies
                })
        
        return {
            'export_timestamp': time.time(),
            'evidence_count': len(exported_evidence),
            'evidence_items': exported_evidence
        }
    
    def import_evidence(self, evidence_data: Dict[str, Any]) -> List[str]:
        """Import evidence data."""
        imported_ids = []
        
        for evidence_item in evidence_data.get('evidence_items', []):
            try:
                evidence = Evidence(
                    id=evidence_item['id'],
                    type=EvidenceType(evidence_item['type']),
                    description=evidence_item['description'],
                    data=evidence_item['data'],
                    quality=EvidenceQuality(evidence_item['quality']),
                    timestamp=evidence_item['timestamp'],
                    source=evidence_item['source'],
                    validation_hash=evidence_item['validation_hash'],
                    metadata=evidence_item.get('metadata', {}),
                    dependencies=evidence_item.get('dependencies', [])
                )
                
                self.add_evidence(evidence)
                imported_ids.append(evidence.id)
                
            except Exception as e:
                logger.warning(f"Failed to import evidence {evidence_item.get('id', 'unknown')}: {e}")
        
        logger.info(f"📥 Imported {len(imported_ids)} evidence items")
        
        return imported_ids
    
    def get_evidence_statistics(self) -> Dict[str, Any]:
        """Get comprehensive evidence statistics."""
        if not self.evidence_items:
            return {'total_evidence': 0}
        
        # Basic counts
        total_evidence = len(self.evidence_items)
        total_chains = len(self.evidence_chains)
        
        # Quality breakdown
        quality_counts = {}
        for evidence in self.evidence_items.values():
            quality = evidence.quality.value
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        # Type breakdown
        type_counts = {}
        for evidence in self.evidence_items.values():
            evidence_type = evidence.type.value
            type_counts[evidence_type] = type_counts.get(evidence_type, 0) + 1
        
        # Validation status
        valid_count = 0
        for evidence_id in self.evidence_items.keys():
            validation = self.validate_evidence(evidence_id)
            if validation['valid']:
                valid_count += 1
        
        # Chain integrity
        chain_integrity_scores = [chain.integrity_score for chain in self.evidence_chains.values()]
        avg_chain_integrity = sum(chain_integrity_scores) / len(chain_integrity_scores) if chain_integrity_scores else 0.0
        
        return {
            'total_evidence': total_evidence,
            'total_chains': total_chains,
            'valid_evidence': valid_count,
            'validation_rate': valid_count / total_evidence if total_evidence > 0 else 0.0,
            'quality_distribution': quality_counts,
            'type_distribution': type_counts,
            'average_chain_integrity': avg_chain_integrity,
            'high_quality_evidence': quality_counts.get('high', 0),
            'medium_quality_evidence': quality_counts.get('medium', 0),
            'low_quality_evidence': quality_counts.get('low', 0),
            'insufficient_evidence': quality_counts.get('insufficient', 0)
        }


# Global instance
_evidence_framework = None

def get_evidence_framework() -> EvidenceFramework:
    """Get the global evidence framework instance."""
    global _evidence_framework
    if _evidence_framework is None:
        _evidence_framework = EvidenceFramework()
    return _evidence_framework


if __name__ == "__main__":
    # Test the evidence framework
    def test_evidence_framework():
        print("📋 Testing Evidence Framework")
        print("=" * 50)
        
        # Initialize framework
        framework = get_evidence_framework()
        
        # Create evidence items
        evidence1 = framework.create_evidence(
            EvidenceType.TEST_EXECUTION,
            "Test execution for sample subject",
            {"success": True, "duration": 0.5, "output": "Test passed"},
            EvidenceQuality.HIGH,
            "test_system"
        )
        
        evidence2 = framework.create_evidence(
            EvidenceType.SUBJECT_ANALYSIS,
            "Subject analysis for sample subject",
            {"name": "Sample Subject", "claims": ["Claim 1", "Claim 2"]},
            EvidenceQuality.MEDIUM,
            "analysis_system"
        )
        
        evidence3 = framework.create_evidence(
            EvidenceType.PERFORMANCE_METRICS,
            "Performance metrics for sample subject",
            {"cpu_usage": 0.75, "memory_usage": 0.60, "throughput": 1000},
            EvidenceQuality.HIGH,
            "monitoring_system"
        )
        
        # Add evidence to framework
        framework.add_evidence(evidence1)
        framework.add_evidence(evidence2)
        framework.add_evidence(evidence3)
        
        print(f"✅ Created and added {len([evidence1, evidence2, evidence3])} evidence items")
        
        # Create evidence chain
        chain_id = framework.create_evidence_chain(
            "Sample Test Chain",
            "Complete test execution chain",
            [evidence1.id, evidence2.id, evidence3.id],
            "sequential"
        )
        
        print(f"✅ Created evidence chain: {chain_id}")
        
        # Validate evidence
        validation1 = framework.validate_evidence(evidence1.id)
        validation2 = framework.validate_evidence(evidence2.id)
        
        print(f"📊 Evidence Validation:")
        print(f"   Evidence 1: {'✅ Valid' if validation1['valid'] else '❌ Invalid'}")
        print(f"   Evidence 2: {'✅ Valid' if validation2['valid'] else '❌ Invalid'}")
        
        # Get statistics
        stats = framework.get_evidence_statistics()
        print(f"\n📈 Evidence Statistics:")
        print(f"   Total Evidence: {stats['total_evidence']}")
        print(f"   Total Chains: {stats['total_chains']}")
        print(f"   Valid Evidence: {stats['valid_evidence']}")
        print(f"   Validation Rate: {stats['validation_rate']:.2%}")
        print(f"   High Quality: {stats['high_quality_evidence']}")
        print(f"   Medium Quality: {stats['medium_quality_evidence']}")
        print(f"   Average Chain Integrity: {stats['average_chain_integrity']:.2f}")
        
        # Analyze patterns
        patterns = framework.analyze_evidence_patterns()
        print(f"\n🔍 Evidence Patterns:")
        print(f"   Type Distribution: {patterns.get('type_distribution', {})}")
        print(f"   Quality Distribution: {patterns.get('quality_distribution', {})}")
        print(f"   Evidence Rate: {patterns.get('temporal_analysis', {}).get('evidence_rate_per_second', 0):.2f}/sec")
        
        # Export evidence
        exported = framework.export_evidence([evidence1.id, evidence2.id])
        print(f"\n📤 Exported {exported['evidence_count']} evidence items")
        
        print("\n✅ Evidence framework test completed!")
    
    # Run test
    test_evidence_framework()

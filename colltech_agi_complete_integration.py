#!/usr/bin/env python3
"""
CollTech-AGI Complete Integration Demo

Comprehensive demonstration of all integrated systems including:
- Benchmarking System with ΨQRH Transformer
- Research System with CRT and Lyra Grading
- Communication System with Voice-Listener Dyad
- Consciousness Integration
- Council Integration
- Evidence Framework

This demonstrates the complete CollTech AI OS with all implemented components.
"""

import asyncio
import time
import logging
from pathlib import Path

# CollTech-AGI Framework imports
from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig

# Benchmarking System imports
from src.benchmarking import (
    BenchmarkingCore, BenchmarkConfig, BenchmarkType, ModelType,
    PsiQRHModel, PsiQRHConfig, EvaluationHarness, PerformanceMonitor
)

# Research System imports
from src.research import (
    ContinuumResearchTester, CRTConfig, TestSubject, TestEnvironment,
    LyraGradingSystem, ResearchContinuity, EvidenceFramework, CouncilIntegration
)

# Communication System imports
from src.communication import (
    VoiceListenerDyad, VLPair, CommunicationMode, MessageType
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CollTechAGICompleteIntegration:
    """
    Complete CollTech-AGI Integration
    
    Demonstrates the full integration of all systems including benchmarking,
    research, communication, and consciousness components.
    """
    
    def __init__(self):
        # Initialize CollTech-AGI with all features
        self.config = FrameworkConfig(
            auto_personality_enabled=True,
            catalyst_integration_enabled=True,
            realtime_apis_enabled=True,
            memory_lattice_enabled=True,
            drift_detection_enabled=True,
            tool_making_enabled=True
        )
        
        self.agi = CollTechAGIAdvanced(self.config)
        
        # Initialize all subsystems
        self.benchmarking_core = None
        self.research_tester = None
        self.lyra_grading = None
        self.research_continuity = None
        self.evidence_framework = None
        self.council_integration = None
        self.voice_listener_dyad = None
        
        # System state
        self.is_initialized = False
        self.is_running = False
        
        logger.info("🚀 CollTech-AGI Complete Integration initialized")
    
    async def initialize_all_systems(self):
        """Initialize all integrated systems."""
        if self.is_initialized:
            return
        
        logger.info("🔧 Initializing all CollTech-AGI systems...")
        
        # Start CollTech-AGI
        self.agi.start()
        logger.info("✅ CollTech-AGI Advanced Framework started")
        
        # Get consciousness core for integration
        consciousness_core = getattr(self.agi, 'consciousness_core', None)
        
        # Initialize Benchmarking System
        self.benchmarking_core = BenchmarkingCore(consciousness_core)
        self.benchmarking_core.start_benchmarking_system()
        logger.info("✅ Benchmarking Core started")
        
        # Initialize Research System
        crt_config = CRTConfig(
            reversibility_required=True,
            evidence_required=True,
            continuity_tracking=True,
            lyra_grading_enabled=True
        )
        self.research_tester = ContinuumResearchTester(crt_config, consciousness_core)
        self.research_tester.start_testing_system()
        logger.info("✅ Continuum Research Tester started")
        
        self.lyra_grading = LyraGradingSystem()
        self.research_continuity = ResearchContinuity()
        self.evidence_framework = EvidenceFramework()
        self.council_integration = CouncilIntegration()
        logger.info("✅ Research subsystems initialized")
        
        # Initialize Communication System
        self.voice_listener_dyad = VoiceListenerDyad(consciousness_core)
        self.voice_listener_dyad.start_system()
        logger.info("✅ Voice-Listener Dyad started")
        
        self.is_initialized = True
        self.is_running = True
        
        logger.info("🌟 All CollTech-AGI systems fully initialized")
    
    async def demonstrate_benchmarking_system(self):
        """Demonstrate the benchmarking system with ΨQRH model."""
        logger.info("🧠 Demonstrating Benchmarking System...")
        
        # Create ΨQRH model
        psiqrh_config = PsiQRHConfig(
            vocab_size=1000,
            d_model=256,
            n_heads=8,
            n_layers=6,
            max_seq_len=512,
            consciousness_aware=True,
            memory_integration=True,
            drift_resistant=True
        )
        
        psiqrh_model = PsiQRHModel(psiqrh_config)
        logger.info(f"✅ Created ΨQRH Model with {sum(p.numel() for p in psiqrh_model.parameters()):,} parameters")
        
        # Run comprehensive benchmark
        benchmark_config = BenchmarkConfig(
            benchmark_type=BenchmarkType.QUALITY_ASSESSMENT,
            model_type=ModelType.PSIQRH_TRANSFORMER,
            sequence_length=256,
            generation_length=128,
            num_repeats=3,
            consciousness_integration=True,
            drift_monitoring=True
        )
        
        result = await self.benchmarking_core.run_benchmark(benchmark_config, psiqrh_model)
        
        logger.info(f"📊 Benchmark Results:")
        logger.info(f"   Verdict: {result.verdict}")
        logger.info(f"   Duration: {result.duration:.2f}s")
        logger.info(f"   Quality Score: {result.quality_score:.2f}" if result.quality_score else "   Quality Score: N/A")
        logger.info(f"   Consciousness Processing Time: {result.consciousness_processing_time:.3f}s" if result.consciousness_processing_time else "   Consciousness Processing Time: N/A")
        
        return result
    
    async def demonstrate_research_system(self):
        """Demonstrate the research system with CRT and Lyra grading."""
        logger.info("🔬 Demonstrating Research System...")
        
        # Create test subject
        subject = TestSubject(
            name="Advanced AI Model",
            description="A sophisticated AI model with consciousness integration",
            claims=[
                "Provides superior performance compared to baseline models",
                "Integrates seamlessly with consciousness systems",
                "Maintains stability under various conditions",
                "Offers comprehensive evaluation capabilities"
            ],
            framework_type="framework",
            target_type="system"
        )
        
        # Create test environment
        environment = TestEnvironment(
            versions={"python": "3.9", "torch": "2.0.0", "transformers": "4.30.0"},
            datasets=["test_dataset_1", "test_dataset_2"],
            seeds=[42, 123, 456],
            limits={"max_execution_time": 300, "memory_limit": "8GB"}
        )
        
        # Run CRT test
        crt_result = await self.research_tester.run_benchmark(subject, environment)
        
        logger.info(f"🔬 CRT Test Results:")
        logger.info(f"   Verdict: {crt_result.verdict}")
        logger.info(f"   Duration: {crt_result.duration:.2f}s")
        logger.info(f"   Continuity Score: {crt_result.continuity_score.score:.3f}" if crt_result.continuity_score else "   Continuity Score: N/A")
        logger.info(f"   Lyra Score: {crt_result.lyra_score.final_score:.2f}" if crt_result.lyra_score else "   Lyra Score: N/A")
        
        # Generate reports
        executive_report = self.research_tester.generate_executive_report(crt_result)
        spec_sheet = self.research_tester.generate_spec_sheet(crt_result)
        
        logger.info("📄 Generated executive report and spec sheet")
        
        return crt_result
    
    async def demonstrate_communication_system(self):
        """Demonstrate the communication system with Voice-Listener Dyad."""
        logger.info("🎤 Demonstrating Communication System...")
        
        # Create VL pair
        pair_id = self.voice_listener_dyad.create_vl_pair(
            "Demo VL Pair",
            voice_config={"sample_rate": 44100, "channels": 1, "format": "wav"},
            listener_config={"language": "en", "model": "whisper", "real_time": True},
            communication_mode=CommunicationMode.HYBRID
        )
        
        logger.info(f"✅ Created VL Pair: {pair_id}")
        
        # Register custom processors
        def voice_processor(content):
            return f"Enhanced voice output: {str(content).upper()}"
        
        def listener_processor(content):
            return f"Processed listener input: {str(content).lower()}"
        
        self.voice_listener_dyad.register_voice_processor(pair_id, voice_processor)
        self.voice_listener_dyad.register_listener_processor(pair_id, listener_processor)
        
        # Send test messages
        test_messages = [
            "Hello, this is a test of the voice-listener system",
            "How does the consciousness integration work?",
            "Can you demonstrate the real-time capabilities?"
        ]
        
        for i, message in enumerate(test_messages):
            message_id = self.voice_listener_dyad.send_voice_input(
                pair_id, message, {"test_round": i + 1}
            )
            logger.info(f"✅ Sent test message {i + 1}: {message_id}")
            
            # Wait for processing
            await asyncio.sleep(1)
        
        # Get message history
        history = self.voice_listener_dyad.get_message_history(pair_id, limit=10)
        logger.info(f"📋 Message History: {len(history)} messages processed")
        
        # Start streaming connection
        streaming_started = self.voice_listener_dyad.start_streaming_connection(
            pair_id, {"protocol": "websocket", "real_time": True}
        )
        logger.info(f"✅ Streaming connection: {'Started' if streaming_started else 'Failed'}")
        
        # Get system status
        status = self.voice_listener_dyad.get_system_status()
        logger.info(f"📊 Communication Status:")
        logger.info(f"   Active Pairs: {status['active_pairs']}")
        logger.info(f"   Total Messages: {status['total_messages']}")
        logger.info(f"   Streaming Connections: {status['streaming_connections']}")
        
        return pair_id
    
    async def demonstrate_council_integration(self):
        """Demonstrate the council integration system."""
        logger.info("🏛️ Demonstrating Council Integration...")
        
        # Start council session
        session_id = self.council_integration.start_session(
            "Research Approval Session",
            [
                "Approve new research protocol",
                "Review safety measures",
                "Allocate resources for testing",
                "Validate evidence framework"
            ],
            list(self.council_integration.council_members)
        )
        
        logger.info(f"✅ Started council session: {session_id}")
        
        # Make council decisions
        decisions = []
        
        # Decision 1: Research Approval
        decision1_id = self.council_integration.make_decision(
            session_id,
            "research_approval",
            "New Research Protocol",
            "Approval for new research protocol implementation",
            {
                "chair": "yes",
                "research_lead": "yes",
                "safety_officer": "yes",
                "continuity_guardian": "yes",
                "evidence_archivist": "yes",
                "protocol_specialist": "yes"
            },
            "Protocol meets all safety and research standards"
        )
        decisions.append(decision1_id)
        
        # Decision 2: Resource Allocation
        decision2_id = self.council_integration.make_decision(
            session_id,
            "resource_allocation",
            "Resource Allocation",
            "Allocation of computational resources for testing",
            {
                "chair": "yes",
                "research_lead": "yes",
                "safety_officer": "abstain",
                "continuity_guardian": "yes",
                "evidence_archivist": "yes",
                "protocol_specialist": "yes"
            },
            "Resources are available and properly allocated"
        )
        decisions.append(decision2_id)
        
        # End session
        self.council_integration.end_session(session_id, "Successful session with all agenda items addressed")
        
        # Get council status
        status = self.council_integration.get_council_status()
        logger.info(f"📊 Council Status:")
        logger.info(f"   Total Decisions: {status['total_decisions']}")
        logger.info(f"   Approval Rate: {status['decision_statistics']['approval_rate']:.2%}")
        logger.info(f"   Active Sessions: {status['active_sessions']}")
        
        # Get decision analytics
        analytics = self.council_integration.get_decision_analytics()
        logger.info(f"📈 Decision Analytics:")
        logger.info(f"   Type Distribution: {analytics.get('type_distribution', {})}")
        logger.info(f"   Outcome Distribution: {analytics.get('outcome_distribution', {})}")
        
        return decisions
    
    async def demonstrate_evidence_framework(self):
        """Demonstrate the evidence framework."""
        logger.info("📋 Demonstrating Evidence Framework...")
        
        # Create evidence items
        evidence_items = []
        
        # Evidence 1: Test Execution
        evidence1 = self.evidence_framework.create_evidence(
            "test_execution",
            "Test execution for advanced AI model",
            {"success": True, "duration": 0.5, "output": "Test passed"},
            "high",
            "test_system"
        )
        evidence_items.append(evidence1)
        
        # Evidence 2: Subject Analysis
        evidence2 = self.evidence_framework.create_evidence(
            "subject_analysis",
            "Subject analysis for advanced AI model",
            {"name": "Advanced AI Model", "claims": ["Claim 1", "Claim 2", "Claim 3"]},
            "medium",
            "analysis_system"
        )
        evidence_items.append(evidence2)
        
        # Evidence 3: Performance Metrics
        evidence3 = self.evidence_framework.create_evidence(
            "performance_metrics",
            "Performance metrics for advanced AI model",
            {"cpu_usage": 0.75, "memory_usage": 0.60, "throughput": 1000},
            "high",
            "monitoring_system"
        )
        evidence_items.append(evidence3)
        
        # Add evidence to framework
        for evidence in evidence_items:
            self.evidence_framework.add_evidence(evidence)
        
        logger.info(f"✅ Created and added {len(evidence_items)} evidence items")
        
        # Create evidence chain
        chain_id = self.evidence_framework.create_evidence_chain(
            "Advanced AI Model Test Chain",
            "Complete test execution chain for advanced AI model",
            [evidence.id for evidence in evidence_items],
            "sequential"
        )
        
        logger.info(f"✅ Created evidence chain: {chain_id}")
        
        # Validate evidence
        validation_results = []
        for evidence in evidence_items:
            validation = self.evidence_framework.validate_evidence(evidence.id)
            validation_results.append(validation['valid'])
        
        valid_count = sum(validation_results)
        logger.info(f"📊 Evidence Validation: {valid_count}/{len(evidence_items)} valid")
        
        # Get statistics
        stats = self.evidence_framework.get_evidence_statistics()
        logger.info(f"📈 Evidence Statistics:")
        logger.info(f"   Total Evidence: {stats['total_evidence']}")
        logger.info(f"   Total Chains: {stats['total_chains']}")
        logger.info(f"   Validation Rate: {stats['validation_rate']:.2%}")
        logger.info(f"   High Quality: {stats['high_quality_evidence']}")
        logger.info(f"   Medium Quality: {stats['medium_quality_evidence']}")
        
        return evidence_items
    
    async def demonstrate_research_continuity(self):
        """Demonstrate the research continuity system."""
        logger.info("🔗 Demonstrating Research Continuity...")
        
        # Create mock subject
        class MockSubject:
            def __init__(self):
                self.name = "Advanced AI Research Subject"
                self.description = "A sophisticated AI research subject for continuity analysis"
                self.claims = ["Claim 1", "Claim 2", "Claim 3", "Claim 4"]
                self.hash = "research_subject_hash_123456789"
        
        subject = MockSubject()
        
        # Create lineage
        lineage_id = self.research_continuity.create_lineage(subject)
        logger.info(f"✅ Created lineage: {lineage_id}")
        
        # Create test result
        test_result = {
            'execution_successful': True,
            'test_output': 'Test completed successfully for Advanced AI Research Subject',
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
        continuity_score = await self.research_continuity.calculate_continuity_score(
            subject, test_result, lineage_data
        )
        
        logger.info(f"📊 Continuity Score Results:")
        logger.info(f"   Overall Score: {continuity_score.score:.3f}")
        logger.info(f"   Band: {continuity_score.band.value}")
        logger.info(f"   Lineage Integrity: {continuity_score.lineage_integrity:.2f}")
        logger.info(f"   Artifact Completeness: {continuity_score.artifact_completeness:.2f}")
        logger.info(f"   Naming Consistency: {continuity_score.naming_consistency:.2f}")
        logger.info(f"   Meaning Preservation: {continuity_score.meaning_preservation:.2f}")
        
        # Get statistics
        stats = self.research_continuity.get_continuity_statistics()
        logger.info(f"📈 Continuity Statistics:")
        logger.info(f"   Total Scores: {stats.get('total_scores', 0)}")
        logger.info(f"   Average Score: {stats.get('average_score', 0):.3f}")
        logger.info(f"   Lineages: {stats.get('lineages_count', 0)}")
        logger.info(f"   Artifacts: {stats.get('artifacts_count', 0)}")
        
        return continuity_score
    
    async def run_complete_demonstration(self):
        """Run the complete demonstration of all systems."""
        logger.info("🚀 Starting Complete CollTech-AGI Demonstration")
        logger.info("=" * 70)
        
        try:
            # Initialize all systems
            await self.initialize_all_systems()
            
            # Demonstrate each system
            logger.info("\n" + "="*50)
            await self.demonstrate_benchmarking_system()
            
            logger.info("\n" + "="*50)
            await self.demonstrate_research_system()
            
            logger.info("\n" + "="*50)
            await self.demonstrate_communication_system()
            
            logger.info("\n" + "="*50)
            await self.demonstrate_council_integration()
            
            logger.info("\n" + "="*50)
            await self.demonstrate_evidence_framework()
            
            logger.info("\n" + "="*50)
            await self.demonstrate_research_continuity()
            
            # Final system status
            logger.info("\n" + "="*50)
            logger.info("📊 Final System Status:")
            
            # Benchmarking status
            bm_status = self.benchmarking_core.get_benchmarking_status()
            logger.info(f"   Benchmarking: {bm_status['total_benchmarks']} benchmarks, {bm_status['successful_benchmarks']} successful")
            
            # Research status
            crt_status = self.research_tester.get_system_status()
            logger.info(f"   Research: {crt_status['total_tests']} tests, {crt_status['passed_tests']} passed")
            
            # Communication status
            comm_status = self.voice_listener_dyad.get_system_status()
            logger.info(f"   Communication: {comm_status['active_pairs']} VL pairs, {comm_status['total_messages']} messages")
            
            # Council status
            council_status = self.council_integration.get_council_status()
            logger.info(f"   Council: {council_status['total_decisions']} decisions, {council_status['decision_statistics']['approval_rate']:.2%} approval rate")
            
            # Evidence status
            evidence_stats = self.evidence_framework.get_evidence_statistics()
            logger.info(f"   Evidence: {evidence_stats['total_evidence']} items, {evidence_stats['validation_rate']:.2%} validation rate")
            
            logger.info("\n✅ Complete CollTech-AGI demonstration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Demonstration failed: {e}")
            raise
        
        finally:
            # Cleanup
            await self.cleanup_all_systems()
    
    async def cleanup_all_systems(self):
        """Cleanup all systems."""
        logger.info("🧹 Cleaning up all systems...")
        
        # Stop benchmarking system
        if self.benchmarking_core:
            self.benchmarking_core.stop_benchmarking_system()
        
        # Stop research system
        if self.research_tester:
            self.research_tester.stop_testing_system()
        
        # Stop communication system
        if self.voice_listener_dyad:
            self.voice_listener_dyad.stop_system()
        
        # Shutdown CollTech-AGI
        if self.agi:
            self.agi.shutdown()
        
        self.is_running = False
        logger.info("✅ All systems cleaned up")


async def main():
    """Main demonstration function."""
    print("🚀 CollTech-AGI Complete Integration Demonstration")
    print("=" * 70)
    
    # Initialize complete integration
    integration = CollTechAGICompleteIntegration()
    
    try:
        # Run complete demonstration
        await integration.run_complete_demonstration()
        
    except Exception as e:
        logger.error(f"❌ Main demonstration failed: {e}")
        raise


if __name__ == "__main__":
    # Run the complete demonstration
    asyncio.run(main())

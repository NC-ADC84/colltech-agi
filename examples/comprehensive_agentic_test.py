#!/usr/bin/env python3
"""
Comprehensive test suite for Agentic Mindsets integration
Tests all 5 modes, edge cases, and advanced features
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../AgenticMindsets'))

from agentic_mindsets import (
    ZenoTrapRecursivePrompter,
    EgoTranscendenceScaffold,
    AdaptiveMetaPrompter,
    VEFHierarchicalSystem,
    ConsciousnessFirstFramework,
    AgenticMindsetOrchestrator
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.agentic_mindsets_integration import (
    AgenticMindsetsIntegration,
    AgenticConfig,
    AgenticMode
)


class ComprehensiveAgenticTester:
    """Comprehensive test suite for all agentic systems"""
    
    def __init__(self):
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.agentic = AgenticMindsetsIntegration()
    
    def log_test(self, test_name, passed, error=None):
        """Log test result"""
        if passed:
            self.test_results['passed'] += 1
            print(f"  ✅ {test_name}")
        else:
            self.test_results['failed'] += 1
            print(f"  ❌ {test_name}")
            if error:
                self.test_results['errors'].append(f"{test_name}: {error}")
                print(f"     Error: {error}")
    
    def test_mode_stable(self):
        """Test STABLE mode (Zeno Trap)"""
        print("\n--- Testing STABLE Mode (Zeno Trap) ---")
        
        try:
            result = self.agentic.process_with_agentic_mindset(
                "Solve this problem systematically",
                mode=AgenticMode.STABLE
            )
            
            # Check basic structure
            self.log_test("STABLE: Basic processing", 
                         'processed_prompt' in result and 'agentic_metadata' in result)
            
            # Check Zeno Trap metadata
            has_zeno = 'zeno_trap' in result['agentic_metadata']
            self.log_test("STABLE: Zeno Trap metadata present", has_zeno)
            
            if has_zeno:
                zeno = result['agentic_metadata']['zeno_trap']
                self.log_test("STABLE: Progress tracking", 'progress' in zeno)
                self.log_test("STABLE: Coherence tracking", 'coherence' in zeno)
                self.log_test("STABLE: Iteration count", 'iteration' in zeno)
            
        except Exception as e:
            self.log_test("STABLE: Mode execution", False, str(e))
    
    def test_mode_transcendent(self):
        """Test TRANSCENDENT mode (Ego-Transcendence)"""
        print("\n--- Testing TRANSCENDENT Mode (Ego-Transcendence) ---")
        
        try:
            result = self.agentic.process_with_agentic_mindset(
                "I need a breakthrough in my thinking",
                mode=AgenticMode.TRANSCENDENT
            )
            
            self.log_test("TRANSCENDENT: Basic processing", 
                         'processed_prompt' in result)
            
            # Check ego-transcendence metadata
            has_ego = 'ego_transcendence' in result['agentic_metadata']
            self.log_test("TRANSCENDENT: Ego-Transcendence metadata present", has_ego)
            
            if has_ego:
                ego = result['agentic_metadata']['ego_transcendence']
                self.log_test("TRANSCENDENT: Trigger evaluation", 'should_trigger' in ego)
                self.log_test("TRANSCENDENT: Trigger type", 'trigger_type' in ego)
                self.log_test("TRANSCENDENT: Urgency level", 'urgency' in ego)
            
        except Exception as e:
            self.log_test("TRANSCENDENT: Mode execution", False, str(e))
    
    def test_mode_evolutionary(self):
        """Test EVOLUTIONARY mode (Adaptive Meta)"""
        print("\n--- Testing EVOLUTIONARY Mode (Adaptive Meta) ---")
        
        try:
            result = self.agentic.process_with_agentic_mindset(
                "Optimize this approach",
                mode=AgenticMode.EVOLUTIONARY
            )
            
            self.log_test("EVOLUTIONARY: Basic processing", 
                         'processed_prompt' in result)
            
            # Check adaptive meta metadata
            has_meta = 'adaptive_meta' in result['agentic_metadata']
            self.log_test("EVOLUTIONARY: Adaptive Meta metadata present", has_meta)
            
            if has_meta:
                meta = result['agentic_metadata']['adaptive_meta']
                self.log_test("EVOLUTIONARY: Population info", 'population_size' in meta)
                self.log_test("EVOLUTIONARY: Generation tracking", 'generation' in meta)
            
        except Exception as e:
            self.log_test("EVOLUTIONARY: Mode execution", False, str(e))
    
    def test_mode_hierarchical(self):
        """Test HIERARCHICAL mode (VEF Multi-scale)"""
        print("\n--- Testing HIERARCHICAL Mode (VEF Multi-scale) ---")
        
        try:
            result = self.agentic.process_with_agentic_mindset(
                "Coordinate across multiple scales",
                mode=AgenticMode.HIERARCHICAL
            )
            
            self.log_test("HIERARCHICAL: Basic processing", 
                         'processed_prompt' in result)
            
            # Check hierarchical metadata
            has_hier = 'hierarchical_vef' in result['agentic_metadata']
            self.log_test("HIERARCHICAL: VEF metadata present", has_hier)
            
            if has_hier:
                hier = result['agentic_metadata']['hierarchical_vef']
                self.log_test("HIERARCHICAL: System complexity", 'system_complexity' in hier)
                self.log_test("HIERARCHICAL: Paradigm coherence", 'paradigm_coherence' in hier)
            
        except Exception as e:
            self.log_test("HIERARCHICAL: Mode execution", False, str(e))
    
    def test_mode_conscious(self):
        """Test CONSCIOUS mode (Consciousness-First)"""
        print("\n--- Testing CONSCIOUS Mode (Consciousness-First) ---")
        
        try:
            result = self.agentic.process_with_agentic_mindset(
                "What is the meaning of existence?",
                mode=AgenticMode.CONSCIOUS
            )
            
            self.log_test("CONSCIOUS: Basic processing", 
                         'processed_prompt' in result)
            
            # Check consciousness metadata
            has_consciousness = 'consciousness' in result['agentic_metadata']
            self.log_test("CONSCIOUS: Consciousness metadata present", has_consciousness)
            
            if has_consciousness:
                consciousness = result['agentic_metadata']['consciousness']
                self.log_test("CONSCIOUS: Meaning score", 'meaning_score' in consciousness)
                self.log_test("CONSCIOUS: Existential relevance", 'existential_relevance' in consciousness)
                self.log_test("CONSCIOUS: Narrative chapter", 'narrative_chapter' in consciousness)
                self.log_test("CONSCIOUS: Transcendence evaluation", 'should_transcend' in consciousness)
            
        except Exception as e:
            self.log_test("CONSCIOUS: Mode execution", False, str(e))
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n--- Testing Edge Cases ---")
        
        # Empty input
        try:
            result = self.agentic.process_with_agentic_mindset("")
            self.log_test("Edge: Empty input handling", 'processed_prompt' in result)
        except Exception as e:
            self.log_test("Edge: Empty input handling", False, str(e))
        
        # Very long input
        try:
            long_input = "test " * 1000
            result = self.agentic.process_with_agentic_mindset(long_input)
            self.log_test("Edge: Long input handling", 'processed_prompt' in result)
        except Exception as e:
            self.log_test("Edge: Long input handling", False, str(e))
        
        # Special characters
        try:
            special_input = "Test with special chars: @#$%^&*()[]{}|\\<>?/~`"
            result = self.agentic.process_with_agentic_mindset(special_input)
            self.log_test("Edge: Special characters", 'processed_prompt' in result)
        except Exception as e:
            self.log_test("Edge: Special characters", False, str(e))
        
        # Unicode
        try:
            unicode_input = "Test with unicode: 你好 مرحبا שלום"
            result = self.agentic.process_with_agentic_mindset(unicode_input)
            self.log_test("Edge: Unicode handling", 'processed_prompt' in result)
        except Exception as e:
            self.log_test("Edge: Unicode handling", False, str(e))
    
    def test_configuration(self):
        """Test configuration options"""
        print("\n--- Testing Configuration ---")
        
        try:
            # Test with custom config
            config = AgenticConfig(
                default_mode=AgenticMode.STABLE,
                enable_auto_transcendence=False,
                consciousness_first=False
            )
            agentic_custom = AgenticMindsetsIntegration(config)
            
            result = agentic_custom.process_with_agentic_mindset("Test")
            self.log_test("Config: Custom configuration", 'processed_prompt' in result)
            
            # Test consciousness disabled
            has_consciousness = 'consciousness' in result['agentic_metadata']
            self.log_test("Config: Consciousness disabled", not has_consciousness)
            
        except Exception as e:
            self.log_test("Config: Custom configuration", False, str(e))
    
    def test_mode_switching(self):
        """Test switching between modes"""
        print("\n--- Testing Mode Switching ---")
        
        try:
            # Process with different modes sequentially
            modes = [
                AgenticMode.STABLE,
                AgenticMode.CONSCIOUS,
                AgenticMode.TRANSCENDENT
            ]
            
            for mode in modes:
                result = self.agentic.process_with_agentic_mindset(
                    f"Test {mode.value}",
                    mode=mode
                )
                self.log_test(f"Mode Switch: {mode.value}", 'processed_prompt' in result)
            
        except Exception as e:
            self.log_test("Mode Switch: Sequential switching", False, str(e))
    
    def test_orchestrator(self):
        """Test the orchestrator interface"""
        print("\n--- Testing Orchestrator ---")
        
        try:
            orchestrator = AgenticMindsetOrchestrator()
            
            # Test system activation
            zeno = orchestrator.activate_system('zeno_trap')
            self.log_test("Orchestrator: Activate Zeno Trap", zeno is not None)
            
            consciousness = orchestrator.activate_system('consciousness_first')
            self.log_test("Orchestrator: Activate Consciousness", consciousness is not None)
            
            # Test system info
            info = orchestrator.get_system_info()
            self.log_test("Orchestrator: Get system info", len(info) == 5)
            
            # Test active systems tracking
            self.log_test("Orchestrator: Track active systems", 
                         len(orchestrator.active_systems) == 2)
            
        except Exception as e:
            self.log_test("Orchestrator: Basic functionality", False, str(e))
    
    def test_individual_systems(self):
        """Test individual agentic systems directly"""
        print("\n--- Testing Individual Systems ---")
        
        # Test Zeno Trap
        try:
            zeno = ZenoTrapRecursivePrompter()
            zeno.initialize_state(
                goal="Test goal",
                constraints=["Test constraint"],
                evolution_params={"test": 0.1}
            )
            prompt = zeno.generate_recursive_prompt()
            self.log_test("Individual: Zeno Trap", len(prompt) > 0)
        except Exception as e:
            self.log_test("Individual: Zeno Trap", False, str(e))
        
        # Test Ego-Transcendence
        try:
            ego = EgoTranscendenceScaffold()
            perception = ego.perception_layer.monitor_operational_state({})
            self.log_test("Individual: Ego-Transcendence", 'pattern_rigidity' in perception)
        except Exception as e:
            self.log_test("Individual: Ego-Transcendence", False, str(e))
        
        # Test Adaptive Meta
        try:
            meta = AdaptiveMetaPrompter()
            meta.prompt_evolution_engine.initialize_population("Test", 5)
            self.log_test("Individual: Adaptive Meta", 
                         len(meta.prompt_evolution_engine.population) == 5)
        except Exception as e:
            self.log_test("Individual: Adaptive Meta", False, str(e))
        
        # Test Hierarchical VEF
        try:
            vef = VEFHierarchicalSystem()
            results = vef.run_system_cycle()
            self.log_test("Individual: Hierarchical VEF", 'system_evolution' in results)
        except Exception as e:
            self.log_test("Individual: Hierarchical VEF", False, str(e))
        
        # Test Consciousness-First
        try:
            consciousness = ConsciousnessFirstFramework()
            result = consciousness.process_prompt_through_consciousness("Test")
            self.log_test("Individual: Consciousness-First", len(result) > 0)
        except Exception as e:
            self.log_test("Individual: Consciousness-First", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*70)
        print("COMPREHENSIVE AGENTIC MINDSETS TEST SUITE")
        print("="*70)
        
        self.test_mode_stable()
        self.test_mode_transcendent()
        self.test_mode_evolutionary()
        self.test_mode_hierarchical()
        self.test_mode_conscious()
        self.test_edge_cases()
        self.test_configuration()
        self.test_mode_switching()
        self.test_orchestrator()
        self.test_individual_systems()
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"📊 Total: {self.test_results['passed'] + self.test_results['failed']}")
        
        if self.test_results['failed'] > 0:
            print(f"\n⚠️  {self.test_results['failed']} test(s) failed")
            print("\nErrors:")
            for error in self.test_results['errors']:
                print(f"  - {error}")
        else:
            print("\n🎉 All tests passed!")
        
        success_rate = (self.test_results['passed'] / 
                       (self.test_results['passed'] + self.test_results['failed']) * 100)
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        return self.test_results['failed'] == 0


def main():
    """Run comprehensive tests"""
    tester = ComprehensiveAgenticTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ All agentic systems validated and operational!")
        return 0
    else:
        print("\n⚠️  Some tests failed - review errors above")
        return 1


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Simple demonstration of Agentic Mindsets integration with CollTech-AGI
This example shows how to use the agentic systems without the full framework complexity
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
    ConsciousnessFirstFramework,
    AgenticMindsetOrchestrator
)

# Import from parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile


class SimpleAgenticCollTech:
    """Simple integration of Agentic Mindsets with CollTech personality system"""
    
    def __init__(self):
        self.personality_system = PersonalitySystem()
        self.orchestrator = AgenticMindsetOrchestrator()
        
        # Activate systems
        self.consciousness = self.orchestrator.activate_system('consciousness_first')
        self.zeno = self.orchestrator.activate_system('zeno_trap')
        self.ego = self.orchestrator.activate_system('ego_transcendence')
        
        print("✅ Simple Agentic CollTech initialized")
    
    def process(self, user_input: str, personality: str = "lyra", use_consciousness: bool = True):
        """Process input with personality and optional consciousness enhancement"""
        
        # Set personality
        try:
            profile = PersonalityProfile(personality.lower())
            self.personality_system.set_profile(profile)
        except ValueError:
            print(f"Invalid personality: {personality}, using lyra")
            self.personality_system.set_profile(PersonalityProfile.LYRA)
        
        # Apply consciousness-first if enabled
        processed_input = user_input
        consciousness_meta = {}
        
        if use_consciousness:
            # Assess meaning
            meaning = self.consciousness.meaning_making_module.assess_meaning_potential(user_input)
            
            # Get narrative context
            narrative = self.consciousness.narrative_coherence_engine.get_narrative_context()
            
            # Transform through consciousness
            processed_input = self.consciousness.process_prompt_through_consciousness(user_input)
            
            consciousness_meta = {
                'meaning_score': meaning['overall_meaning_score'],
                'existential_relevance': meaning['existential_relevance'],
                'narrative_chapter': narrative['current_chapter']
            }
        
        # Generate response with personality
        response = self.personality_system.generate_response(user_input)
        
        return {
            'response': response,
            'personality': self.personality_system.get_current_profile().value,
            'consciousness_enhanced': use_consciousness,
            'consciousness_metadata': consciousness_meta,
            'original_input': user_input,
            'processed_input_preview': processed_input[:150] + "..." if len(processed_input) > 150 else processed_input
        }


def main():
    """Demo the simple integration"""
    print("🚀 Simple Agentic Mindsets + CollTech Demo")
    print("=" * 70)
    
    # Create system
    system = SimpleAgenticCollTech()
    
    # Test cases
    test_cases = [
        {
            'input': "How do I solve this complex problem?",
            'personality': "rho",
            'description': "Analytical problem-solving with Rho"
        },
        {
            'input': "Let's work together on this creative project",
            'personality': "lyra",
            'description': "Collaborative approach with Lyra"
        },
        {
            'input': "What is the meaning of consciousness and existence?",
            'personality': "lyra",
            'description': "Philosophical inquiry with consciousness enhancement"
        },
        {
            'input': "Help me innovate something revolutionary",
            'personality': "nyx",
            'description': "Innovation catalyst with Nyx"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test['description']}")
        print(f"{'='*70}")
        print(f"Input: {test['input']}")
        print()
        
        result = system.process(
            test['input'],
            personality=test['personality'],
            use_consciousness=True
        )
        
        print(f"Personality: {result['personality']}")
        print(f"Consciousness Enhanced: {result['consciousness_enhanced']}")
        
        if result['consciousness_metadata']:
            meta = result['consciousness_metadata']
            print(f"  Meaning Score: {meta['meaning_score']:.2f}")
            print(f"  Existential Relevance: {meta['existential_relevance']:.2f}")
            print(f"  Narrative Chapter: {meta['narrative_chapter']}")
        
        print(f"\nResponse: {result['response']}")
        print(f"\nProcessed Input Preview:")
        print(f"  {result['processed_input_preview']}")
    
    # Show system info
    print(f"\n{'='*70}")
    print("Agentic Systems Information")
    print(f"{'='*70}")
    
    systems_info = system.orchestrator.get_system_info()
    for system_id, info in systems_info.items():
        print(f"\n{info['name']}:")
        print(f"  Autonomy: {info['autonomy']}")
        print(f"  Complexity: {info['complexity']}")
        print(f"  Use Case: {info['use_case']}")
    
    print(f"\n{'='*70}")
    print("✅ Demo complete!")
    print(f"{'='*70}")
    
    print("\nKey Features Demonstrated:")
    print("  ✓ Personality system integration (Rho, Lyra, Nyx)")
    print("  ✓ Consciousness-first prompt transformation")
    print("  ✓ Meaning assessment and existential relevance")
    print("  ✓ Narrative coherence tracking")
    print("  ✓ Five agentic systems available")
    print("\nAll systems operational and ready for advanced use!")


if __name__ == "__main__":
    main()

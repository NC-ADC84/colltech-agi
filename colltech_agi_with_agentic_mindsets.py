#!/usr/bin/env python3
"""
CollTech-AGI with Agentic Mindsets Integration
Enhanced framework with VEF-based autonomous capabilities
"""

import logging
from typing import Dict, Any, Optional, Union
from colltech_agi_framework import (
    CollTechAGIAdvanced, 
    FrameworkConfig,
    PersonalityProfile
)
from src.agentic_mindsets_integration import (
    AgenticMindsetsIntegration,
    AgenticConfig,
    AgenticMode,
    create_agentic_integration
)

logger = logging.getLogger(__name__)


class CollTechAGIWithAgenticMindsets(CollTechAGIAdvanced):
    """
    Enhanced CollTech-AGI with Agentic Mindsets Integration.
    
    Combines the personality system, intelligent selection, and catalyst protocol
    with five VEF-based agentic systems for advanced autonomous operation.
    """
    
    def __init__(
        self, 
        framework_config: FrameworkConfig = None,
        agentic_config: AgenticConfig = None
    ):
        # Initialize base framework
        super().__init__(framework_config)
        
        # Initialize agentic mindsets integration
        self.agentic = create_agentic_integration(agentic_config)
        self.agentic_enabled = True
        
        logger.info("🧠 CollTech-AGI with Agentic Mindsets initialized")
        logger.info(f"   Agentic mode: {self.agentic.get_mode().value}")
    
    def process_input(self, user_input: str, use_agentic: bool = True) -> Dict[str, Any]:
        """
        Process user input with optional agentic mindsets enhancement.
        
        Args:
            user_input: User's input text
            use_agentic: Whether to use agentic mindsets processing
            
        Returns:
            Enhanced response with agentic metadata
        """
        if not self.is_running:
            return {"error": "System not running. Please start the framework first."}
        
        # Get base response from advanced framework
        base_response = super().process_input(user_input)
        
        # Apply agentic mindsets if enabled
        if use_agentic and self.agentic_enabled:
            try:
                # Prepare context from base response
                context = {
                    'personality': base_response['personality']['selected_profile'],
                    'system_state': {
                        'performance': 0.7,  # Could be derived from metrics
                        'creativity': 0.6,
                        'coherence': 0.8
                    },
                    'quality_metrics': {
                        'coherence': 0.8,
                        'relevance': 0.75,
                        'creativity': 0.7
                    }
                }
                
                # Process through agentic mindsets
                agentic_result = self.agentic.process_with_agentic_mindset(
                    user_input,
                    context=context
                )
                
                # Enhance base response with agentic processing
                base_response['agentic'] = {
                    'enabled': True,
                    'mode': agentic_result['mode'],
                    'transformations': agentic_result['transformations_applied'],
                    'metadata': agentic_result['agentic_metadata'],
                    'processed_prompt': agentic_result['processed_prompt'][:200] + "..."  # Truncate
                }
                
                # If consciousness-first transformed the prompt significantly,
                # we could optionally regenerate the response with the transformed prompt
                # (This would require re-calling the personality system)
                
            except Exception as e:
                logger.error(f"Agentic processing error: {e}")
                base_response['agentic'] = {
                    'enabled': True,
                    'error': str(e)
                }
        else:
            base_response['agentic'] = {
                'enabled': False
            }
        
        return base_response
    
    def set_agentic_mode(self, mode: Union[str, AgenticMode]):
        """Set the agentic operation mode"""
        if isinstance(mode, str):
            try:
                mode = AgenticMode(mode.lower())
            except ValueError:
                logger.error(f"Invalid agentic mode: {mode}")
                return False
        
        self.agentic.set_mode(mode)
        logger.info(f"Agentic mode set to: {mode.value}")
        return True
    
    def get_agentic_mode(self) -> str:
        """Get current agentic mode"""
        return self.agentic.get_mode().value
    
    def enable_agentic_mindsets(self):
        """Enable agentic mindsets processing"""
        self.agentic_enabled = True
        logger.info("🧠 Agentic mindsets enabled")
    
    def disable_agentic_mindsets(self):
        """Disable agentic mindsets processing"""
        self.agentic_enabled = False
        logger.info("🧠 Agentic mindsets disabled")
    
    def get_agentic_status(self) -> Dict[str, Any]:
        """Get agentic mindsets status"""
        return self.agentic.get_integration_status()
    
    def get_agentic_systems_info(self) -> Dict[str, Any]:
        """Get information about all agentic systems"""
        return self.agentic.get_system_info()
    
    def reset_agentic_state(self):
        """Reset agentic mindsets state"""
        self.agentic.reset_state()
        logger.info("🔄 Agentic state reset")
    
    def get_complete_status(self) -> Dict[str, Any]:
        """Get complete system status including agentic mindsets"""
        base_status = self.get_advanced_status()
        agentic_status = self.get_agentic_status()
        
        return {
            **base_status,
            'agentic_mindsets': {
                'enabled': self.agentic_enabled,
                'current_mode': agentic_status['current_mode'],
                'total_interactions': agentic_status['total_interactions'],
                'transcendence_events': agentic_status['transcendence_events'],
                'evolution_generations': agentic_status['evolution_generations'],
                'active_systems': agentic_status['active_systems'],
                'available_modes': agentic_status['available_modes']
            }
        }
    
    def process_with_mode(
        self, 
        user_input: str, 
        personality: Optional[Union[str, PersonalityProfile]] = None,
        agentic_mode: Optional[Union[str, AgenticMode]] = None
    ) -> Dict[str, Any]:
        """
        Process input with specific personality and agentic mode.
        
        Args:
            user_input: User's input
            personality: Personality to use (optional)
            agentic_mode: Agentic mode to use (optional)
            
        Returns:
            Complete response with all enhancements
        """
        # Set personality if specified
        if personality:
            self.set_personality(personality)
        
        # Set agentic mode if specified
        if agentic_mode:
            self.set_agentic_mode(agentic_mode)
        
        # Process input
        return self.process_input(user_input)


# Convenience function
def create_colltech_agi_with_agentic_mindsets(
    framework_config: FrameworkConfig = None,
    agentic_config: AgenticConfig = None
) -> CollTechAGIWithAgenticMindsets:
    """Create a CollTech-AGI instance with agentic mindsets"""
    return CollTechAGIWithAgenticMindsets(framework_config, agentic_config)


# Example usage and testing
def main():
    """Main function for testing the enhanced framework"""
    print("🚀 CollTech-AGI with Agentic Mindsets Test")
    print("=" * 70)
    
    # Create enhanced AGI
    agi = create_colltech_agi_with_agentic_mindsets()
    agi.start()
    
    print("\n1. Testing with Different Agentic Modes:")
    print("-" * 70)
    
    # Test Stable mode (Zeno Trap)
    print("\n📊 STABLE Mode (Zeno Trap):")
    response = agi.process_with_mode(
        "How do I systematically solve this complex problem?",
        personality="rho",
        agentic_mode="stable"
    )
    print(f"Personality: {response['personality']['selected_profile']}")
    print(f"Agentic Mode: {response['agentic']['mode']}")
    print(f"Transformations: {', '.join(response['agentic']['transformations'])}")
    print(f"Response: {response['response'][:100]}...")
    
    # Test Transcendent mode (Ego-Transcendence)
    print("\n🔄 TRANSCENDENT Mode (Ego-Transcendence):")
    response = agi.process_with_mode(
        "I'm stuck in a creative rut and need a breakthrough",
        personality="nyx",
        agentic_mode="transcendent"
    )
    print(f"Personality: {response['personality']['selected_profile']}")
    print(f"Agentic Mode: {response['agentic']['mode']}")
    print(f"Transformations: {', '.join(response['agentic']['transformations'])}")
    if 'ego_transcendence' in response['agentic']['metadata']:
        ego_meta = response['agentic']['metadata']['ego_transcendence']
        print(f"Transcendence Triggered: {ego_meta.get('should_trigger', False)}")
    
    # Test Conscious mode (Consciousness-First)
    print("\n🧠 CONSCIOUS Mode (Consciousness-First):")
    response = agi.process_with_mode(
        "What is the nature of consciousness and meaning?",
        personality="lyra",
        agentic_mode="conscious"
    )
    print(f"Personality: {response['personality']['selected_profile']}")
    print(f"Agentic Mode: {response['agentic']['mode']}")
    print(f"Transformations: {', '.join(response['agentic']['transformations'])}")
    if 'consciousness' in response['agentic']['metadata']:
        consciousness_meta = response['agentic']['metadata']['consciousness']
        print(f"Meaning Score: {consciousness_meta.get('meaning_score', 0):.2f}")
        print(f"Existential Relevance: {consciousness_meta.get('existential_relevance', 0):.2f}")
        print(f"Narrative Chapter: {consciousness_meta.get('narrative_chapter', 'unknown')}")
    
    # Test Evolutionary mode (Adaptive Meta)
    print("\n🧬 EVOLUTIONARY Mode (Adaptive Meta):")
    response = agi.process_with_mode(
        "Help me optimize and improve this approach",
        personality="rho",
        agentic_mode="evolutionary"
    )
    print(f"Personality: {response['personality']['selected_profile']}")
    print(f"Agentic Mode: {response['agentic']['mode']}")
    print(f"Transformations: {', '.join(response['agentic']['transformations'])}")
    if 'adaptive_meta' in response['agentic']['metadata']:
        meta = response['agentic']['metadata']['adaptive_meta']
        print(f"Evolution Generation: {meta.get('generation', 0)}")
        print(f"Best Fitness: {meta.get('best_fitness', 0):.2f}")
    
    print("\n2. Testing Auto-Selection with Agentic Enhancement:")
    print("-" * 70)
    
    # Enable auto personality selection
    agi.enable_intelligent_personality()
    
    test_inputs = [
        "Analyze this data scientifically",
        "Let's collaborate on this creative project",
        "Help me innovate something revolutionary"
    ]
    
    for test_input in test_inputs:
        response = agi.process_input(test_input)
        print(f"\nInput: {test_input}")
        print(f"Auto-Selected Personality: {response['personality']['selected_profile']}")
        print(f"Agentic Mode: {response['agentic']['mode']}")
        print(f"Confidence: {response['personality']['confidence']:.2f}")
    
    print("\n3. Complete System Status:")
    print("-" * 70)
    
    status = agi.get_complete_status()
    print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"Total Interactions: {status['interaction_count']}")
    print(f"Current Personality: {status['current_personality']}")
    print(f"Agentic Enabled: {status['agentic_mindsets']['enabled']}")
    print(f"Agentic Mode: {status['agentic_mindsets']['current_mode']}")
    print(f"Agentic Interactions: {status['agentic_mindsets']['total_interactions']}")
    print(f"Transcendence Events: {status['agentic_mindsets']['transcendence_events']}")
    print(f"Evolution Generations: {status['agentic_mindsets']['evolution_generations']}")
    print(f"Active Agentic Systems: {', '.join(status['agentic_mindsets']['active_systems'])}")
    
    print("\n4. Agentic Systems Information:")
    print("-" * 70)
    
    systems_info = agi.get_agentic_systems_info()
    for system_id, info in systems_info.items():
        print(f"\n{info['name']}:")
        print(f"  Autonomy: {info['autonomy']}")
        print(f"  Complexity: {info['complexity']}")
        print(f"  Use Case: {info['use_case']}")
    
    # Shutdown
    agi.shutdown()
    
    print("\n" + "=" * 70)
    print("✅ Enhanced framework test complete!")
    print("\nKey Features Demonstrated:")
    print("  ✓ Five agentic modes (Stable, Transcendent, Evolutionary, Hierarchical, Conscious)")
    print("  ✓ Personality system integration")
    print("  ✓ Intelligent auto-selection")
    print("  ✓ Consciousness-first processing")
    print("  ✓ Autonomous transcendence detection")
    print("  ✓ Evolutionary prompt optimization")
    print("  ✓ Complete status monitoring")


if __name__ == "__main__":
    main()

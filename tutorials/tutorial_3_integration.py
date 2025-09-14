#!/usr/bin/env python3
"""
Tutorial 3: CollTech-AGI Integration Examples

This tutorial covers integration examples for the CollTech-AGI framework.
You'll learn about:
- Custom framework extensions
- Integration with external systems
- Building custom personality profiles
- Creating custom selection logic
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile, AttributeType
from intelligent_personality_selector import IntelligentPersonalitySelector

def tutorial_3_integration():
    """Tutorial 3: Integration examples."""
    print("🎓 TUTORIAL 3: CollTech-AGI Integration Examples")
    print("=" * 60)
    print("In this tutorial, you'll learn:")
    print("• Custom framework extensions")
    print("• Integration with external systems")
    print("• Building custom personality profiles")
    print("• Creating custom selection logic")
    print("=" * 60)
    
    # Step 1: Custom framework extension
    print("\n📚 Step 1: Custom Framework Extension")
    print("-" * 40)
    
    class CustomCollTechAGI(CollTechAGIAdvanced):
        """Custom CollTech-AGI with additional features."""
        
        def __init__(self, config=None):
            super().__init__(config)
            self.custom_features = {
                "mood_tracking": True,
                "conversation_memory": [],
                "user_preferences": {}
            }
            print("✅ Custom CollTech-AGI initialized with additional features")
        
        def process_input(self, user_input: str):
            """Override process_input to add custom features."""
            # Store conversation in memory
            self.custom_features["conversation_memory"].append({
                "input": user_input,
                "timestamp": time.time()
            })
            
            # Process with parent class
            result = super().process_input(user_input)
            
            # Add custom features to result
            result["custom_features"] = {
                "conversation_length": len(self.custom_features["conversation_memory"]),
                "mood_tracking": self.custom_features["mood_tracking"]
            }
            
            return result
        
        def get_conversation_history(self):
            """Get conversation history."""
            return self.custom_features["conversation_memory"]
        
        def set_user_preference(self, key: str, value: any):
            """Set user preference."""
            self.custom_features["user_preferences"][key] = value
        
        def get_user_preference(self, key: str):
            """Get user preference."""
            return self.custom_features["user_preferences"].get(key)
    
    # Test custom framework
    import time
    custom_agi = CustomCollTechAGI()
    custom_agi.start()
    
    print("Testing custom framework:")
    result = custom_agi.process_input("Hello, this is a test")
    print(f"Response: {result['response']}")
    print(f"Custom features: {result['custom_features']}")
    
    # Step 2: Custom personality profile
    print("\n📚 Step 2: Custom Personality Profile")
    print("-" * 40)
    
    class CustomPersonalitySystem(PersonalitySystem):
        """Custom personality system with additional profiles."""
        
        def __init__(self):
            super().__init__()
            # Add custom personality descriptions
            self.custom_descriptions = {
                "creative_analyst": "Combines analytical thinking with creative problem-solving",
                "empathetic_innovator": "Balances innovation with emotional intelligence",
                "systematic_creator": "Systematic approach to creative endeavors"
            }
        
        def get_custom_profile_description(self, profile_name: str) -> str:
            """Get custom profile description."""
            return self.custom_descriptions.get(profile_name, "Custom profile")
        
        def generate_custom_response(self, user_input: str, profile_name: str) -> str:
            """Generate response for custom profile."""
            base_response = self.generate_response(user_input)
            custom_description = self.get_custom_profile_description(profile_name)
            return f"[{profile_name.title()}] {base_response} | {custom_description}"
    
    # Test custom personality system
    custom_personality = CustomPersonalitySystem()
    custom_personality.set_profile(PersonalityProfile.RHO)
    
    print("Testing custom personality system:")
    response = custom_personality.generate_custom_response("Help me solve this", "creative_analyst")
    print(f"Custom response: {response}")
    
    # Step 3: Custom selection logic
    print("\n📚 Step 3: Custom Selection Logic")
    print("-" * 40)
    
    class CustomPersonalitySelector(IntelligentPersonalitySelector):
        """Custom personality selector with additional logic."""
        
        def __init__(self):
            super().__init__()
            self.custom_rules = {
                "technical_keywords": ["code", "programming", "algorithm", "system"],
                "creative_keywords": ["design", "art", "creative", "innovative"],
                "collaborative_keywords": ["team", "together", "collaborate", "help"]
            }
        
        def _calculate_personality_scores(self, pattern):
            """Override to add custom scoring logic."""
            scores = super()._calculate_personality_scores(pattern)
            
            # Add custom keyword-based scoring
            content_lower = pattern.content.lower()
            
            # Technical keywords favor Rho
            tech_count = sum(1 for keyword in self.custom_rules["technical_keywords"] 
                           if keyword in content_lower)
            if tech_count > 0:
                scores[PersonalityProfile.RHO] += 0.2
            
            # Creative keywords favor Nyx
            creative_count = sum(1 for keyword in self.custom_rules["creative_keywords"] 
                               if keyword in content_lower)
            if creative_count > 0:
                scores[PersonalityProfile.NYX] += 0.2
            
            # Collaborative keywords favor Lyra
            collab_count = sum(1 for keyword in self.custom_rules["collaborative_keywords"] 
                             if keyword in content_lower)
            if collab_count > 0:
                scores[PersonalityProfile.LYRA] += 0.2
            
            return scores
        
        def get_custom_rules(self):
            """Get custom rules."""
            return self.custom_rules
    
    # Test custom selector
    custom_selector = CustomPersonalitySelector()
    
    print("Testing custom selection logic:")
    test_inputs = [
        "Help me write code for this algorithm",
        "Let's design something creative and innovative",
        "We need to work together as a team"
    ]
    
    for test_input in test_inputs:
        selection = custom_selector.select_personality(test_input)
        print(f"Input: {test_input}")
        print(f"Selected: {selection.selected_profile.value.title()}")
        print(f"Reasoning: {selection.reasoning}")
        print()
    
    # Step 4: External system integration
    print("\n📚 Step 4: External System Integration")
    print("-" * 40)
    
    class ExternalSystemIntegration:
        """Example of integrating with external systems."""
        
        def __init__(self, agi_instance):
            self.agi = agi_instance
            self.external_data = {}
            self.integration_status = "active"
        
        def process_with_external_data(self, user_input: str, external_context: dict):
            """Process input with external context."""
            # Store external context
            self.external_data = external_context
            
            # Modify input based on external context
            enhanced_input = f"[Context: {external_context.get('source', 'unknown')}] {user_input}"
            
            # Process with AGI
            result = self.agi.process_input(enhanced_input)
            
            # Add external context to result
            result["external_context"] = external_context
            result["integration_status"] = self.integration_status
            
            return result
        
        def get_integration_status(self):
            """Get integration status."""
            return {
                "status": self.integration_status,
                "external_data_count": len(self.external_data),
                "last_context": self.external_data
            }
    
    # Test external system integration
    integration = ExternalSystemIntegration(custom_agi)
    
    print("Testing external system integration:")
    external_context = {
        "source": "web_api",
        "user_id": "12345",
        "session_id": "abc123",
        "timestamp": time.time()
    }
    
    result = integration.process_with_external_data("Help me with this problem", external_context)
    print(f"Response: {result['response']}")
    print(f"External context: {result['external_context']}")
    print(f"Integration status: {result['integration_status']}")
    
    # Step 5: Building a complete custom system
    print("\n📚 Step 5: Building a Complete Custom System")
    print("-" * 40)
    
    class CompleteCustomSystem:
        """Complete custom system combining all features."""
        
        def __init__(self):
            # Initialize components
            self.agi = CustomCollTechAGI()
            self.personality = CustomPersonalitySystem()
            self.selector = CustomPersonalitySelector()
            self.integration = ExternalSystemIntegration(self.agi)
            
            # Start the system
            self.agi.start()
            print("✅ Complete custom system initialized")
        
        def process_complete(self, user_input: str, external_context: dict = None):
            """Process input through complete custom system."""
            # Use custom selector
            selection = self.selector.select_personality(user_input)
            self.agi.personality_system.set_profile(selection.selected_profile)
            
            # Process with external integration if context provided
            if external_context:
                result = self.integration.process_with_external_data(user_input, external_context)
            else:
                result = self.agi.process_input(user_input)
            
            # Add selection info
            result["custom_selection"] = {
                "selected_profile": selection.selected_profile.value,
                "confidence": selection.confidence_score,
                "reasoning": selection.reasoning
            }
            
            return result
        
        def get_system_status(self):
            """Get complete system status."""
            agi_status = self.agi.get_advanced_status()
            integration_status = self.integration.get_integration_status()
            
            return {
                "agi_status": agi_status,
                "integration_status": integration_status,
                "custom_features": self.agi.custom_features
            }
        
        def shutdown(self):
            """Shutdown the system."""
            self.agi.shutdown()
            print("✅ Complete custom system shutdown")
    
    # Test complete custom system
    complete_system = CompleteCustomSystem()
    
    print("Testing complete custom system:")
    result = complete_system.process_complete("Help me create an innovative solution")
    print(f"Response: {result['response']}")
    print(f"Custom selection: {result['custom_selection']}")
    print(f"Custom features: {result['custom_features']}")
    
    # Step 6: Interactive custom system
    print("\n📚 Step 6: Interactive Custom System")
    print("-" * 40)
    print("Let's test the complete custom system interactively!")
    print("Commands:")
    print("• 'status' - Show system status")
    print("• 'history' - Show conversation history")
    print("• 'preference <key> <value>' - Set user preference")
    print("• 'rules' - Show custom selection rules")
    print("• 'quit' - End tutorial")
    
    # Interactive loop
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                status = complete_system.get_system_status()
                print(f"\n📊 System Status:")
                print(f"• Interactions: {status['agi_status']['interaction_count']}")
                print(f"• Custom Features: {status['custom_features']}")
                print(f"• Integration: {status['integration_status']}")
            elif user_input.lower() == 'history':
                history = complete_system.agi.get_conversation_history()
                print(f"\n📚 Conversation History ({len(history)} entries):")
                for i, entry in enumerate(history[-5:], 1):
                    print(f"{i}. {entry['input'][:50]}...")
            elif user_input.startswith('preference '):
                parts = user_input.split(' ', 2)
                if len(parts) >= 3:
                    key, value = parts[1], parts[2]
                    complete_system.agi.set_user_preference(key, value)
                    print(f"\n✅ Preference set: {key} = {value}")
                else:
                    print(f"\n❌ Usage: preference <key> <value>")
            elif user_input.lower() == 'rules':
                rules = complete_system.selector.get_custom_rules()
                print(f"\n📋 Custom Selection Rules:")
                for rule_type, keywords in rules.items():
                    print(f"• {rule_type}: {', '.join(keywords)}")
            else:
                # Process with complete system
                result = complete_system.process_complete(user_input)
                
                print(f"\n🧠 Custom-Selected: {result['custom_selection']['selected_profile'].title()}")
                print(f"💭 Reasoning: {result['custom_selection']['reasoning']}")
                print(f"🎯 Confidence: {result['custom_selection']['confidence']:.2f}")
                print(f"🤖 Response: {result['response']}")
                print(f"🔧 Custom Features: {result['custom_features']}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Step 7: Cleanup
    print("\n📚 Step 7: Cleanup")
    print("-" * 40)
    
    # Shutdown all systems
    complete_system.shutdown()
    custom_agi.shutdown()
    
    print("✅ All systems shutdown complete")
    
    print("\n🎉 Tutorial 3 Complete!")
    print("=" * 60)
    print("You've learned:")
    print("✅ Custom framework extensions")
    print("✅ Integration with external systems")
    print("✅ Building custom personality profiles")
    print("✅ Creating custom selection logic")
    print("✅ Building complete custom systems")
    print("✅ Interactive custom functionality")
    print("\nYou're now ready to build your own CollTech-AGI integrations!")

def main():
    """Main function to run tutorial 3."""
    tutorial_3_integration()

if __name__ == "__main__":
    main()

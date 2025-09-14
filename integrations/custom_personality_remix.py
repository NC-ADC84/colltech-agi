#!/usr/bin/env python3
"""
Custom Personality Remix - CollTech-AGI Framework

This example shows how to create custom personality profiles
by remixing and extending the existing personality system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile, AttributeType
from colltech_agi_framework import CollTechAGI, FrameworkConfig

class CustomPersonalityRemix(PersonalitySystem):
    """Custom personality system with remixed profiles."""
    
    def __init__(self):
        super().__init__()
        
        # Create custom personality profiles by remixing attributes
        self.custom_profiles = {
            "analyst_creator": {
                "description": "Analytical creator - combines systematic analysis with creative innovation",
                "attributes": {
                    AttributeType.ARCHIVIST: 0.9,  # High knowledge preservation
                    AttributeType.SKEPTIC: 0.8,    # High critical analysis
                    AttributeType.BUILDER: 0.9,    # High construction
                    AttributeType.CATALYST: 0.7,   # Moderate transformation
                    AttributeType.MIRROR: 0.5,     # Moderate reflection
                    AttributeType.LISTENER: 0.6    # Moderate listening
                }
            },
            "empathetic_innovator": {
                "description": "Empathetic innovator - balances innovation with emotional intelligence",
                "attributes": {
                    AttributeType.MIRROR: 0.9,     # High reflection
                    AttributeType.LISTENER: 0.8,   # High listening
                    AttributeType.CATALYST: 0.9,   # High transformation
                    AttributeType.BUILDER: 0.7,    # Moderate construction
                    AttributeType.WEAVER: 0.8,     # High connection
                    AttributeType.VOICE: 0.7       # Moderate expression
                }
            },
            "systematic_gardener": {
                "description": "Systematic gardener - combines systematic approach with nurturing growth",
                "attributes": {
                    AttributeType.ARCHIVIST: 0.8,  # High knowledge preservation
                    AttributeType.JUDGE: 0.7,      # High evaluation
                    AttributeType.GARDENER: 0.9,   # High nurturing
                    AttributeType.WEAVER: 0.8,     # High connection
                    AttributeType.SENTINEL: 0.6,   # Moderate protection
                    AttributeType.BRIDGE: 0.7      # Moderate mediation
                }
            }
        }
        
        # Override default profiles with custom ones
        self._apply_custom_profiles()
    
    def _apply_custom_profiles(self):
        """Apply custom profiles to the personality system."""
        for profile_name, profile_data in self.custom_profiles.items():
            # Create custom personality scores
            custom_scores = PersonalityScores()
            for attr, score in profile_data["attributes"].items():
                setattr(custom_scores, attr.value, score)
            
            # Store custom profile
            setattr(self, f"_{profile_name}_scores", custom_scores)
    
    def get_custom_profile(self, profile_name: str):
        """Get custom profile information."""
        if profile_name in self.custom_profiles:
            return self.custom_profiles[profile_name]
        return None
    
    def generate_custom_response(self, user_input: str, profile_name: str) -> str:
        """Generate response using custom profile."""
        if profile_name not in self.custom_profiles:
            return self.generate_response(user_input)
        
        profile_data = self.custom_profiles[profile_name]
        description = profile_data["description"]
        
        # Generate base response
        base_response = self.generate_response(user_input)
        
        # Customize response based on profile
        if profile_name == "analyst_creator":
            return f"[Analyst-Creator] {base_response} | I approach this with systematic analysis and creative innovation."
        elif profile_name == "empathetic_innovator":
            return f"[Empathetic-Innovator] {base_response} | I understand your needs and will innovate with empathy."
        elif profile_name == "systematic_gardener":
            return f"[Systematic-Gardener] {base_response} | I'll nurture this systematically with care and structure."
        
        return base_response
    
    def get_custom_profile_attributes(self, profile_name: str):
        """Get attributes for custom profile."""
        if profile_name in self.custom_profiles:
            return self.custom_profiles[profile_name]["attributes"]
        return {}
    
    def list_custom_profiles(self):
        """List all custom profiles."""
        return list(self.custom_profiles.keys())

class CustomPersonalityAGI(CollTechAGI):
    """CollTech-AGI with custom personality remix."""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.custom_personality = CustomPersonalityRemix()
        self.current_custom_profile = None
    
    def set_custom_personality(self, profile_name: str):
        """Set custom personality profile."""
        if profile_name in self.custom_personality.list_custom_profiles():
            self.current_custom_profile = profile_name
            print(f"✅ Custom personality set to: {profile_name}")
            return True
        else:
            print(f"❌ Invalid custom profile. Available: {self.custom_personality.list_custom_profiles()}")
            return False
    
    def process_input(self, user_input: str) -> str:
        """Process input with custom personality."""
        if self.current_custom_profile:
            return self.custom_personality.generate_custom_response(user_input, self.current_custom_profile)
        else:
            return super().process_input(user_input)
    
    def get_custom_personality_info(self, profile_name: str = None):
        """Get custom personality information."""
        if profile_name is None:
            profile_name = self.current_custom_profile
        
        if profile_name and profile_name in self.custom_personality.list_custom_profiles():
            profile_data = self.custom_personality.get_custom_profile(profile_name)
            attributes = self.custom_personality.get_custom_profile_attributes(profile_name)
            
            return {
                "profile_name": profile_name,
                "description": profile_data["description"],
                "attributes": [(attr.value, score) for attr, score in attributes.items()],
                "current": profile_name == self.current_custom_profile
            }
        else:
            return {
                "available_profiles": self.custom_personality.list_custom_profiles(),
                "current_profile": self.current_custom_profile
            }

def main():
    """Main function to demonstrate custom personality remix."""
    print("🎨 Custom Personality Remix - CollTech-AGI Framework")
    print("=" * 60)
    print("This example demonstrates how to create custom personality profiles")
    print("by remixing and extending the existing personality system.")
    print("=" * 60)
    
    # Initialize custom AGI
    config = FrameworkConfig(debug_mode=True)
    custom_agi = CustomPersonalityAGI(config)
    custom_agi.start()
    
    print("\n🎭 Available Custom Personalities:")
    profiles = custom_agi.custom_personality.list_custom_profiles()
    for profile in profiles:
        info = custom_agi.get_custom_personality_info(profile)
        print(f"• {profile}: {info['description']}")
    
    print("\n💬 Testing Custom Personalities:")
    print("-" * 40)
    
    # Test each custom personality
    test_questions = [
        "Help me solve this complex problem",
        "I need to create something innovative",
        "Let's work together on this project"
    ]
    
    for profile in profiles:
        print(f"\n🎭 Testing {profile.upper()}:")
        custom_agi.set_custom_personality(profile)
        
        for question in test_questions:
            response = custom_agi.process_input(question)
            print(f"Q: {question}")
            print(f"A: {response}")
            print()
    
    print("\n🎮 Interactive Custom Personality Chat:")
    print("-" * 40)
    print("Commands:")
    print("• 'profile <name>' - Set custom personality")
    print("• 'info [profile]' - Show profile information")
    print("• 'list' - List available profiles")
    print("• 'quit' - Exit")
    
    # Interactive loop
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.startswith('profile '):
                profile_name = user_input.split(' ', 1)[1]
                custom_agi.set_custom_personality(profile_name)
            elif user_input.startswith('info'):
                parts = user_input.split(' ', 1)
                profile_name = parts[1] if len(parts) > 1 else None
                info = custom_agi.get_custom_personality_info(profile_name)
                print(f"\n📊 Profile Info: {info}")
            elif user_input.lower() == 'list':
                profiles = custom_agi.custom_personality.list_custom_profiles()
                print(f"\n📋 Available Profiles: {', '.join(profiles)}")
            else:
                response = custom_agi.process_input(user_input)
                current_profile = custom_agi.current_custom_profile or "default"
                print(f"\n🤖 CollTech-AGI ({current_profile}): {response}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Cleanup
    custom_agi.shutdown()
    print("\n✅ Custom personality remix demo complete!")

if __name__ == "__main__":
    main()

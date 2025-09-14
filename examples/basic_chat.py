#!/usr/bin/env python3
"""
Basic Chat Example - CollTech-AGI Framework

A simple example showing how to use the basic CollTech-AGI framework
for personality-based chat interactions.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGI, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

def main():
    """Main function for basic chat example."""
    print("🤖 CollTech-AGI Basic Chat Example")
    print("=" * 50)
    print("This example demonstrates basic personality-based chat.")
    print("Commands:")
    print("• 'personality <rho/lyra/nyx>' - Switch personality")
    print("• 'info' - Show personality info")
    print("• 'status' - Show system status")
    print("• 'quit' - Exit the chat")
    print("=" * 50)
    
    # Create framework configuration
    config = FrameworkConfig(
        auto_personality_enabled=False,  # Manual personality selection for this example
        debug_mode=True
    )
    
    # Initialize CollTech-AGI
    agi = CollTechAGI(config)
    agi.start()
    
    print(f"\n✅ CollTech-AGI started with {agi.get_personality()} personality")
    print("Type your message and press Enter to chat!")
    
    # Chat loop
    while agi.is_running:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                status = agi.get_system_status()
                print(f"\n📊 System Status:")
                print(f"• Uptime: {status['uptime_seconds']:.2f} seconds")
                print(f"• Interactions: {status['interaction_count']}")
                print(f"• Current Personality: {status['current_personality']}")
                print(f"• Auto-Personality: {status['config']['auto_personality_enabled']}")
            elif user_input.lower() == 'info':
                info = agi.get_personality_info()
                print(f"\n🎭 Personality Info:")
                print(f"• Current: {info['current_profile']}")
                print(f"• Description: {info['description']}")
                print(f"• Dominant Attributes: {', '.join([f'{attr} ({score:.1f})' for attr, score in info['dominant_attributes']])}")
                print(f"• Available: {', '.join(info['available_profiles'])}")
            elif user_input.startswith('personality '):
                profile_name = user_input.split(' ', 1)[1].lower()
                if agi.set_personality(profile_name):
                    print(f"\n🎭 Switched to {profile_name.title()} personality")
                    info = agi.get_personality_info()
                    print(f"Description: {info['description']}")
                else:
                    print(f"\n❌ Invalid personality. Available: rho, lyra, nyx")
            else:
                # Process user input
                response = agi.process_input(user_input)
                print(f"\n🤖 CollTech-AGI ({agi.get_personality().title()}): {response}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Shutdown
    agi.shutdown()
    print("\n👋 Chat session ended. Goodbye!")

if __name__ == "__main__":
    main()

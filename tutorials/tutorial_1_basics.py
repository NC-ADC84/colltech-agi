#!/usr/bin/env python3
"""
Tutorial 1: CollTech-AGI Framework Basics

This tutorial covers the fundamental concepts and usage of the CollTech-AGI framework.
You'll learn about:
- Basic framework initialization
- Personality system basics
- Simple chat interactions
- System status monitoring
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGI, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

def tutorial_1_basics():
    """Tutorial 1: Basic framework usage."""
    print("🎓 TUTORIAL 1: CollTech-AGI Framework Basics")
    print("=" * 60)
    print("In this tutorial, you'll learn:")
    print("• How to initialize the framework")
    print("• Basic personality system usage")
    print("• Simple chat interactions")
    print("• System status monitoring")
    print("=" * 60)
    
    # Step 1: Initialize the framework
    print("\n📚 Step 1: Initialize the Framework")
    print("-" * 40)
    
    # Create a basic configuration
    config = FrameworkConfig(
        auto_personality_enabled=False,  # We'll control personality manually
        debug_mode=True  # Enable debug output
    )
    
    # Initialize CollTech-AGI
    agi = CollTechAGI(config)
    print("✅ CollTech-AGI initialized with basic configuration")
    
    # Start the system
    agi.start()
    print("✅ CollTech-AGI started successfully")
    
    # Step 2: Explore personality system
    print("\n📚 Step 2: Explore Personality System")
    print("-" * 40)
    
    # Get current personality info
    info = agi.get_personality_info()
    print(f"Current personality: {info['current_profile']}")
    print(f"Description: {info['description']}")
    print(f"Available personalities: {', '.join(info['available_profiles'])}")
    
    # Step 3: Test different personalities
    print("\n📚 Step 3: Test Different Personalities")
    print("-" * 40)
    
    personalities = [
        ("rho", "How do I solve this complex problem?"),
        ("lyra", "Let's work together on this project"),
        ("nyx", "Help me create something innovative")
    ]
    
    for personality, question in personalities:
        print(f"\n🎭 Testing {personality.upper()} personality:")
        agi.set_personality(personality)
        response = agi.process_input(question)
        print(f"Question: {question}")
        print(f"Response: {response}")
        
        # Show personality details
        info = agi.get_personality_info()
        dominant_attrs = [f"{attr} ({score:.1f})" for attr, score in info['dominant_attributes']]
        print(f"Dominant attributes: {', '.join(dominant_attrs)}")
    
    # Step 4: System status monitoring
    print("\n📚 Step 4: System Status Monitoring")
    print("-" * 40)
    
    # Get system status
    status = agi.get_system_status()
    print("System Status:")
    print(f"• Running: {status['is_running']}")
    print(f"• Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"• Interactions: {status['interaction_count']}")
    print(f"• Current Personality: {status['current_personality']}")
    print(f"• Auto-Personality: {status['config']['auto_personality_enabled']}")
    print(f"• Debug Mode: {status['config']['debug_mode']}")
    
    # Step 5: Interactive chat
    print("\n📚 Step 5: Interactive Chat")
    print("-" * 40)
    print("Let's have a conversation! Try different personalities and questions.")
    print("Commands:")
    print("• 'personality <rho/lyra/nyx>' - Switch personality")
    print("• 'status' - Show system status")
    print("• 'quit' - End tutorial")
    
    # Interactive loop
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                status = agi.get_system_status()
                print(f"\n📊 Status: {status['interaction_count']} interactions, {status['uptime_seconds']:.2f}s uptime")
            elif user_input.startswith('personality '):
                profile = user_input.split(' ', 1)[1].lower()
                if agi.set_personality(profile):
                    info = agi.get_personality_info()
                    print(f"\n🎭 Switched to {profile.title()}: {info['description']}")
                else:
                    print(f"\n❌ Invalid personality. Use: rho, lyra, or nyx")
            else:
                response = agi.process_input(user_input)
                print(f"\n🤖 CollTech-AGI ({agi.get_personality().title()}): {response}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Step 6: Cleanup
    print("\n📚 Step 6: Cleanup")
    print("-" * 40)
    
    # Shutdown the system
    agi.shutdown()
    print("✅ CollTech-AGI shutdown complete")
    
    print("\n🎉 Tutorial 1 Complete!")
    print("=" * 60)
    print("You've learned:")
    print("✅ How to initialize CollTech-AGI")
    print("✅ Basic personality system usage")
    print("✅ How to switch between personalities")
    print("✅ System status monitoring")
    print("✅ Interactive chat functionality")
    print("\nNext: Tutorial 2 - Advanced Features")

def main():
    """Main function to run tutorial 1."""
    tutorial_1_basics()

if __name__ == "__main__":
    main()

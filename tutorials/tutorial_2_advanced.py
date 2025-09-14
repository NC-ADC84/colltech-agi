#!/usr/bin/env python3
"""
Tutorial 2: CollTech-AGI Advanced Features

This tutorial covers advanced features of the CollTech-AGI framework.
You'll learn about:
- Intelligent personality auto-selection
- Catalyst integration protocol (CIP v1)
- Advanced system monitoring
- Learning and adaptation
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

def tutorial_2_advanced():
    """Tutorial 2: Advanced framework features."""
    print("🎓 TUTORIAL 2: CollTech-AGI Advanced Features")
    print("=" * 60)
    print("In this tutorial, you'll learn:")
    print("• Intelligent personality auto-selection")
    print("• Catalyst integration protocol (CIP v1)")
    print("• Advanced system monitoring")
    print("• Learning and adaptation")
    print("=" * 60)
    
    # Step 1: Initialize advanced framework
    print("\n📚 Step 1: Initialize Advanced Framework")
    print("-" * 40)
    
    # Create advanced configuration
    config = FrameworkConfig(
        auto_personality_enabled=True,  # Enable intelligent selection
        catalyst_integration_enabled=True,
        realtime_apis_enabled=True,
        memory_lattice_enabled=True,
        drift_detection_enabled=True,
        tool_making_enabled=True,
        debug_mode=True
    )
    
    # Initialize advanced CollTech-AGI
    agi = CollTechAGIAdvanced(config)
    print("✅ CollTech-AGI Advanced initialized with all features")
    
    # Start the system
    agi.start()
    print("✅ CollTech-AGI Advanced started successfully")
    
    # Step 2: Intelligent personality selection
    print("\n📚 Step 2: Intelligent Personality Selection")
    print("-" * 40)
    
    # Test different types of questions to see auto-selection
    test_questions = [
        ("How do I analyze this complex data set?", "Should select RHO for analysis"),
        ("Let's work together on this collaborative project", "Should select LYRA for collaboration"),
        ("Help me create something revolutionary and innovative", "Should select NYX for innovation"),
        ("What is the history of this technology?", "Should select RHO for historical analysis"),
        ("I need someone to listen and understand my situation", "Should select LYRA for empathy"),
        ("How can we disrupt this industry with new ideas?", "Should select NYX for disruption")
    ]
    
    print("Testing intelligent personality selection:")
    for question, expected in test_questions:
        print(f"\n❓ Question: {question}")
        print(f"🎯 Expected: {expected}")
        
        result = agi.process_input(question)
        selected = result['personality']['selected_profile']
        confidence = result['personality']['confidence']
        reasoning = result['personality']['reasoning']
        
        print(f"🧠 Selected: {selected.title()} (confidence: {confidence:.2f})")
        print(f"💭 Reasoning: {reasoning}")
        print(f"🤖 Response: {result['response'][:100]}...")
    
    # Step 3: Catalyst integration protocol
    print("\n📚 Step 3: Catalyst Integration Protocol (CIP v1)")
    print("-" * 40)
    
    # Get catalyst status
    cip_status = agi.get_catalyst_status()
    print("Catalyst Integration Protocol Status:")
    print(f"• Status: {cip_status['catalyst_status']}")
    print(f"• Orbit Stability: {cip_status['orbit_stability']:.2f}")
    print(f"• Reciprocity Ratio: {cip_status['reciprocity_metrics']['ratio']:.2f}")
    print(f"• Containment Score: {cip_status['containment_metrics']['score']:.2f}")
    print(f"• Elevation Eligible: {cip_status['elevation']['eligible']}")
    
    # Test catalyst pairing
    print("\n🔗 Testing catalyst pairing with stabilizer:")
    pair_result = agi.pair_catalyst_with_stabilizer("rho")
    print(f"Pairing result: {pair_result}")
    
    # Test catalyst elevation
    print("\n🚀 Testing catalyst elevation:")
    elevation_result = agi.elevate_catalyst()
    print(f"Elevation result: {elevation_result}")
    
    # Step 4: Learning and adaptation
    print("\n📚 Step 4: Learning and Adaptation")
    print("-" * 40)
    
    # Show selection history
    history = agi.get_selection_history()
    print(f"Selection history: {len(history)} interactions")
    for i, entry in enumerate(history[-3:], 1):  # Show last 3
        print(f"{i}. {entry['interaction_type']} ({entry['data_context']}) - Complexity: {entry['complexity_level']:.2f}")
    
    # Show learned preferences
    preferences = agi.get_learned_preferences()
    print(f"\nLearned preferences: {len(preferences)} patterns")
    for pattern, score in list(preferences.items())[:3]:  # Show top 3
        print(f"• {pattern}: {score:.3f}")
    
    # Step 5: Advanced system monitoring
    print("\n📚 Step 5: Advanced System Monitoring")
    print("-" * 40)
    
    # Get advanced status
    status = agi.get_advanced_status()
    print("Advanced System Status:")
    print(f"• Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"• Interactions: {status['interaction_count']}")
    print(f"• Current Personality: {status['current_personality']}")
    print(f"• Intelligent Selection: {status['intelligent_personality']['enabled']}")
    print(f"• Catalyst Integration: {status['catalyst_integration']['enabled']}")
    print(f"• Memory Lattice: {status['advanced_features']['memory_lattice']}")
    print(f"• Drift Detection: {status['advanced_features']['drift_detection']}")
    print(f"• Tool Making: {status['advanced_features']['tool_making']}")
    
    # Step 6: Interactive advanced features
    print("\n📚 Step 6: Interactive Advanced Features")
    print("-" * 40)
    print("Let's explore advanced features interactively!")
    print("Commands:")
    print("• 'auto <on/off>' - Toggle intelligent personality selection")
    print("• 'cip_status' - Show catalyst integration status")
    print("• 'cip_pair <rho/lyra>' - Pair catalyst with stabilizer")
    print("• 'cip_elevate' - Attempt catalyst elevation")
    print("• 'history' - Show selection history")
    print("• 'preferences' - Show learned preferences")
    print("• 'reset' - Reset learned preferences")
    print("• 'status' - Show advanced system status")
    print("• 'quit' - End tutorial")
    
    # Interactive loop
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.startswith('auto '):
                mode = user_input.split(' ', 1)[1].lower()
                if mode == 'on':
                    agi.enable_intelligent_personality()
                    print(f"\n🧠 Intelligent personality selection ENABLED")
                elif mode == 'off':
                    agi.disable_intelligent_personality()
                    print(f"\n🧠 Intelligent personality selection DISABLED")
                else:
                    print(f"\n❌ Invalid mode. Use 'on' or 'off'")
            elif user_input.lower() == 'cip_status':
                cip_status = agi.get_catalyst_status()
                print(f"\n⚡ Catalyst Status: {cip_status['catalyst_status']}")
                print(f"Orbit Stability: {cip_status['orbit_stability']:.2f}")
                print(f"Reciprocity Ratio: {cip_status['reciprocity_metrics']['ratio']:.2f}")
            elif user_input.startswith('cip_pair '):
                stabilizer = user_input.split(' ', 1)[1]
                result = agi.pair_catalyst_with_stabilizer(stabilizer)
                print(f"\n🔗 Pairing Result: {result}")
            elif user_input.lower() == 'cip_elevate':
                result = agi.elevate_catalyst()
                print(f"\n🚀 Elevation Result: {result}")
            elif user_input.lower() == 'history':
                history = agi.get_selection_history()
                print(f"\n📊 Selection History ({len(history)} interactions):")
                for i, entry in enumerate(history[-5:], 1):
                    print(f"{i}. {entry['interaction_type']} ({entry['data_context']}) - Complexity: {entry['complexity_level']:.2f}")
            elif user_input.lower() == 'preferences':
                preferences = agi.get_learned_preferences()
                print(f"\n🎯 Learned Preferences ({len(preferences)} patterns):")
                for pattern, score in list(preferences.items())[:5]:
                    print(f"• {pattern}: {score:.3f}")
            elif user_input.lower() == 'reset':
                agi.reset_learned_preferences()
                print(f"\n🔄 Learned preferences reset")
            elif user_input.lower() == 'status':
                status = agi.get_advanced_status()
                print(f"\n📊 Advanced Status:")
                print(f"• Interactions: {status['interaction_count']}")
                print(f"• Intelligent Selection: {status['intelligent_personality']['enabled']}")
                print(f"• Catalyst Status: {status['catalyst_integration']['status']}")
                print(f"• Advanced Features: {status['advanced_features']}")
            else:
                # Process with advanced features
                result = agi.process_input(user_input)
                
                print(f"\n🧠 Auto-Selected: {result['personality']['selected_profile'].title()}")
                if result['personality']['auto_selected']:
                    print(f"💭 Reasoning: {result['personality']['reasoning']}")
                    print(f"🎯 Confidence: {result['personality']['confidence']:.2f}")
                
                print(f"🤖 Response: {result['response']}")
                
                # Show catalyst info if applicable
                if result['catalyst']:
                    print(f"⚡ Catalyst Status: {result['catalyst']['cip_status']}")
                    if result['catalyst']['safety_filters_triggered']:
                        print(f"🛡️ Safety Filters: {', '.join(result['catalyst']['safety_filters_triggered'])}")
                
                # Show memory info if applicable
                if result['memory']:
                    print(f"🧠 Memory: {result['memory']['memory_level']} storage")
                
                # Show drift info if applicable
                if result['drift']:
                    if result['drift']['drift_detected']:
                        print(f"⚠️ Drift Detected: {result['drift']['drift_score']:.2f}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Step 7: Cleanup
    print("\n📚 Step 7: Cleanup")
    print("-" * 40)
    
    # Shutdown the system
    agi.shutdown()
    print("✅ CollTech-AGI Advanced shutdown complete")
    
    print("\n🎉 Tutorial 2 Complete!")
    print("=" * 60)
    print("You've learned:")
    print("✅ Intelligent personality auto-selection")
    print("✅ Catalyst integration protocol (CIP v1)")
    print("✅ Advanced system monitoring")
    print("✅ Learning and adaptation features")
    print("✅ Interactive advanced functionality")
    print("\nNext: Tutorial 3 - Integration Examples")

def main():
    """Main function to run tutorial 2."""
    tutorial_2_advanced()

if __name__ == "__main__":
    main()

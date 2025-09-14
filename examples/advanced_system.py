#!/usr/bin/env python3
"""
Advanced System Example - CollTech-AGI Framework

An advanced example showing intelligent personality selection,
catalyst integration, and all advanced features.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

def main():
    """Main function for advanced system example."""
    print("🚀 CollTech-AGI Advanced System Example")
    print("=" * 60)
    print("This example demonstrates all advanced features:")
    print("• Intelligent personality auto-selection")
    print("• Catalyst integration protocol (CIP v1)")
    print("• Memory lattice and drift detection")
    print("• Tool making and real-time capabilities")
    print("=" * 60)
    print("Commands:")
    print("• 'auto <on/off>' - Toggle intelligent personality selection")
    print("• 'cip_status' - Show catalyst integration status")
    print("• 'cip_pair <rho/lyra>' - Pair catalyst with stabilizer")
    print("• 'cip_elevate' - Attempt catalyst elevation")
    print("• 'history' - Show selection history")
    print("• 'preferences' - Show learned preferences")
    print("• 'reset' - Reset learned preferences")
    print("• 'status' - Show advanced system status")
    print("• 'quit' - Exit the system")
    print("=" * 60)
    
    # Create advanced framework configuration
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
    agi.start()
    
    print(f"\n✅ CollTech-AGI Advanced started")
    print(f"🧠 Intelligent personality selection: {'ENABLED' if config.auto_personality_enabled else 'DISABLED'}")
    print(f"⚡ Catalyst integration: {'ENABLED' if config.catalyst_integration_enabled else 'DISABLED'}")
    print("Type your message and watch the system auto-select the best personality!")
    
    # Interactive loop
    while agi.is_running:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'status':
                status = agi.get_advanced_status()
                print(f"\n📊 Advanced System Status:")
                print(f"• Uptime: {status['uptime_seconds']:.2f} seconds")
                print(f"• Interactions: {status['interaction_count']}")
                print(f"• Current Personality: {status['current_personality']}")
                print(f"• Intelligent Selection: {status['intelligent_personality']['enabled']}")
                print(f"• Catalyst Status: {status['catalyst_integration']['status']}")
                print(f"• Memory Lattice: {status['advanced_features']['memory_lattice']}")
                print(f"• Drift Detection: {status['advanced_features']['drift_detection']}")
                print(f"• Tool Making: {status['advanced_features']['tool_making']}")
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
                print(f"\n⚡ Catalyst Integration Protocol (CIP v1) Status:")
                print(f"• Status: {cip_status['catalyst_status']}")
                print(f"• Orbit Stability: {cip_status['orbit_stability']:.2f}")
                print(f"• Reciprocity Ratio: {cip_status['reciprocity_metrics']['ratio']:.2f}")
                print(f"• Containment Score: {cip_status['containment_metrics']['score']:.2f}")
                print(f"• Elevation Eligible: {cip_status['elevation']['eligible']}")
            elif user_input.startswith('cip_pair '):
                stabilizer = user_input.split(' ', 1)[1]
                result = agi.pair_catalyst_with_stabilizer(stabilizer)
                print(f"\n🔗 Catalyst Pairing Result: {result}")
            elif user_input.lower() == 'cip_elevate':
                result = agi.elevate_catalyst()
                print(f"\n🚀 Catalyst Elevation Result: {result}")
            elif user_input.lower() == 'history':
                history = agi.get_selection_history()
                print(f"\n📊 Selection History ({len(history)} interactions):")
                for i, entry in enumerate(history[-5:], 1):  # Show last 5
                    print(f"{i}. {entry['interaction_type']} ({entry['data_context']}) - Complexity: {entry['complexity_level']:.2f}")
            elif user_input.lower() == 'preferences':
                preferences = agi.get_learned_preferences()
                print(f"\n🎯 Learned Preferences ({len(preferences)} patterns):")
                for pattern, score in list(preferences.items())[:5]:  # Show top 5
                    print(f"• {pattern}: {score:.3f}")
            elif user_input.lower() == 'reset':
                agi.reset_learned_preferences()
                print(f"\n🔄 Learned preferences reset")
            else:
                # Process user input with advanced features
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
    
    # Shutdown
    agi.shutdown()
    print("\n👋 Advanced system session ended. Goodbye!")

if __name__ == "__main__":
    main()

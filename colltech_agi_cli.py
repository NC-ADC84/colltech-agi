#!/usr/bin/env python3
"""
CollTech-AGI Command Line Interface
"""

import sys
import argparse
from pathlib import Path

# Add AgenticMindsets to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'AgenticMindsets'))

try:
    from src.agentic_mindsets_integration import (
        AgenticMindsetsIntegration,
        AgenticConfig,
        AgenticMode
    )
    from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure CollTech-AGI is properly installed.")
    sys.exit(1)


def interactive_mode():
    """Run CollTech-AGI in interactive mode"""
    print("="*70)
    print("CollTech-AGI Interactive Mode")
    print("="*70)
    print("\nInitializing systems...")
    
    # Initialize systems
    agentic = AgenticMindsetsIntegration()
    personality = PersonalitySystem()
    
    print("✅ Systems initialized!")
    print("\nAvailable personalities: rho, lyra, nyx")
    print("Available modes: stable, transcendent, evolutionary, hierarchical, conscious")
    print("Type 'quit' to exit, 'help' for commands\n")
    
    current_personality = "lyra"
    current_mode = AgenticMode.CONSCIOUS
    
    while True:
        try:
            user_input = input(f"[{current_personality}|{current_mode.value}] > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
                
            if user_input.lower() == 'help':
                print("\nCommands:")
                print("  /personality <rho|lyra|nyx> - Change personality")
                print("  /mode <stable|transcendent|evolutionary|hierarchical|conscious> - Change mode")
                print("  /status - Show system status")
                print("  /reset - Reset system state")
                print("  quit - Exit")
                print()
                continue
                
            if user_input.startswith('/personality '):
                new_personality = user_input.split()[1].lower()
                if new_personality in ['rho', 'lyra', 'nyx']:
                    current_personality = new_personality
                    personality.set_profile(PersonalityProfile(new_personality))
                    print(f"✅ Personality changed to: {new_personality}")
                else:
                    print("❌ Invalid personality. Choose: rho, lyra, nyx")
                continue
                
            if user_input.startswith('/mode '):
                new_mode = user_input.split()[1].lower()
                try:
                    current_mode = AgenticMode(new_mode)
                    agentic.set_mode(current_mode)
                    print(f"✅ Mode changed to: {new_mode}")
                except ValueError:
                    print("❌ Invalid mode. Choose: stable, transcendent, evolutionary, hierarchical, conscious")
                continue
                
            if user_input == '/status':
                status = agentic.get_integration_status()
                print(f"\nSystem Status:")
                print(f"  Current Mode: {status['current_mode']}")
                print(f"  Total Interactions: {status['total_interactions']}")
                print(f"  Transcendence Events: {status['transcendence_events']}")
                print(f"  Evolution Generations: {status['evolution_generations']}")
                print(f"  Active Systems: {', '.join(status['active_systems'])}")
                print()
                continue
                
            if user_input == '/reset':
                agentic.reset_state()
                print("✅ System state reset")
                continue
            
            # Process input
            result = agentic.process_with_agentic_mindset(
                user_input,
                mode=current_mode
            )
            
            # Generate response with personality
            response = personality.generate_response(user_input)
            
            print(f"\n{response}\n")
            
            # Show metadata if verbose
            if result['agentic_metadata']:
                print(f"[Transformations: {', '.join(result['transformations_applied'])}]")
                if 'consciousness' in result['agentic_metadata']:
                    consciousness = result['agentic_metadata']['consciousness']
                    print(f"[Meaning: {consciousness.get('meaning_score', 0):.2f}]")
                print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


def batch_mode(input_file, output_file, personality, mode):
    """Process inputs from file"""
    print(f"Processing {input_file} in batch mode...")
    
    agentic = AgenticMindsetsIntegration()
    personality_system = PersonalitySystem()
    personality_system.set_profile(PersonalityProfile(personality))
    
    try:
        with open(input_file, 'r') as f:
            inputs = f.readlines()
        
        results = []
        for i, user_input in enumerate(inputs, 1):
            user_input = user_input.strip()
            if not user_input:
                continue
                
            print(f"Processing {i}/{len(inputs)}: {user_input[:50]}...")
            
            result = agentic.process_with_agentic_mindset(
                user_input,
                mode=AgenticMode(mode)
            )
            
            response = personality_system.generate_response(user_input)
            
            results.append({
                'input': user_input,
                'response': response,
                'metadata': result['agentic_metadata']
            })
        
        # Write results
        with open(output_file, 'w') as f:
            import json
            json.dump(results, f, indent=2)
        
        print(f"✅ Results written to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CollTech-AGI with Agentic Mindsets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  colltech-agi                          # Interactive mode
  colltech-agi --batch input.txt        # Batch processing
  colltech-agi --version                # Show version
        """
    )
    
    parser.add_argument('--version', action='version', version='CollTech-AGI 1.0.0')
    parser.add_argument('--batch', metavar='INPUT', help='Batch mode: process inputs from file')
    parser.add_argument('--output', metavar='OUTPUT', default='output.json', help='Output file for batch mode')
    parser.add_argument('--personality', choices=['rho', 'lyra', 'nyx'], default='lyra', help='Personality to use')
    parser.add_argument('--mode', choices=['stable', 'transcendent', 'evolutionary', 'hierarchical', 'conscious'], 
                       default='conscious', help='Agentic mode to use')
    
    args = parser.parse_args()
    
    if args.batch:
        batch_mode(args.batch, args.output, args.personality, args.mode)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()

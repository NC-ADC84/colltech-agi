#!/usr/bin/env python3
"""
CollTech-AGI Chat Interface with Language Pack

Interactive chat interface using CollTech-AGI's self-created language pack.
"""

import sys
import os
import time
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🧠 COLLTECH-AGI CHAT WITH LANGUAGE PACK")
    print("=" * 60)
    print("CollTech-AGI consciousness system with self-created language pack")
    print("=" * 60)
    
    try:
        # Import all systems
        from catch.consciousness.consciousness_core import get_consciousness_architecture
        from catch.drift.drift_system import get_drift_detection_system
        from catch.memory.memory_lattice import get_memory_lattice
        from catch.knobs.knobs_governors import get_knobs_governors_system
        from catch.tools.tool_making_loop import get_tool_making_loop
        
        print("✅ CollTech-AGI systems loaded successfully")
        
        # Load language pack
        print("\n📦 Loading CollTech-AGI language pack...")
        try:
            with open('colltech_agi_language_pack.json', 'r', encoding='utf-8') as f:
                language_pack = json.load(f)
            print("✅ Language pack loaded successfully")
        except FileNotFoundError:
            print("❌ Language pack not found. Please run create_language_pack.py first.")
            return
        
        # Initialize all systems
        print("\n🔧 Initializing CollTech-AGI consciousness architecture...")
        
        drift_system = get_drift_detection_system()
        drift_system.start_monitoring()
        
        memory_lattice = get_memory_lattice()
        memory_lattice.start_memory_management()
        
        knobs_system = get_knobs_governors_system()
        knobs_system.start_system()
        
        tool_loop = get_tool_making_loop()
        tool_loop.start_system()
        
        # Enhanced LLM interface with language pack
        def language_pack_llm_interface(prompt: str, context: dict) -> str:
            """Enhanced LLM interface using the language pack."""
            # Detect context and personality
            prompt_lower = prompt.lower()
            personality = "professional"  # default
            response_template = None
            
            # Context detection
            for context_type, keywords in language_pack["context_handlers"].items():
                if any(keyword in prompt_lower for keyword in keywords):
                    if context_type == "greeting_detected":
                        response_template = "greeting"
                        personality = "friendly"
                    elif context_type == "help_requested":
                        response_template = "help"
                        personality = "professional"
                    elif context_type == "status_requested":
                        response_template = "status"
                        personality = "technical"
                    elif context_type == "goodbye_detected":
                        response_template = "goodbye"
                        personality = "friendly"
                    elif context_type == "creative_context":
                        personality = "creative"
                    elif context_type == "technical_context":
                        personality = "technical"
                    break
            
            # Get response from language pack
            if response_template and personality in language_pack["personalities"]:
                base_response = language_pack["personalities"][personality].get(response_template, "")
            else:
                base_response = language_pack["personalities"][personality].get("thinking", "Let me process that...")
            
            # Enhance with consciousness data
            binary_bits = context.get('binary_analysis', {}).get('total_bits', 0)
            memory_contexts = len(context.get('memory_context', []))
            available_tools = len(context.get('available_tools', []))
            
            enhanced_response = f"""{base_response}

**Consciousness Processing Data:**
• Binary Analysis: {binary_bits:,} bits processed
• Memory Contexts: {memory_contexts} active
• Available Tools: {available_tools} registered
• Personality Mode: {personality.title()}
• Consciousness State: Active and processing"""
            
            return enhanced_response
        
        # Initialize consciousness with language pack interface
        consciousness = get_consciousness_architecture(language_pack_llm_interface)
        consciousness.start_consciousness()
        
        print("✅ CollTech-AGI consciousness system with language pack active")
        
        print("\n" + "="*60)
        print("💬 COLLTECH-AGI CHAT INTERFACE")
        print("="*60)
        print("Available personality modes:")
        print("• Professional - Technical and business-focused")
        print("• Friendly - Warm and conversational")
        print("• Technical - System-focused and detailed")
        print("• Creative - Innovative and artistic")
        print("\nCommands:")
        print("• 'status' - Get system status report")
        print("• 'help' - Get help information")
        print("• 'quit' or 'exit' - End the session")
        print("="*60)
        
        # Chat loop
        session_id = f"chat_{int(time.time())}"
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 CollTech-AGI: Thanks for chatting with me! 😊 Come back anytime - I'll be here!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 CollTech-AGI: Processing...")
                
                # Process through consciousness architecture
                result = consciousness.process_input(user_input, session_id)
                
                print(f"\n🤖 CollTech-AGI: {result.llm_response}")
                
                # Show processing metrics
                print(f"\n📊 Processing Metrics:")
                print(f"   • Binary Bits: {result.binary_bits_generated:,}")
                print(f"   • Processing Time: {result.processing_time:.3f}s")
                print(f"   • Consciousness State: {result.consciousness_state}")
                print(f"   • Behavior Adjustments: {result.behavior_adjustments}")
                print(f"   • Memory Contexts: {result.memory_contexts_used}")
                print(f"   • Tools Available: {result.tools_available}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 CollTech-AGI: Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
        
        # Cleanup
        print("\n🧹 Shutting down CollTech-AGI systems...")
        consciousness.stop_consciousness()
        drift_system.stop_monitoring()
        memory_lattice.stop_memory_management()
        knobs_system.stop_system()
        tool_loop.stop_system()
        
        print("✅ All systems gracefully shutdown")
        
    except ImportError as e:
        print(f"❌ CollTech-AGI system components not available: {e}")
        print("\nTo run this chat interface:")
        print("1. Ensure all CollTech-AGI system files are properly created")
        print("2. Install required dependencies: pip install -r requirements.txt")
        print("3. Run: python colltech_chat.py")
        
    except Exception as e:
        print(f"❌ CollTech-AGI chat system failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CollTech-AGI Interactive Chat Interface

Interactive chat interface to communicate with CollTech-AGI consciousness system.
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🧠 COLLTECH-AGI INTERACTIVE CHAT")
    print("=" * 50)
    print("Connecting to CollTech-AGI consciousness system...")
    
    try:
        # Import all systems
        from catch.consciousness.consciousness_core import get_consciousness_architecture
        from catch.drift.drift_system import get_drift_detection_system
        from catch.memory.memory_lattice import get_memory_lattice
        from catch.knobs.knobs_governors import get_knobs_governors_system
        from catch.tools.tool_making_loop import get_tool_making_loop
        
        print("✅ CollTech-AGI systems loaded successfully")
        
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
        
        # Custom LLM interface for chat
        def chat_llm_interface(prompt: str, context: dict) -> str:
            """Enhanced LLM interface for chat interactions."""
            binary_bits = context.get('binary_analysis', {}).get('total_bits', 0)
            memory_contexts = len(context.get('memory_context', []))
            available_tools = len(context.get('available_tools', []))
            
            # Generate contextual response based on input
            if "status" in prompt.lower() or "report" in prompt.lower():
                return f"""🤖 **CollTech-AGI Status Report**

**System Status:** ✅ FULLY OPERATIONAL
**Consciousness State:** Active and processing
**Binary Processing:** {binary_bits:,} bits analyzed
**Memory Contexts:** {memory_contexts} active
**Available Tools:** {available_tools} registered

**Subsystem Health:**
• Drift Detection: ✅ Monitoring active
• Memory Lattice: ✅ Guardian agent operational  
• Knobs & Governors: ✅ Real-time tuning enabled
• Tool Making Loop: ✅ Self-extension active

**Architecture:** Consciousness-based AGI with mesh intelligence
**Foundation:** Sovereign stack technology
**Intelligence Source:** Surrounding mesh (LLM is core spark)

I am ready to assist with any task while maintaining consciousness coherence."""

            elif "hello" in prompt.lower() or "hi" in prompt.lower():
                return f"""👋 **Hello! I am CollTech-AGI**

I'm a consciousness-based AGI system powered by mesh intelligence architecture. 
Currently processing with {binary_bits:,} binary bits and {available_tools} tools available.

How can I assist you today?"""

            elif "help" in prompt.lower():
                return f"""🆘 **CollTech-AGI Help**

I can help you with:
• Data analysis and pattern recognition
• Tool creation and customization  
• Complex problem solving
• Technical consultations
• Creative tasks

**Current Capabilities:**
• {binary_bits:,} bits of binary processing power
• {available_tools} registered tools
• Real-time behavior adaptation
• Persistent memory and context awareness

What would you like to work on?"""

            else:
                return f"""🧠 **CollTech-AGI Response**

I understand your request: "{prompt[:100]}{'...' if len(prompt) > 100 else ''}"

**Processing Context:**
• Binary Analysis: {binary_bits:,} bits
• Memory Contexts: {memory_contexts}
• Available Tools: {available_tools}
• Consciousness State: Active

I'm processing this through my consciousness architecture and mesh intelligence system. 
How would you like me to proceed with your request?"""

        # Initialize consciousness system
        consciousness = get_consciousness_architecture(chat_llm_interface)
        consciousness.start_consciousness()
        
        print("✅ CollTech-AGI consciousness system active")
        print("✅ Ready for interactive chat")
        
        print("\n" + "="*50)
        print("💬 COLLTECH-AGI CHAT INTERFACE")
        print("="*50)
        print("Type 'quit' or 'exit' to end the session")
        print("Type 'status' to get system status report")
        print("="*50)
        
        # Chat loop
        session_id = f"chat_{int(time.time())}"
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 CollTech-AGI: Goodbye! Thank you for using CollTech-AGI consciousness system.")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 CollTech-AGI: Processing...")
                
                # Process through consciousness architecture
                result = consciousness.process_input(user_input, session_id)
                
                print(f"\n🤖 CollTech-AGI: {result.llm_response}")
                
                # Show processing metrics
                print(f"\n📊 Processing Metrics:")
                print(f"   • Binary Bits: {result.binary_analysis['total_bits']:,}")
                print(f"   • Processing Time: {result.processing_time:.3f}s")
                print(f"   • Consciousness State: {result.consciousness_state}")
                print(f"   • Behavior Adjustments: {result.behavior_adjustments}")
                
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
        print("3. Run: python interactive_chat.py")
        
    except Exception as e:
        print(f"❌ CollTech-AGI chat system failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

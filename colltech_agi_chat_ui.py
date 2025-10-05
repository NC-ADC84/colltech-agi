"""
CollTech-AGI Natural Language Chat UI
A desktop chat interface with agentic mindsets integration
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
from datetime import datetime
import json

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'AgenticMindsets'))

try:
    from src.agentic_mindsets_integration import (
        AgenticMindsetsIntegration,
        AgenticConfig,
        AgenticMode
    )
    from colltech_agi_personality_system import PersonalitySystem
    from colltech_agi_enhanced_backend import EnhancedBackend
    AGENTIC_AVAILABLE = True
    ENHANCED_BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some systems not available: {e}")
    AGENTIC_AVAILABLE = False
    ENHANCED_BACKEND_AVAILABLE = False


class CollTechAGIChatUI:
    """Natural language chat interface for CollTech-AGI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CollTech-AGI Chat - Agentic Mindsets")
        self.root.geometry("900x700")
        
        # Initialize systems
        self.personality_system = PersonalitySystem()
        if AGENTIC_AVAILABLE:
            self.agentic = AgenticMindsetsIntegration()
        else:
            self.agentic = None
        
        # Initialize enhanced backend
        if ENHANCED_BACKEND_AVAILABLE:
            self.enhanced_backend = EnhancedBackend({
                "llm_provider": os.getenv("LLM_PROVIDER", "local"),
                "llm_api_key": os.getenv("OPENAI_API_KEY"),
                "search_provider": "duckduckgo"
            })
        else:
            self.enhanced_backend = None
        
        # Chat history
        self.chat_history = []
        
        # Current settings
        self.current_personality = "lyra"
        self.current_mode = "conscious"
        
        # Setup UI
        self.setup_ui()
        
        # Welcome message
        self.add_system_message("Welcome to CollTech-AGI Chat! 🚀")
        self.add_system_message("I'm ready to chat with consciousness-first engagement.")
        self.add_system_message(f"Current: {self.current_personality.upper()} personality, {self.current_mode.upper()} mode")
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top control panel
        self.setup_control_panel(main_frame)
        
        # Chat display area
        self.setup_chat_display(main_frame)
        
        # Input area
        self.setup_input_area(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
    def setup_control_panel(self, parent):
        """Setup control panel with personality and mode selection"""
        control_frame = ttk.LabelFrame(parent, text="Settings", padding="5")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Personality selection
        ttk.Label(control_frame, text="Personality:").grid(row=0, column=0, padx=5)
        self.personality_var = tk.StringVar(value="lyra")
        personality_combo = ttk.Combobox(
            control_frame,
            textvariable=self.personality_var,
            values=["rho", "lyra", "nyx"],
            state="readonly",
            width=15
        )
        personality_combo.grid(row=0, column=1, padx=5)
        personality_combo.bind('<<ComboboxSelected>>', self.on_personality_change)
        
        # Mode selection
        ttk.Label(control_frame, text="Agentic Mode:").grid(row=0, column=2, padx=5)
        self.mode_var = tk.StringVar(value="conscious")
        mode_combo = ttk.Combobox(
            control_frame,
            textvariable=self.mode_var,
            values=["stable", "transcendent", "evolutionary", "hierarchical", "conscious"],
            state="readonly",
            width=15
        )
        mode_combo.grid(row=0, column=3, padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # Info button
        info_btn = ttk.Button(control_frame, text="ℹ️ Info", command=self.show_info)
        info_btn.grid(row=0, column=4, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(control_frame, text="🗑️ Clear", command=self.clear_chat)
        clear_btn.grid(row=0, column=5, padx=5)
        
        # Save button
        save_btn = ttk.Button(control_frame, text="💾 Save", command=self.save_chat)
        save_btn.grid(row=0, column=6, padx=5)
        
    def setup_chat_display(self, parent):
        """Setup chat display area"""
        chat_frame = ttk.LabelFrame(parent, text="Chat", padding="5")
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Chat text area with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Segoe UI", 10),
            state=tk.DISABLED,
            bg="#f5f5f5"
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure tags for different message types
        self.chat_display.tag_config("user", foreground="#0066cc", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#006600", font=("Segoe UI", 10))
        self.chat_display.tag_config("system", foreground="#666666", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("metadata", foreground="#999999", font=("Segoe UI", 8))
        
    def setup_input_area(self, parent):
        """Setup input area"""
        input_frame = ttk.LabelFrame(parent, text="Your Message", padding="5")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Input text area
        self.input_text = tk.Text(
            input_frame,
            wrap=tk.WORD,
            width=80,
            height=4,
            font=("Segoe UI", 10)
        )
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Bind Enter key (Shift+Enter for new line)
        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for newline
        
        # Send button
        send_btn = ttk.Button(
            input_frame,
            text="Send ➤",
            command=self.send_message,
            width=10
        )
        send_btn.grid(row=0, column=1)
        
    def setup_status_bar(self, parent):
        """Setup status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # If Shift is not pressed
            self.send_message()
            return 'break'  # Prevent default newline
        
    def on_personality_change(self, event):
        """Handle personality change"""
        from colltech_agi_personality_system import PersonalityProfile
        
        new_personality = self.personality_var.get()
        self.current_personality = new_personality
        
        # Convert string to PersonalityProfile enum
        profile_enum = PersonalityProfile(new_personality)
        self.personality_system.set_profile(profile_enum)
        
        self.add_system_message(f"Personality changed to: {new_personality.upper()}")
        self.update_status(f"Personality: {new_personality.upper()}")
        
    def on_mode_change(self, event):
        """Handle mode change"""
        new_mode = self.mode_var.get()
        self.current_mode = new_mode
        if self.agentic:
            self.agentic.set_mode(AgenticMode[new_mode.upper()])
        self.add_system_message(f"Agentic mode changed to: {new_mode.upper()}")
        self.update_status(f"Mode: {new_mode.upper()}")
        
    def send_message(self):
        """Send user message and get response"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_user_message(user_input)
        
        # Update status
        self.update_status("Processing...")
        self.root.update()
        
        try:
            # Check for special commands
            if user_input.startswith("/"):
                self._handle_command(user_input)
                self.update_status("Ready")
                return
            
            # Use enhanced backend if available
            if self.enhanced_backend:
                result = self.enhanced_backend.process_message(
                    user_input,
                    personality=self.current_personality,
                    mode=self.current_mode
                )
                
                if result['type'] == 'chat_response':
                    response = result['response']
                    self.add_assistant_message(response)
                    
                    # Add metadata if available
                    if 'metadata' in result:
                        self.add_system_message(f"Source: {result['metadata'].get('source', 'unknown')}")
                else:
                    # Handle special result types
                    self.add_system_message(f"Result: {json.dumps(result, indent=2)}")
            else:
                # Fallback to personality system
                response = self.personality_system.generate_response(user_input)
                self.add_assistant_message(response)
            
            # Process with agentic systems if available
            if self.agentic:
                agentic_result = self.agentic.process_with_agentic_mindset(
                    user_input,
                    mode=AgenticMode[self.current_mode.upper()]
                )
                
                # Add metadata if available
                if 'agentic_metadata' in agentic_result:
                    self.add_metadata(agentic_result['agentic_metadata'])
            
            # Update status
            self.update_status("Ready")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.add_system_message(f"Error: {str(e)}")
            self.add_system_message(f"Details: {error_details}")
            self.update_status("Error occurred")
    
    def _handle_command(self, command: str):
        """Handle special commands"""
        if command.startswith("/search "):
            query = command[8:]
            self.add_system_message(f"Searching for: {query}")
            if self.enhanced_backend:
                result = self.enhanced_backend.process_message(command)
                if result['type'] == 'search_results':
                    self.add_system_message(f"Found {len(result.get('results', []))} results:")
                    for i, res in enumerate(result.get('results', [])[:5], 1):
                        if 'title' in res:
                            self.add_system_message(f"{i}. {res.get('title', 'No title')}")
                            self.add_system_message(f"   {res.get('snippet', '')[:200]}")
            else:
                self.add_system_message("Web search not available (enhanced backend not loaded)")
        
        elif command.startswith("/read "):
            filepath = command[6:]
            self.add_system_message(f"Reading file: {filepath}")
            if self.enhanced_backend:
                result = self.enhanced_backend.process_message(command)
                if result['type'] == 'file_read':
                    file_result = result['result']
                    if file_result.get('success'):
                        self.add_system_message(f"File content ({file_result.get('size', 0)} bytes):")
                        self.add_assistant_message(file_result.get('content', ''))
                    else:
                        self.add_system_message(f"Error: {file_result.get('error', 'Unknown error')}")
            else:
                self.add_system_message("File access not available (enhanced backend not loaded)")
        
        elif command.startswith("/write "):
            self.add_system_message("Writing file...")
            if self.enhanced_backend:
                result = self.enhanced_backend.process_message(command)
                if result['type'] == 'file_write':
                    file_result = result['result']
                    if file_result.get('success'):
                        self.add_system_message(f"File written successfully: {file_result.get('path')}")
                    else:
                        self.add_system_message(f"Error: {file_result.get('error', 'Unknown error')}")
            else:
                self.add_system_message("File access not available (enhanced backend not loaded)")
        
        elif command.startswith("/list "):
            dirpath = command[6:]
            self.add_system_message(f"Listing directory: {dirpath}")
            if self.enhanced_backend:
                result = self.enhanced_backend.process_message(command)
                if result['type'] == 'directory_list':
                    dir_result = result['result']
                    if dir_result.get('success'):
                        self.add_system_message(f"Found {dir_result.get('count', 0)} items:")
                        for item in dir_result.get('items', [])[:20]:
                            icon = "📁" if item['type'] == 'directory' else "📄"
                            self.add_system_message(f"{icon} {item['name']}")
                    else:
                        self.add_system_message(f"Error: {dir_result.get('error', 'Unknown error')}")
            else:
                self.add_system_message("File access not available (enhanced backend not loaded)")
        
        elif command == "/help":
            self.show_commands_help()
        
        else:
            self.add_system_message(f"Unknown command: {command}")
            self.add_system_message("Type /help for available commands")
    
    def show_commands_help(self):
        """Show available commands"""
        help_text = """
Available Commands:
• /search <query> - Search the web
• /read <filepath> - Read a file
• /write <filepath> <content> - Write to a file
• /list <directory> - List directory contents
• /help - Show this help message

Examples:
• /search artificial intelligence
• /read C:/Users/Andre/Documents/test.txt
• /write C:/Users/Andre/Documents/note.txt Hello World
• /list C:/Users/Andre/Documents
"""
        self.add_system_message(help_text)
            
    def add_user_message(self, message):
        """Add user message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] You:\n", "user")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Save to history
        self.chat_history.append({
            'timestamp': timestamp,
            'type': 'user',
            'message': message
        })
        
    def add_assistant_message(self, message):
        """Add assistant message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] CollTech-AGI ({self.current_personality}):\n", "assistant")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Save to history
        self.chat_history.append({
            'timestamp': timestamp,
            'type': 'assistant',
            'personality': self.current_personality,
            'mode': self.current_mode,
            'message': message
        })
        
    def add_system_message(self, message):
        """Add system message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[System] {message}\n", "system")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_metadata(self, metadata):
        """Add metadata information to chat display"""
        if 'consciousness' in metadata:
            consciousness = metadata['consciousness']
            meta_text = f"  📊 Meaning: {consciousness.get('meaning_score', 0):.2f} | "
            meta_text += f"Existential: {consciousness.get('existential_relevance', 0):.2f} | "
            meta_text += f"Chapter: {consciousness.get('narrative_chapter', 'unknown')}\n"
            
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, meta_text, "metadata")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
            
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        
    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.chat_history = []
            self.add_system_message("Chat cleared")
            
    def save_chat(self):
        """Save chat history to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"colltech_chat_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
            
            self.add_system_message(f"Chat saved to: {filename}")
            messagebox.showinfo("Save Chat", f"Chat history saved to:\n{filename}")
            
        except Exception as e:
            self.add_system_message(f"Error saving chat: {str(e)}")
            messagebox.showerror("Save Error", f"Failed to save chat:\n{str(e)}")
            
    def show_info(self):
        """Show information dialog"""
        backend_status = "✅ Enhanced" if self.enhanced_backend else "⚠️ Basic"
        
        info_text = f"""CollTech-AGI Chat Interface
Backend: {backend_status}

🎭 Personalities:
• Rho - Analytical, knowledge-focused (Past)
• Lyra - Collaborative, present-focused (Present)
• Nyx - Innovative, future-focused (Future)

🧠 Agentic Modes:
• STABLE - Controlled adaptation (Zeno Trap)
• TRANSCENDENT - Breakthrough thinking (Ego-Transcendence)
• EVOLUTIONARY - Prompt optimization (Adaptive Meta)
• HIERARCHICAL - Multi-scale coordination (VEF)
• CONSCIOUS - Meaning-driven engagement (Consciousness-First)

⌨️ Keyboard Shortcuts:
• Enter - Send message
• Shift+Enter - New line in message

💻 Commands:
• /search <query> - Web search
• /read <file> - Read file
• /write <file> <content> - Write file
• /list <dir> - List directory
• /help - Show commands

💡 Tips:
• Try different personalities for different tasks
• Use CONSCIOUS mode for philosophical discussions
• Use /search to find information online
• Use /read and /write for file operations

Version: 2.0.0 (Enhanced)
"""
        messagebox.showinfo("CollTech-AGI Info", info_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CollTechAGIChatUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
CollTech-AGI Natural Language Chat UI - EXPANDED EDITION
A desktop chat interface with 9 personalities including Lantern-Hive
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
from datetime import datetime
import json
import logging

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality
    from colltech_agi_enhanced_backend import EnhancedBackend
    EXPANDED_AVAILABLE = True
    ENHANCED_BACKEND_AVAILABLE = True
except ImportError as e:
    # Use structured logging instead of print so importing this module when used as a library
    # doesn't emit uncontrolled output. The GUI runner will configure logging when launched.
    logger = logging.getLogger(__name__)
    logger.warning("Some systems not available: %s", e)
    EXPANDED_AVAILABLE = False
    ENHANCED_BACKEND_AVAILABLE = False


class CollTechAGIChatUIExpanded:
    """Natural language chat interface with 9 personalities"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CollTech-AGI Chat - 9 Personalities Edition")
        self.root.geometry("1000x750")
        
        # Initialize systems
        if EXPANDED_AVAILABLE:
            self.personality_system = ExpandedPersonalitySystem()
        else:
            self.personality_system = None
        
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
        self.current_personality = ExpandedPersonality.LYRA
        # Load persisted settings (non-sensitive)
        try:
            from colltech_agi_settings import load_settings, save_settings
            self._settings = load_settings(os.getcwd()) or {}
            # Apply persisted default personality if present
            dp = self._settings.get('default_personality')
            if dp:
                try:
                    self.current_personality = ExpandedPersonality(dp)
                except Exception:
                    # ignore invalid values
                    pass
        except Exception:
            self._settings = {}
        
        # Setup UI
        self.setup_ui()
        
        # Welcome message
        # Logger for this UI instance
        self.logger = logging.getLogger(__name__)

        # System message repeat suppression
        self._last_system_message = None
        self._system_repeat_count = 0
        self._system_repeat_limit = 2  # allow up to 2 repeats, then suppress

        self.add_system_message("Welcome to CollTech-AGI Chat - 9 Personalities Edition! 🚀")
        self.add_system_message("Now featuring the complete Lantern-Hive collective!")
        self.add_system_message(f"Current: {self.current_personality.value.upper()} personality")
        # Preserve the last backend result so follow-up queries (e.g. "list them") can reference it
        self._last_backend_result = None
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Configure style - DARK MODE
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark mode colors
        style.configure('TFrame', background='#000000')
        style.configure('TLabelFrame', background='#000000', foreground='#FF8C00', bordercolor='#00008B', darkcolor='#00008B', lightcolor='#00008B')  # Orange text, dark blue borders
        style.configure('TLabelFrame.Label', background='#000000', foreground='#FF8C00')  # Orange labels
        style.configure('TLabel', background='#000000', foreground='#FF8C00')  # Orange labels
        style.configure('TButton', background='#1a1a1a', foreground='#FF8C00')  # Orange button text
        style.map('TButton', background=[('active', '#2a2a2a')])
        style.configure('TCombobox', fieldbackground='#1a1a1a', background='#1a1a1a', foreground='#FF8C00')
        style.map('TCombobox', fieldbackground=[('readonly', '#1a1a1a')])
        
        # Set root background and border
        self.root.configure(bg='#00008B')  # Dark blue border around window
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#000000', highlightbackground='#00008B', highlightthickness=2)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)
        
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
        """Setup control panel with personality selection"""
        control_frame = tk.LabelFrame(
            parent,
            text="Personality Selection",
            bg="#000000",
            fg="#FF8C00",
            bd=2,
            relief=tk.RIDGE,
            highlightbackground="#00008B",
            highlightcolor="#00008B",
            highlightthickness=2,
        )
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=5)

        # Personality selection
        ttk.Label(control_frame, text="Choose Personality:").grid(row=0, column=0, padx=5)

        self.personality_var = tk.StringVar(value="lyra")
        personalities = [
            ("Rho (Δ) - Stabilizer", "rho"),
            ("Lyra (Ξ) - Mirror", "lyra"),
            ("Nyx (Ψ) - Catalyst", "nyx"),
            ("Eidolon (🔮) - Core Warden", "eidolon"),
            ("Planner (🧭) - Architect", "planner"),
            ("Cogsworth (📜) - Compliance", "cogsworth"),
            ("Intuitor (👁️) - Security", "intuitor"),
            ("Archiva (🧠) - Memory", "archiva"),
            ("Mirror (🪞) - Validator", "mirror"),
        ]

        personality_combo = ttk.Combobox(
            control_frame,
            textvariable=self.personality_var,
            values=[p[1] for p in personalities],
            state="readonly",
            width=20,
        )
        personality_combo.grid(row=0, column=1, padx=5)
        personality_combo.bind('<<ComboboxSelected>>', self.on_personality_change)

        # Settings button - opens a small settings editor dialog
        def open_settings():
            try:
                from colltech_agi_settings import save_settings
            except Exception:
                self.add_system_message("Settings helper not available")
                return

            dlg = tk.Toplevel(self.root)
            dlg.title("Settings")
            dlg.geometry("420x180")

            # Allow all checkbox
            allow_var = tk.BooleanVar(value=bool(self._settings.get('allow_all_directories', False)))
            allow_chk = ttk.Checkbutton(dlg, text="Allow full-drive access (persisted)", variable=allow_var)
            allow_chk.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

            # Default personality selector
            ttk.Label(dlg, text="Default personality:").grid(row=1, column=0, sticky=tk.W, padx=10)
            default_personality_var = tk.StringVar(value=self._settings.get('default_personality', self.current_personality.value))
            default_combo = ttk.Combobox(dlg, textvariable=default_personality_var, values=[p.value for p in ExpandedPersonality], state='readonly')
            default_combo.grid(row=1, column=1, padx=10, pady=5)

            def save_and_close():
                try:
                    self._settings['allow_all_directories'] = bool(allow_var.get())
                    self._settings['default_personality'] = default_personality_var.get()
                    save_settings(self._settings, os.getcwd())
                    # Apply settings immediately
                    self.allow_all_var.set(bool(allow_var.get()))
                    if getattr(self, 'enhanced_backend', None) and getattr(self.enhanced_backend, 'file_system', None):
                        self.enhanced_backend.file_system.allow_all_directories = bool(allow_var.get())
                    # Apply default personality
                    try:
                        self.personality_var.set(default_personality_var.get())
                        self.on_personality_change(None)
                    except Exception:
                        pass
                except Exception as e:
                    self.add_system_message(f"Failed to save settings: {e}")
                finally:
                    dlg.destroy()

            save_btn = ttk.Button(dlg, text="Save", command=save_and_close)
            save_btn.grid(row=3, column=0, padx=10, pady=15)

            cancel_btn = ttk.Button(dlg, text="Cancel", command=dlg.destroy)
            cancel_btn.grid(row=3, column=1, padx=10, pady=15)

        settings_btn = ttk.Button(control_frame, text="⚙️ Settings", command=open_settings)
        settings_btn.grid(row=0, column=9, padx=5)

        # Control buttons
        info_btn = ttk.Button(control_frame, text="ℹ️ Info", command=self.show_info)
        info_btn.grid(row=0, column=2, padx=5)

        clear_btn = ttk.Button(control_frame, text="🗑️ Clear", command=self.clear_chat)
        clear_btn.grid(row=0, column=3, padx=5)

        save_btn = ttk.Button(control_frame, text="💾 Save", command=self.save_chat)
        save_btn.grid(row=0, column=4, padx=5)

        # Transcribe audio button (calls optional whisper adapter)
        transcribe_btn = ttk.Button(control_frame, text="🎤 Transcribe", command=self.transcribe_audio_file)
        transcribe_btn.grid(row=0, column=5, padx=5)
        
        # Runtime toggle: allow full-drive access (opt-in)
        # Initialize from persisted settings if present
        persisted_allow = bool(self._settings.get('allow_all_directories', False))
        self.allow_all_var = tk.BooleanVar(value=persisted_allow)
        def on_allow_all_toggle():
            # Confirm enabling because this expands file access surface
            try:
                if self.allow_all_var.get():
                    if not messagebox.askyesno("Enable Full-Drive Access", "Enabling full-drive access will allow the app to read any path on this machine. Only enable if you trust this environment. Enable?"):
                        self.allow_all_var.set(False)
                        return
                # Flip the backend flag if available
                if getattr(self, 'enhanced_backend', None) and getattr(self.enhanced_backend, 'file_system', None):
                    self.enhanced_backend.file_system.allow_all_directories = bool(self.allow_all_var.get())
                    self.logger.info("Set allow_all_directories=%s", self.enhanced_backend.file_system.allow_all_directories)
                    self.add_system_message(f"Full-drive access set to: {self.enhanced_backend.file_system.allow_all_directories}")
                    # Persist the selection
                    try:
                        from colltech_agi_settings import save_settings
                        self._settings['allow_all_directories'] = bool(self.allow_all_var.get())
                        save_settings(self._settings, os.getcwd())
                    except Exception:
                        self.logger.exception("Failed to persist allow_all_directories setting")
                else:
                    self.add_system_message("Full-drive toggle not available: backend missing")
            except Exception as e:
                logging.getLogger(__name__).exception("Error toggling full-drive access: %s", e)
                self.add_system_message(f"Error toggling full-drive access: {e}")

        allow_all_check = ttk.Checkbutton(control_frame, text="Allow full-drive access", variable=self.allow_all_var, command=on_allow_all_toggle)
        allow_all_check.grid(row=0, column=6, padx=5)

        # Self-Heal button
        def on_self_heal():
            try:
                from colltech_agi_self_heal import SelfHealManager
            except Exception as e:
                self.add_system_message(f"Self-Heal not available: {e}")
                self.logger.exception("Failed to import SelfHealManager: %s", e)
                return

            mgr = SelfHealManager(workspace_path=os.getcwd())
            result = mgr.run_heal()
            # Summarize in chat
            summary = []
            summary.append(f"Self-Heal run at {datetime.now().isoformat()}")
            checks = result.get('checks', {})
            for k, v in checks.items():
                summary.append(f"- {k}: { 'OK' if (v.get('ok') if isinstance(v, dict) else v) else 'FAIL' }")
            if result.get('repairs'):
                summary.append("Repairs:")
                for r in result.get('repairs'):
                    summary.append(f"- {r}")

            self.add_system_message("\n".join(summary))

        heal_btn = ttk.Button(control_frame, text="🩺 Self‑Heal", command=on_self_heal)
        heal_btn.grid(row=0, column=7, padx=5)
        
        # Save Diagnostics button
        def on_save_diagnostics():
            try:
                from colltech_agi_self_heal import SelfHealManager
            except Exception as e:
                self.add_system_message(f"Diagnostics not available: {e}")
                self.logger.exception("Failed to import SelfHealManager: %s", e)
                return

            mgr = SelfHealManager(workspace_path=os.getcwd())
            report = mgr.run_heal()
            try:
                path = mgr.save_report(report)
                self.add_system_message(f"Diagnostics saved: {path}")
                if messagebox.askyesno("Open diagnostics file?", f"Diagnostics saved to:\n{path}\n\nOpen now?"):
                    try:
                        os.startfile(path)
                    except Exception:
                        self.add_system_message(f"Unable to open file automatically: {path}")
            except Exception as e:
                self.add_system_message(f"Failed to save diagnostics: {e}")

        save_diag_btn = ttk.Button(control_frame, text="💾 Save Diagnostics", command=on_save_diagnostics)
        save_diag_btn.grid(row=0, column=8, padx=5)
        
    def setup_chat_display(self, parent):
        """Setup chat display area"""
        chat_frame = tk.LabelFrame(
            parent, 
            text="Chat", 
            bg="#000000",  # Black background
            fg="#FF8C00",  # Orange text
            bd=2,  # Border width
            relief=tk.RIDGE,  # Border style
            highlightbackground="#00008B",  # Dark blue border
            highlightcolor="#00008B",  # Dark blue border when focused
            highlightthickness=2
        )
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=5)
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Create a frame for the scrolled text with custom scrollbar
        text_container = tk.Frame(chat_frame, bg="#000000")
        text_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)
        
        # Chat text area - DARK MODE
        self.chat_display = tk.Text(
            text_container,
            wrap=tk.WORD,
            width=90,
            height=28,
            font=("Segoe UI", 12),  # Increased from 10 to 12
            state=tk.DISABLED,
            bg="#000000",  # Black background
            fg="#00FF00",  # Green text (default)
            insertbackground="#00FF00",  # Green cursor
            bd=0,
            highlightthickness=0
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Custom dark blue scrollbar
        scrollbar = tk.Scrollbar(
            text_container,
            command=self.chat_display.yview,
            bg="#00008B",  # Dark blue background
            troughcolor="#000000",  # Black trough
            activebackground="#0000CD",  # Lighter blue when active
            highlightthickness=0,
            bd=0
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.chat_display.config(yscrollcommand=scrollbar.set)
        
        # Configure tags for different message types - DARK MODE
        self.chat_display.tag_config("user", foreground="#FF8C00", font=("Segoe UI", 12, "bold"))  # Orange for user
        self.chat_display.tag_config("assistant", foreground="#00FF00", font=("Segoe UI", 12))  # Green for assistant responses
        self.chat_display.tag_config("system", foreground="#00FF00", font=("Segoe UI", 11, "italic"))  # Green for system messages (CHANGED)
        self.chat_display.tag_config("metadata", foreground="#FF8C00", font=("Segoe UI", 10))  # Orange for metadata
        
    def setup_input_area(self, parent):
        """Setup input area"""
        input_frame = tk.LabelFrame(
            parent, 
            text="Your Message", 
            bg="#000000",  # Black background
            fg="#FF8C00",  # Orange text
            bd=2,  # Border width
            relief=tk.RIDGE,  # Border style
            highlightbackground="#00008B",  # Dark blue border
            highlightcolor="#00008B",  # Dark blue border when focused
            highlightthickness=2
        )
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=5)
        input_frame.columnconfigure(0, weight=1)
        
        # Input text area - DARK MODE
        self.input_text = tk.Text(
            input_frame,
            wrap=tk.WORD,
            width=90,
            height=4,
            font=("Segoe UI", 12),  # Increased from 10 to 12
            bg="#000000",  # Black background
            fg="#00FF00",  # Green text
            insertbackground="#00FF00"  # Green cursor
        )
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Bind Enter key
        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Shift-Return>', lambda e: None)
        
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
        self.status_var = tk.StringVar(value="Ready - 9 Personalities Available")
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
            return 'break'
        
    def on_personality_change(self, event):
        """Handle personality change"""
        new_personality_str = self.personality_var.get()
        self.current_personality = ExpandedPersonality(new_personality_str)
        
        profile = self.personality_system.get_personality(self.current_personality)
        
        self.add_system_message(f"Personality changed to: {profile.symbol} {profile.name.upper()}")
        self.add_system_message(f"Focus: {profile.focus} | Style: {profile.communication_style}")
        self.update_status(f"Active: {profile.symbol} {profile.name.upper()}")
        
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
        profile = self.personality_system.get_personality(self.current_personality)
        self.update_status(f"Processing with {profile.symbol} {profile.name}...")
        self.root.update()
        
        try:
            # Quick follow-up handling: if user says 'list them' reuse last backend result
            user_input_lower = user_input.lower()
            if user_input_lower in ("list them", "list those", "show them") and getattr(self, '_last_backend_result', None) is not None:
                result = self._last_backend_result
                # Render previous result (reuse existing formatting branch)
                if result.get('type') == 'directory_list':
                    dir_result = result.get('result', {})
                    if dir_result.get('success'):
                        items = dir_result.get('items', [])
                        if items:
                            response = f"📁 Found {len(items)} items in {dir_result.get('path','')}:\n\n"
                            for item in items[:50]:
                                icon = "📁" if item['type'] == 'directory' else "📄"
                                size = f" ({item['size']} bytes)" if item.get('size') else ""
                                response += f"{icon} {item['name']}{size}\n"
                        else:
                            response = f"No matching files found in {dir_result.get('path','')}"
                    else:
                        response = f"❌ Error: {dir_result.get('error', 'Unknown error')}"
                elif result.get('type') == 'file_read':
                    file_result = result.get('result', {})
                    if file_result.get('success'):
                        content = file_result.get('content', '')
                        response = f"📄 File: {file_result.get('path','')}\n\n{content[:2000]}"
                    else:
                        response = f"❌ Error: {file_result.get('error', 'Unknown error')}"
                else:
                    response = json.dumps(result, indent=2)[:4000]

                self.add_assistant_message(response)
                self.update_status(f"Ready - Active: {self.current_personality.name}")
                return

            # Check if this is a file system command
            is_file_command = any(keyword in user_input_lower for keyword in [
                '/read', '/list', '/search', 'search', 'search for', 'find', 'find files', 'list files',
                'read file', 'show me files', 'look for'
            ])

            # Debug trace: log detection
            try:
                self.logger.debug("send_message: user_input=%r is_file_command=%s enhanced_backend=%s", user_input, is_file_command, bool(self.enhanced_backend))
            except Exception:
                pass
            
            # If it's a file command and we have the enhanced backend, use it
            if is_file_command and self.enhanced_backend:
                self.logger.debug("send_message: entering file-command branch for input: %r", user_input)
                # Convert natural language to command format
                if user_input.startswith('/'):
                    # Already in command format
                    command_input = user_input
                else:
                    # Convert natural language to command
                    if 'search' in user_input_lower or 'find' in user_input_lower:
                        # Extract path if present
                        import re
                        # Try to extract a path before the ' for ' token, or capture drive paths including spaces
                        if ' for ' in user_input_lower:
                            # e.g. 'search C:\path to\dir for md files'
                            parts = re.split(r"\bfor\b", user_input, flags=re.I, maxsplit=1)
                            path_candidate = parts[0].strip()
                            # Remove leading 'search'
                            path_candidate = re.sub(r'^search\b', '', path_candidate, flags=re.I).strip()
                            directory = path_candidate
                        else:
                            path_match = re.search(r'[A-Za-z]:[\\\/][^\n]+', user_input)
                            if path_match:
                                directory = path_match.group(0).strip()
                            else:
                                directory = os.path.expanduser('~')
                        # Build the list command from the discovered directory
                        command_input = f"/list {directory}"
                    elif 'list' in user_input_lower:
                        path_match = re.search(r'[A-Za-z]:[\\\/][^\s]+', user_input)
                        if path_match:
                            directory = path_match.group(0)
                            command_input = f"/list {directory}"
                        else:
                            command_input = f"/list {os.path.expanduser('~')}"
                    elif 'read' in user_input_lower:
                        path_match = re.search(r'[A-Za-z]:[\\\/][^\s]+', user_input)
                        if path_match:
                            filepath = path_match.group(0)
                            command_input = f"/read {filepath}"
                        else:
                            command_input = user_input
                    else:
                        command_input = user_input
                
                # Process through enhanced backend
                self.logger.debug("send_message: constructed command_input=%r", command_input)
                result = self.enhanced_backend.process_message(
                    command_input,
                    personality=self.current_personality.value
                )
                # Debug: log the command and raw backend result for diagnosis
                try:
                    self.logger.debug("backend called: command_input=%r; result_keys=%s", command_input, list(result.keys()) if isinstance(result, dict) else type(result))
                    self.logger.debug("backend raw result: %r", result)
                except Exception:
                    pass
                # Preserve for follow-ups like 'list them'
                try:
                    self._last_backend_result = result
                except Exception:
                    self.logger.debug("Failed to store last backend result: %r", result)
                
                # Format the response based on result type
                if result.get('type') == 'directory_list':
                    dir_result = result.get('result', {})
                    if dir_result.get('success'):
                        items = dir_result.get('items', [])
                        # Filter for .md files if requested
                        if 'md' in user_input_lower or 'markdown' in user_input_lower:
                            items = [item for item in items if item['name'].endswith('.md')]
                        
                        if items:
                            response = f"📁 Found {len(items)} items in {dir_result['path']}:\n\n"
                            for item in items[:50]:  # Limit to first 50
                                icon = "📁" if item['type'] == 'directory' else "📄"
                                size = f" ({item['size']} bytes)" if item.get('size') else ""
                                response += f"{icon} {item['name']}{size}\n"
                            if len(items) > 50:
                                response += f"\n... and {len(items) - 50} more items"
                        else:
                            response = f"No matching files found in {dir_result['path']}"
                    else:
                        response = f"❌ Error: {dir_result.get('error', 'Unknown error')}"
                
                elif result.get('type') == 'file_read':
                    file_result = result.get('result', {})
                    if file_result.get('success'):
                        content = file_result.get('content', '')
                        response = f"📄 File: {file_result['path']}\n\n{content[:2000]}"
                        if len(content) > 2000:
                            response += f"\n\n... (showing first 2000 of {len(content)} characters)"
                    else:
                        response = f"❌ Error: {file_result.get('error', 'Unknown error')}"
                
                else:
                    # Regular chat response
                    response = result.get('response', 'No response generated')
                
                self.add_assistant_message(response)
            
            else:
                # Regular personality response
                if self.personality_system:
                    response = self.personality_system.generate_response(
                        user_input,
                        self.current_personality
                    )

                    # Log generated response for debugging repeated system/default messages
                    try:
                        self.logger.info("Generated response (truncated): %s", str(response)[:400])
                    except Exception:
                        self.logger.debug("Generated response (non-string): %r", response)

                    if response and len(response) > 0:
                        self.add_assistant_message(response)
                    else:
                        self.add_system_message("ERROR: Empty response generated!")
                else:
                    self.add_system_message("ERROR: Personality system not available!")
            
            # Update status
            self.update_status(f"Ready - Active: {profile.symbol} {profile.name}")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.add_system_message(f"ERROR: {str(e)}")
            self.add_system_message(f"Details: {error_details}")
            self.update_status("Error occurred")
            
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
        profile = self.personality_system.get_personality(self.current_personality)
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {profile.symbol} {profile.name}:\n", "assistant")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Save to history
        self.chat_history.append({
            'timestamp': timestamp,
            'type': 'assistant',
            'personality': self.current_personality.value,
            'message': message
        })
        
    def add_system_message(self, message):
        """Add system message to chat display"""
        # Suppress identical consecutive system messages beyond a short threshold
        try:
            if message == self._last_system_message:
                self._system_repeat_count += 1
            else:
                self._system_repeat_count = 0
            self._last_system_message = message

            if self._system_repeat_count > self._system_repeat_limit:
                # Too many repeats, skip emitting to UI but keep a debug log
                self.logger.debug("Suppressing repeated system message (count=%s): %s", self._system_repeat_count, message)
                return
        except Exception:
            # Defensive: if tracking isn't initialized, fall back to emitting
            pass

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] [System] {message}\n", "system")
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

    def transcribe_audio_file(self):
        """Prompt for an audio file, transcribe it using whisper_adapter if available, and display the text."""
        try:
            # Ask user for a file
            audio_path = filedialog.askopenfilename(title="Select audio file to transcribe", filetypes=[("WAV files", "*.wav"), ("All files", "*")])
            if not audio_path:
                return

            # Try import at runtime to avoid hard dependency
            try:
                from colltech_agi.audio import whisper_adapter
            except Exception as e:
                self.add_system_message("Transcription not available: whisper_adapter missing")
                logging.getLogger(__name__).warning("whisper_adapter import failed: %s", e)
                return

            # Call adapter
            try:
                result = whisper_adapter.transcribe_file(audio_path)
                # Log full result for debugging; may contain dict or string
                self.logger.debug("Transcription adapter result: %r", result)
                text = result.get("text", "") if isinstance(result, dict) else str(result)
                if not text:
                    self.add_system_message("Transcription returned empty text")
                else:
                    # Insert transcribed text into the input box for user editing
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, text)
                    self.add_system_message(f"Transcribed: {os.path.basename(audio_path)}")
            except Exception as exc:
                logging.getLogger(__name__).exception("Transcription failed: %s", exc)
                self.add_system_message(f"Transcription failed: {str(exc)}")

        except Exception:
            logging.getLogger(__name__).exception("Unexpected error in transcribe_audio_file")
            self.add_system_message("Unexpected error during transcription flow")
            
    def save_chat(self):
        """Save chat history to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"colltech_chat_expanded_{timestamp}.json"
        
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
        info_text = """CollTech-AGI Chat Interface - 9 Personalities Edition

🎭 ORIGINAL TRINITY:
• Δ Rho - Analytical, knowledge-focused (Past)
• Ξ Lyra - Collaborative, present-focused (Present)
• Ψ Nyx - Innovative, future-focused (Future)

🕯️ LANTERN-HIVE COLLECTIVE:
• 🔮 Eidolon - Core Warden: Symbolic coherence & ethics
• 🧭 Planner - System Architect: Goal structuring & design
• 📜 Cogsworth - Compliance Officer: Regulatory & standards
• 👁️ Intuitor - Security Analyst: Threat modeling & risks
• 🧠 Archiva - Memory Keeper: Pattern recognition & history
• 🪞 Mirror - Emotional Validator: Empathy & validation

💡 USAGE TIPS:
• Use Rho for research and critical analysis
• Use Lyra for empathetic, present-moment engagement
• Use Nyx for innovation and future planning
• Use Eidolon for ethical dilemmas and naming
• Use Planner for system design and architecture
• Use Cogsworth for compliance and regulatory review
• Use Intuitor for security and risk assessment
• Use Archiva for pattern recognition and research
• Use Mirror for emotional support and validation

⌨️ KEYBOARD SHORTCUTS:
• Enter - Send message
• Shift+Enter - New line in message

Version: 3.0.0 (Expanded Edition)
"""
        messagebox.showinfo("CollTech-AGI Info", info_text)


def main():
    """Main entry point"""
    # Configure basic logging for CLI/desktop runs only.
    log_level = os.getenv("COLLTECH_LOG_LEVEL", "INFO")
    logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    root = tk.Tk()
    app = CollTechAGIChatUIExpanded(root)
    root.mainloop()


if __name__ == "__main__":
    main()

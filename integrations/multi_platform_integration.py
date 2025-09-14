#!/usr/bin/env python3
"""
Multi-Platform Integration - CollTech-AGI Framework

This example shows how to integrate CollTech-AGI with multiple platforms
including Discord, web APIs, mobile apps, and desktop applications.
"""

import sys
import os
import asyncio
import json
import time
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

class MultiPlatformIntegration:
    """Multi-platform integration manager for CollTech-AGI."""
    
    def __init__(self):
        # Initialize CollTech-AGI
        config = FrameworkConfig(
            auto_personality_enabled=True,
            catalyst_integration_enabled=True,
            debug_mode=False
        )
        self.agi = CollTechAGIAdvanced(config)
        self.agi.start()
        
        # Platform configurations
        self.platforms = {
            "discord": {"enabled": False, "bot": None},
            "web_api": {"enabled": False, "app": None},
            "mobile": {"enabled": False, "client": None},
            "desktop": {"enabled": False, "app": None}
        }
        
        # Cross-platform data
        self.shared_context = {
            "user_sessions": {},
            "conversation_history": [],
            "platform_preferences": {}
        }
        
        print("✅ Multi-Platform Integration initialized")
    
    def process_cross_platform(self, user_input: str, platform: str, user_id: str = None, context: Dict[str, Any] = None):
        """Process input across multiple platforms."""
        # Store platform context
        if user_id:
            if user_id not in self.shared_context["user_sessions"]:
                self.shared_context["user_sessions"][user_id] = {
                    "platform": platform,
                    "interactions": 0,
                    "preferences": {}
                }
            
            self.shared_context["user_sessions"][user_id]["interactions"] += 1
        
        # Add platform context to input
        enhanced_input = f"[Platform: {platform}] {user_input}"
        if context:
            enhanced_input += f" [Context: {json.dumps(context)}]"
        
        # Process with CollTech-AGI
        result = self.agi.process_input(enhanced_input)
        
        # Add cross-platform metadata
        result["cross_platform"] = {
            "platform": platform,
            "user_id": user_id,
            "session_interactions": self.shared_context["user_sessions"].get(user_id, {}).get("interactions", 0),
            "timestamp": time.time()
        }
        
        # Store in conversation history
        self.shared_context["conversation_history"].append({
            "user_input": user_input,
            "response": result["response"],
            "platform": platform,
            "user_id": user_id,
            "timestamp": time.time()
        })
        
        return result
    
    def get_platform_status(self):
        """Get status of all platforms."""
        return {
            "platforms": self.platforms,
            "shared_context": {
                "active_users": len(self.shared_context["user_sessions"]),
                "conversation_count": len(self.shared_context["conversation_history"]),
                "platforms_active": [name for name, config in self.platforms.items() if config["enabled"]]
            }
        }
    
    def setup_discord_integration(self, bot_token: str):
        """Setup Discord integration."""
        try:
            import discord
            from discord.ext import commands
            
            # Create Discord bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            @bot.event
            async def on_ready():
                print(f"✅ Discord bot {bot.user} is online!")
                self.platforms["discord"]["enabled"] = True
            
            @bot.event
            async def on_message(message):
                if message.author == bot.user:
                    return
                
                # Process with CollTech-AGI
                result = self.process_cross_platform(
                    message.content,
                    "discord",
                    str(message.author.id),
                    {"guild_id": str(message.guild.id) if message.guild else None}
                )
                
                # Send response
                embed = discord.Embed(
                    title="🤖 CollTech-AGI Response",
                    description=result["response"],
                    color=0x00ff00
                )
                embed.add_field(
                    name="🎭 Personality",
                    value=result["personality"]["selected_profile"].title(),
                    inline=True
                )
                embed.add_field(
                    name="🧠 Confidence",
                    value=f"{result['personality']['confidence']:.2f}",
                    inline=True
                )
                
                await message.channel.send(embed=embed)
            
            self.platforms["discord"]["bot"] = bot
            print("✅ Discord integration setup complete")
            return bot
            
        except ImportError:
            print("❌ Discord.py not installed. Install with: pip install discord.py")
            return None
    
    def setup_web_api_integration(self, port: int = 8000):
        """Setup web API integration."""
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from pydantic import BaseModel
            import uvicorn
            
            # Create FastAPI app
            app = FastAPI(title="CollTech-AGI Multi-Platform API")
            
            # Add CORS middleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            class ChatRequest(BaseModel):
                message: str
                user_id: Optional[str] = None
                context: Optional[Dict[str, Any]] = None
            
            @app.post("/chat")
            async def chat(request: ChatRequest):
                result = self.process_cross_platform(
                    request.message,
                    "web_api",
                    request.user_id,
                    request.context
                )
                return result
            
            @app.get("/status")
            async def status():
                return self.get_platform_status()
            
            @app.get("/history")
            async def history():
                return self.shared_context["conversation_history"][-50:]  # Last 50 interactions
            
            self.platforms["web_api"]["app"] = app
            print("✅ Web API integration setup complete")
            return app
            
        except ImportError:
            print("❌ FastAPI not installed. Install with: pip install fastapi uvicorn")
            return None
    
    def setup_mobile_integration(self):
        """Setup mobile app integration."""
        # This would typically involve creating a mobile app
        # For this example, we'll create a simple client interface
        
        class MobileClient:
            def __init__(self, integration_manager):
                self.integration = integration_manager
                self.user_id = f"mobile_user_{int(time.time())}"
            
            def send_message(self, message: str, context: Dict[str, Any] = None):
                result = self.integration.process_cross_platform(
                    message,
                    "mobile",
                    self.user_id,
                    context
                )
                return result
            
            def get_conversation_history(self):
                return [
                    entry for entry in self.integration.shared_context["conversation_history"]
                    if entry["user_id"] == self.user_id
                ]
        
        mobile_client = MobileClient(self)
        self.platforms["mobile"]["client"] = mobile_client
        print("✅ Mobile integration setup complete")
        return mobile_client
    
    def setup_desktop_integration(self):
        """Setup desktop application integration."""
        # This would typically involve creating a desktop app
        # For this example, we'll create a simple GUI interface
        
        try:
            import tkinter as tk
            from tkinter import scrolledtext, messagebox
            
            class DesktopApp:
                def __init__(self, integration_manager):
                    self.integration = integration_manager
                    self.user_id = f"desktop_user_{int(time.time())}"
                    self.setup_gui()
                
                def setup_gui(self):
                    self.root = tk.Tk()
                    self.root.title("CollTech-AGI Desktop Client")
                    self.root.geometry("800x600")
                    
                    # Chat display
                    self.chat_display = scrolledtext.ScrolledText(
                        self.root, wrap=tk.WORD, state=tk.DISABLED
                    )
                    self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    
                    # Input frame
                    input_frame = tk.Frame(self.root)
                    input_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    self.input_entry = tk.Entry(input_frame)
                    self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.input_entry.bind('<Return>', self.send_message)
                    
                    send_button = tk.Button(input_frame, text="Send", command=self.send_message)
                    send_button.pack(side=tk.RIGHT, padx=(5, 0))
                    
                    # Status frame
                    status_frame = tk.Frame(self.root)
                    status_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    self.status_label = tk.Label(status_frame, text="Ready")
                    self.status_label.pack(side=tk.LEFT)
                
                def send_message(self, event=None):
                    message = self.input_entry.get().strip()
                    if not message:
                        return
                    
                    self.input_entry.delete(0, tk.END)
                    self.add_message("You", message)
                    
                    # Process with CollTech-AGI
                    try:
                        result = self.integration.process_cross_platform(
                            message,
                            "desktop",
                            self.user_id
                        )
                        
                        self.add_message(
                            f"CollTech-AGI ({result['personality']['selected_profile'].title()})",
                            result["response"]
                        )
                        
                        self.status_label.config(text=f"Last response: {result['personality']['selected_profile'].title()}")
                    
                    except Exception as e:
                        self.add_message("Error", str(e))
                
                def add_message(self, sender: str, message: str):
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
                    self.chat_display.config(state=tk.DISABLED)
                    self.chat_display.see(tk.END)
                
                def run(self):
                    self.root.mainloop()
            
            desktop_app = DesktopApp(self)
            self.platforms["desktop"]["app"] = desktop_app
            print("✅ Desktop integration setup complete")
            return desktop_app
            
        except ImportError:
            print("❌ Tkinter not available on this system")
            return None
    
    def run_web_api(self, port: int = 8000):
        """Run web API server."""
        if self.platforms["web_api"]["app"]:
            import uvicorn
            print(f"🚀 Starting web API server on port {port}")
            uvicorn.run(self.platforms["web_api"]["app"], host="0.0.0.0", port=port)
    
    def run_discord_bot(self, bot_token: str):
        """Run Discord bot."""
        if self.platforms["discord"]["bot"]:
            print("🚀 Starting Discord bot")
            self.platforms["discord"]["bot"].run(bot_token)
    
    def run_desktop_app(self):
        """Run desktop application."""
        if self.platforms["desktop"]["app"]:
            print("🚀 Starting desktop application")
            self.platforms["desktop"]["app"].run()
    
    def shutdown(self):
        """Shutdown all platforms."""
        self.agi.shutdown()
        print("✅ Multi-platform integration shutdown complete")

def main():
    """Main function to demonstrate multi-platform integration."""
    print("🌐 Multi-Platform Integration - CollTech-AGI Framework")
    print("=" * 60)
    print("This example demonstrates how to integrate CollTech-AGI")
    print("with multiple platforms including Discord, web APIs, mobile, and desktop.")
    print("=" * 60)
    
    # Initialize multi-platform integration
    integration = MultiPlatformIntegration()
    
    print("\n🔧 Setting up platform integrations:")
    print("-" * 40)
    
    # Setup web API
    web_app = integration.setup_web_api_integration()
    
    # Setup mobile client
    mobile_client = integration.setup_mobile_integration()
    
    # Setup desktop app
    desktop_app = integration.setup_desktop_integration()
    
    # Test cross-platform functionality
    print("\n💬 Testing cross-platform functionality:")
    print("-" * 40)
    
    # Test web API
    if web_app:
        result = integration.process_cross_platform(
            "Hello from web API!",
            "web_api",
            "web_user_123",
            {"source": "browser"}
        )
        print(f"Web API Response: {result['response'][:100]}...")
    
    # Test mobile
    if mobile_client:
        result = mobile_client.send_message(
            "Hello from mobile app!",
            {"device": "iPhone", "os": "iOS"}
        )
        print(f"Mobile Response: {result['response'][:100]}...")
    
    # Test desktop
    if desktop_app:
        result = integration.process_cross_platform(
            "Hello from desktop app!",
            "desktop",
            "desktop_user_456",
            {"app": "CollTech-AGI Desktop"}
        )
        print(f"Desktop Response: {result['response'][:100]}...")
    
    # Show platform status
    print("\n📊 Platform Status:")
    status = integration.get_platform_status()
    print(f"Active Users: {status['shared_context']['active_users']}")
    print(f"Conversation Count: {status['shared_context']['conversation_count']}")
    print(f"Platforms Active: {', '.join(status['shared_context']['platforms_active'])}")
    
    print("\n🎮 Interactive Multi-Platform Demo:")
    print("-" * 40)
    print("Commands:")
    print("• 'web' - Start web API server")
    print("• 'desktop' - Start desktop application")
    print("• 'status' - Show platform status")
    print("• 'history' - Show conversation history")
    print("• 'test <platform>' - Test specific platform")
    print("• 'quit' - Exit")
    
    # Interactive loop
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'web':
                if web_app:
                    print("🚀 Starting web API server...")
                    integration.run_web_api()
                else:
                    print("❌ Web API not available")
            elif user_input.lower() == 'desktop':
                if desktop_app:
                    print("🚀 Starting desktop application...")
                    integration.run_desktop_app()
                else:
                    print("❌ Desktop app not available")
            elif user_input.lower() == 'status':
                status = integration.get_platform_status()
                print(f"\n📊 Platform Status: {status}")
            elif user_input.lower() == 'history':
                history = integration.shared_context["conversation_history"]
                print(f"\n📚 Conversation History ({len(history)} entries):")
                for entry in history[-5:]:  # Show last 5
                    print(f"• [{entry['platform']}] {entry['user_input'][:50]}...")
            elif user_input.startswith('test '):
                platform = user_input.split(' ', 1)[1]
                if platform in ["web_api", "mobile", "desktop"]:
                    result = integration.process_cross_platform(
                        f"Test message from {platform}",
                        platform,
                        f"test_user_{platform}",
                        {"test": True}
                    )
                    print(f"\n✅ {platform.title()} Test Result:")
                    print(f"Response: {result['response']}")
                    print(f"Personality: {result['personality']['selected_profile'].title()}")
                else:
                    print(f"❌ Invalid platform. Use: web_api, mobile, desktop")
            else:
                # Process as general input
                result = integration.process_cross_platform(
                    user_input,
                    "console",
                    "console_user",
                    {"source": "command_line"}
                )
                print(f"\n🤖 CollTech-AGI: {result['response']}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Cleanup
    integration.shutdown()
    print("\n✅ Multi-platform integration demo complete!")

if __name__ == "__main__":
    main()

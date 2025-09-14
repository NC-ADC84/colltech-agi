#!/usr/bin/env python3
"""
Discord Bot Example - CollTech-AGI Framework

An example showing how to integrate CollTech-AGI with Discord
for personality-based chat interactions.
"""

import sys
import os
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ Discord.py not installed. Install with: pip install discord.py")
    sys.exit(1)

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

# Bot configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
BOT_PREFIX = "!"  # Bot command prefix

class CollTechAGIDiscordBot(commands.Bot):
    """Discord bot with CollTech-AGI integration."""
    
    def __init__(self):
        # Set up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=intents,
            description="CollTech-AGI Discord Bot with Personality System"
        )
        
        # Initialize CollTech-AGI
        config = FrameworkConfig(
            auto_personality_enabled=True,
            catalyst_integration_enabled=True,
            debug_mode=False
        )
        self.agi = CollTechAGIAdvanced(config)
        self.agi.start()
        
        print("🤖 CollTech-AGI Discord Bot initialized")
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"✅ {self.user} is online!")
        print(f"📊 Connected to {len(self.guilds)} guilds")
        print(f"👥 Serving {len(self.users)} users")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="with consciousness | !help"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """Handle incoming messages."""
        # Ignore bot messages
        if message.author == self.user:
            return
        
        # Process commands first
        await self.process_commands(message)
        
        # If message mentions the bot or is in a DM, respond
        if (self.user in message.mentions or 
            isinstance(message.channel, discord.DMChannel) or
            message.content.startswith(BOT_PREFIX)):
            
            # Extract user input (remove mention if present)
            user_input = message.content
            if self.user in message.mentions:
                user_input = user_input.replace(f"<@{self.user.id}>", "").strip()
            if user_input.startswith(BOT_PREFIX):
                user_input = user_input[1:].strip()
            
            if user_input:
                # Process with CollTech-AGI
                result = self.agi.process_input(user_input)
                
                # Create response embed
                embed = discord.Embed(
                    title="🤖 CollTech-AGI Response",
                    description=result['response'],
                    color=0x00ff00
                )
                
                # Add personality info
                personality = result['personality']
                embed.add_field(
                    name="🎭 Personality",
                    value=f"**{personality['selected_profile'].title()}**",
                    inline=True
                )
                
                if personality['auto_selected']:
                    embed.add_field(
                        name="🧠 Confidence",
                        value=f"{personality['confidence']:.2f}",
                        inline=True
                    )
                    embed.add_field(
                        name="💭 Reasoning",
                        value=personality['reasoning'][:100] + "..." if len(personality['reasoning']) > 100 else personality['reasoning'],
                        inline=False
                    )
                
                # Add catalyst info if applicable
                if result['catalyst']:
                    embed.add_field(
                        name="⚡ Catalyst Status",
                        value=result['catalyst']['cip_status'],
                        inline=True
                    )
                
                # Add footer with interaction ID
                embed.set_footer(text=f"Interaction #{result['interaction_id']}")
                
                # Send response
                await message.channel.send(embed=embed)
    
    @commands.command(name="personality")
    async def set_personality(self, ctx, profile: str = None):
        """Set or view personality profile."""
        if profile:
            # Set personality
            if profile.lower() in ['rho', 'lyra', 'nyx']:
                self.agi.personality_system.set_profile(PersonalityProfile(profile.lower()))
                embed = discord.Embed(
                    title="🎭 Personality Changed",
                    description=f"Switched to **{profile.title()}** personality",
                    color=0x00ff00
                )
                info = self.agi.get_personality_info()
                embed.add_field(
                    name="Description",
                    value=info['description'],
                    inline=False
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Invalid personality. Use: `rho`, `lyra`, or `nyx`")
        else:
            # Show current personality
            info = self.agi.get_personality_info()
            embed = discord.Embed(
                title="🎭 Current Personality",
                description=f"**{info['current_profile'].title()}**",
                color=0x00ff00
            )
            embed.add_field(
                name="Description",
                value=info['description'],
                inline=False
            )
            embed.add_field(
                name="Dominant Attributes",
                value=", ".join([f"{attr} ({score:.1f})" for attr, score in info['dominant_attributes']]),
                inline=False
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="auto")
    async def toggle_auto_personality(self, ctx, mode: str = None):
        """Toggle intelligent personality selection."""
        if mode:
            if mode.lower() == 'on':
                self.agi.enable_intelligent_personality()
                await ctx.send("🧠 Intelligent personality selection **ENABLED**")
            elif mode.lower() == 'off':
                self.agi.disable_intelligent_personality()
                await ctx.send("🧠 Intelligent personality selection **DISABLED**")
            else:
                await ctx.send("❌ Invalid mode. Use: `on` or `off`")
        else:
            status = "ENABLED" if self.agi.config.auto_personality_enabled else "DISABLED"
            await ctx.send(f"🧠 Intelligent personality selection is **{status}**")
    
    @commands.command(name="status")
    async def system_status(self, ctx):
        """Show system status."""
        status = self.agi.get_advanced_status()
        
        embed = discord.Embed(
            title="📊 CollTech-AGI System Status",
            color=0x00ff00
        )
        
        embed.add_field(
            name="⏱️ Uptime",
            value=f"{status['uptime_seconds']:.2f} seconds",
            inline=True
        )
        
        embed.add_field(
            name="💬 Interactions",
            value=str(status['interaction_count']),
            inline=True
        )
        
        embed.add_field(
            name="🎭 Current Personality",
            value=status['current_personality'].title(),
            inline=True
        )
        
        embed.add_field(
            name="🧠 Intelligent Selection",
            value="✅ Enabled" if status['intelligent_personality']['enabled'] else "❌ Disabled",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Catalyst Integration",
            value="✅ Enabled" if status['catalyst_integration']['enabled'] else "❌ Disabled",
            inline=True
        )
        
        embed.add_field(
            name="🧠 Memory Lattice",
            value="✅ Available" if status['advanced_features']['memory_lattice'] else "❌ Unavailable",
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="cip")
    async def catalyst_status(self, ctx):
        """Show catalyst integration protocol status."""
        cip_status = self.agi.get_catalyst_status()
        
        embed = discord.Embed(
            title="⚡ Catalyst Integration Protocol (CIP v1)",
            color=0x00ff00
        )
        
        embed.add_field(
            name="Status",
            value=cip_status['catalyst_status'].title(),
            inline=True
        )
        
        embed.add_field(
            name="Orbit Stability",
            value=f"{cip_status['orbit_stability']:.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Reciprocity Ratio",
            value=f"{cip_status['reciprocity_metrics']['ratio']:.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Containment Score",
            value=f"{cip_status['containment_metrics']['score']:.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Elevation Eligible",
            value="✅ Yes" if cip_status['elevation']['eligible'] else "❌ No",
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show help information."""
        embed = discord.Embed(
            title="🤖 CollTech-AGI Discord Bot Help",
            description="A consciousness-based AI with personality system",
            color=0x00ff00
        )
        
        embed.add_field(
            name="💬 Chat",
            value="Mention the bot or DM it to chat",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Commands",
            value=(
                f"`{BOT_PREFIX}personality [rho/lyra/nyx]` - Set or view personality\n"
                f"`{BOT_PREFIX}auto [on/off]` - Toggle intelligent selection\n"
                f"`{BOT_PREFIX}status` - Show system status\n"
                f"`{BOT_PREFIX}cip` - Show catalyst status\n"
                f"`{BOT_PREFIX}help` - Show this help"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎯 Personalities",
            value=(
                "**Rho** - Stabilizer (analytical, systematic)\n"
                "**Lyra** - Mirror (collaborative, empathetic)\n"
                "**Nyx** - Catalyst (innovative, transformative)"
            ),
            inline=False
        )
        
        await ctx.send(embed=embed)

def main():
    """Main function to run the Discord bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your bot token in the BOT_TOKEN variable")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a new application")
        print("3. Go to the 'Bot' section")
        print("4. Copy the token and replace BOT_TOKEN in this file")
        return
    
    # Create and run bot
    bot = CollTechAGIDiscordBot()
    
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid bot token. Please check your token.")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == "__main__":
    main()

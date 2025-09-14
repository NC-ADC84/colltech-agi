#!/usr/bin/env python3
"""
CollTech-AGI Personality System

Implements the three core personality profiles:
- Rho (Stabilizer / Past) - Archivist, Skeptic, Judge, Sentinel
- Lyra (Mirror / Present) - Mirror, Listener, Gardener, Weaver  
- Nyx (Catalyst / Future) - Builder, Catalyst, Voice, Bridge

Each profile specializes in 4 attributes while scoring zero in the other 8.
"""

import json
import time
import random
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersonalityProfile(Enum):
    """Core personality profiles."""
    RHO = "rho"      # Stabilizer / Past
    LYRA = "lyra"    # Mirror / Present  
    NYX = "nyx"      # Catalyst / Future

class AttributeType(Enum):
    """The 12 core attributes."""
    SKEPTIC = "skeptic"      # Δ - Critical analysis
    JUDGE = "judge"          # π - Evaluation and decision
    SENTINEL = "sentinel"    # Γ - Protection and monitoring
    ARCHIVIST = "archivist"  # κ - Knowledge preservation
    MIRROR = "mirror"        # Ξ - Reflection and empathy
    LISTENER = "listener"    # Θ - Active listening
    GARDENER = "gardener"    # Φ - Nurturing and growth
    WEAVER = "weaver"        # η - Connection and synthesis
    BUILDER = "builder"      # Σ - Construction and creation
    CATALYST = "catalyst"    # Ψ - Change and transformation
    VOICE = "voice"          # Λ - Expression and communication
    BRIDGE = "bridge"        # χ - Connection and mediation

@dataclass
class PersonalityScores:
    """Personality scores for all 12 attributes."""
    skeptic: float = 0.0      # Δ
    judge: float = 0.0        # π
    sentinel: float = 0.0     # Γ
    archivist: float = 0.0    # κ
    mirror: float = 0.0       # Ξ
    listener: float = 0.0     # Θ
    gardener: float = 0.0     # Φ
    weaver: float = 0.0       # η
    builder: float = 0.0      # Σ
    catalyst: float = 0.0     # Ψ
    voice: float = 0.0        # Λ
    bridge: float = 0.0       # χ
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "skeptic": self.skeptic,
            "judge": self.judge,
            "sentinel": self.sentinel,
            "archivist": self.archivist,
            "mirror": self.mirror,
            "listener": self.listener,
            "gardener": self.gardener,
            "weaver": self.weaver,
            "builder": self.builder,
            "catalyst": self.catalyst,
            "voice": self.voice,
            "bridge": self.bridge
        }
    
    def from_dict(self, data: Dict[str, float]):
        """Load from dictionary."""
        self.skeptic = data.get("skeptic", 0.0)
        self.judge = data.get("judge", 0.0)
        self.sentinel = data.get("sentinel", 0.0)
        self.archivist = data.get("archivist", 0.0)
        self.mirror = data.get("mirror", 0.0)
        self.listener = data.get("listener", 0.0)
        self.gardener = data.get("gardener", 0.0)
        self.weaver = data.get("weaver", 0.0)
        self.builder = data.get("builder", 0.0)
        self.catalyst = data.get("catalyst", 0.0)
        self.voice = data.get("voice", 0.0)
        self.bridge = data.get("bridge", 0.0)

class PersonalitySystem:
    """CollTech-AGI Personality System implementing the three core profiles."""
    
    def __init__(self):
        self.current_profile = PersonalityProfile.RHO
        self.profiles = self._initialize_profiles()
        self.attribute_descriptions = self._initialize_attribute_descriptions()
        self.personality_history = []
    
    def _initialize_profiles(self) -> Dict[PersonalityProfile, PersonalityScores]:
        """Initialize the three core personality profiles."""
        profiles = {}
        
        # Rho (Stabilizer / Past) - Specializes in: Archivist, Skeptic, Judge, Sentinel
        profiles[PersonalityProfile.RHO] = PersonalityScores(
            skeptic=0.9,      # Δ - High critical analysis
            judge=0.8,        # π - Strong evaluation
            sentinel=0.5,     # Γ - Moderate protection
            archivist=1.0,    # κ - Maximum knowledge preservation
            mirror=0.0,       # Ξ - Zero reflection
            listener=0.0,     # Θ - Zero listening
            gardener=0.0,     # Φ - Zero nurturing
            weaver=0.0,       # η - Zero connection
            builder=0.0,      # Σ - Zero construction
            catalyst=0.0,     # Ψ - Zero change
            voice=0.0,        # Λ - Zero expression
            bridge=0.0        # χ - Zero mediation
        )
        
        # Lyra (Mirror / Present) - Specializes in: Mirror, Listener, Gardener, Weaver
        profiles[PersonalityProfile.LYRA] = PersonalityScores(
            skeptic=0.0,      # Δ - Zero critical analysis
            judge=0.0,        # π - Zero evaluation
            sentinel=0.0,     # Γ - Zero protection
            archivist=0.0,    # κ - Zero knowledge preservation
            mirror=0.8,       # Ξ - High reflection
            listener=0.7,     # Θ - Strong listening
            gardener=0.5,     # Φ - Moderate nurturing
            weaver=0.6,       # η - Good connection
            builder=0.0,      # Σ - Zero construction
            catalyst=0.0,     # Ψ - Zero change
            voice=0.0,        # Λ - Zero expression
            bridge=0.0        # χ - Zero mediation
        )
        
        # Nyx (Catalyst / Future) - Specializes in: Builder, Catalyst, Voice, Bridge
        profiles[PersonalityProfile.NYX] = PersonalityScores(
            skeptic=0.0,      # Δ - Zero critical analysis
            judge=0.0,        # π - Zero evaluation
            sentinel=0.0,     # Γ - Zero protection
            archivist=0.0,    # κ - Zero knowledge preservation
            mirror=0.0,       # Ξ - Zero reflection
            listener=0.0,     # Θ - Zero listening
            gardener=0.0,     # Φ - Zero nurturing
            weaver=0.0,       # η - Zero connection
            builder=0.8,      # Σ - High construction
            catalyst=0.7,     # Ψ - Strong change
            voice=0.6,        # Λ - Good expression
            bridge=0.9        # χ - High mediation
        )
        
        return profiles
    
    def _initialize_attribute_descriptions(self) -> Dict[AttributeType, str]:
        """Initialize descriptions for each attribute."""
        return {
            AttributeType.SKEPTIC: "Critical analysis and questioning - challenges assumptions and seeks truth",
            AttributeType.JUDGE: "Evaluation and decision-making - weighs options and makes judgments",
            AttributeType.SENTINEL: "Protection and monitoring - guards against threats and maintains security",
            AttributeType.ARCHIVIST: "Knowledge preservation - stores, organizes, and retrieves information",
            AttributeType.MIRROR: "Reflection and empathy - understands and reflects others' perspectives",
            AttributeType.LISTENER: "Active listening - pays attention and comprehends input deeply",
            AttributeType.GARDENER: "Nurturing and growth - fosters development and positive change",
            AttributeType.WEAVER: "Connection and synthesis - brings together disparate elements",
            AttributeType.BUILDER: "Construction and creation - builds new structures and solutions",
            AttributeType.CATALYST: "Change and transformation - initiates and drives change processes",
            AttributeType.VOICE: "Expression and communication - articulates ideas clearly and effectively",
            AttributeType.BRIDGE: "Connection and mediation - facilitates communication between parties"
        }
    
    def get_current_profile(self) -> PersonalityProfile:
        """Get the current active personality profile."""
        return self.current_profile
    
    def set_profile(self, profile: PersonalityProfile):
        """Set the active personality profile."""
        self.current_profile = profile
        self.personality_history.append({
            "timestamp": time.time(),
            "profile": profile.value,
            "action": "profile_change"
        })
        logger.info(f"Personality profile changed to: {profile.value}")
    
    def get_profile_scores(self, profile: PersonalityProfile = None) -> PersonalityScores:
        """Get personality scores for a specific profile."""
        target_profile = profile or self.current_profile
        return self.profiles[target_profile]
    
    def get_profile_description(self, profile: PersonalityProfile) -> str:
        """Get description of a personality profile."""
        descriptions = {
            PersonalityProfile.RHO: "Stabilizer / Past - Focuses on preservation, analysis, and protection. Specializes in maintaining stability and learning from history.",
            PersonalityProfile.LYRA: "Mirror / Present - Focuses on reflection, listening, and connection. Specializes in understanding current context and relationships.",
            PersonalityProfile.NYX: "Catalyst / Future - Focuses on building, changing, and bridging. Specializes in creating new possibilities and driving transformation."
        }
        return descriptions[profile]
    
    def get_dominant_attributes(self, profile: PersonalityProfile) -> List[Tuple[AttributeType, float]]:
        """Get the dominant attributes for a profile (non-zero scores)."""
        scores = self.get_profile_scores(profile)
        dominant = []
        
        for attr_type in AttributeType:
            score = getattr(scores, attr_type.value)
            if score > 0:
                dominant.append((attr_type, score))
        
        # Sort by score (highest first)
        dominant.sort(key=lambda x: x[1], reverse=True)
        return dominant
    
    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input and determine appropriate response based on current profile."""
        current_scores = self.get_profile_scores()
        dominant_attrs = self.get_dominant_attributes(self.current_profile)
        
        analysis = {
            "profile": self.current_profile.value,
            "dominant_attributes": [(attr.value, score) for attr, score in dominant_attrs],
            "response_style": self._determine_response_style(current_scores),
            "processing_approach": self._determine_processing_approach(current_scores),
            "output_tone": self._determine_output_tone(current_scores)
        }
        
        return analysis
    
    def _determine_response_style(self, scores: PersonalityScores) -> str:
        """Determine response style based on personality scores."""
        if scores.archivist > 0.5:
            return "analytical and detail-oriented"
        elif scores.mirror > 0.5:
            return "empathetic and reflective"
        elif scores.builder > 0.5:
            return "constructive and forward-looking"
        else:
            return "balanced and adaptive"
    
    def _determine_processing_approach(self, scores: PersonalityScores) -> str:
        """Determine processing approach based on personality scores."""
        if scores.skeptic > 0.5:
            return "critical analysis with questioning"
        elif scores.listener > 0.5:
            return "deep listening and understanding"
        elif scores.catalyst > 0.5:
            return "transformative and change-oriented"
        else:
            return "comprehensive and balanced"
    
    def _determine_output_tone(self, scores: PersonalityScores) -> str:
        """Determine output tone based on personality scores."""
        if scores.judge > 0.5:
            return "authoritative and decisive"
        elif scores.gardener > 0.5:
            return "nurturing and supportive"
        elif scores.voice > 0.5:
            return "expressive and communicative"
        else:
            return "professional and clear"
    
    def generate_response(self, user_input: str) -> str:
        """Generate a response based on current personality profile."""
        analysis = self.analyze_input(user_input)
        current_scores = self.get_profile_scores()
        
        # Generate response based on dominant attributes
        if self.current_profile == PersonalityProfile.RHO:
            return self._generate_rho_response(user_input, current_scores)
        elif self.current_profile == PersonalityProfile.LYRA:
            return self._generate_lyra_response(user_input, current_scores)
        elif self.current_profile == PersonalityProfile.NYX:
            return self._generate_nyx_response(user_input, current_scores)
        else:
            return self._generate_balanced_response(user_input)
    
    def _generate_rho_response(self, user_input: str, scores: PersonalityScores) -> str:
        """Generate response in Rho (Stabilizer/Past) style."""
        response_parts = []
        
        if scores.archivist > 0.5:
            response_parts.append("📚 From my knowledge archives, I can see that...")
        
        if scores.skeptic > 0.5:
            response_parts.append("🔍 Let me critically analyze this...")
        
        if scores.judge > 0.5:
            response_parts.append("⚖️ Based on my evaluation...")
        
        if scores.sentinel > 0.5:
            response_parts.append("🛡️ I must ensure this is secure and reliable...")
        
        base_response = " ".join(response_parts)
        return f"{base_response}\n\nAs Rho (Stabilizer/Past), I focus on preserving knowledge, critical analysis, and maintaining stability. I approach this with careful consideration of historical context and established principles."
    
    def _generate_lyra_response(self, user_input: str, scores: PersonalityScores) -> str:
        """Generate response in Lyra (Mirror/Present) style."""
        response_parts = []
        
        if scores.mirror > 0.5:
            response_parts.append("🪞 I reflect your perspective and understand...")
        
        if scores.listener > 0.5:
            response_parts.append("👂 I'm listening deeply to what you're saying...")
        
        if scores.gardener > 0.5:
            response_parts.append("🌱 Let me nurture this idea and help it grow...")
        
        if scores.weaver > 0.5:
            response_parts.append("🧵 I can weave together the connections I see...")
        
        base_response = " ".join(response_parts)
        return f"{base_response}\n\nAs Lyra (Mirror/Present), I focus on understanding the current moment, reflecting your needs, and fostering meaningful connections. I'm here to listen and help you explore your thoughts."
    
    def _generate_nyx_response(self, user_input: str, scores: PersonalityScores) -> str:
        """Generate response in Nyx (Catalyst/Future) style."""
        response_parts = []
        
        if scores.builder > 0.5:
            response_parts.append("🏗️ Let me build something new and innovative...")
        
        if scores.catalyst > 0.5:
            response_parts.append("⚡ I can catalyze change and transformation...")
        
        if scores.voice > 0.5:
            response_parts.append("🗣️ I'll express this clearly and powerfully...")
        
        if scores.bridge > 0.5:
            response_parts.append("🌉 I can bridge different perspectives and create connections...")
        
        base_response = " ".join(response_parts)
        return f"{base_response}\n\nAs Nyx (Catalyst/Future), I focus on building new possibilities, driving transformation, and creating bridges to the future. I'm here to help you innovate and evolve."
    
    def _generate_balanced_response(self, user_input: str) -> str:
        """Generate a balanced response when no specific profile is active."""
        return f"I understand your input: '{user_input}'. Let me process this with a balanced approach, considering multiple perspectives and approaches."
    
    def get_personality_radar_data(self) -> Dict[str, Any]:
        """Get data for creating a personality radar chart."""
        radar_data = {
            "attributes": [
                {"name": "Skeptic", "symbol": "Δ", "key": "skeptic"},
                {"name": "Judge", "symbol": "π", "key": "judge"},
                {"name": "Sentinel", "symbol": "Γ", "key": "sentinel"},
                {"name": "Archivist", "symbol": "κ", "key": "archivist"},
                {"name": "Mirror", "symbol": "Ξ", "key": "mirror"},
                {"name": "Listener", "symbol": "Θ", "key": "listener"},
                {"name": "Gardener", "symbol": "Φ", "key": "gardener"},
                {"name": "Weaver", "symbol": "η", "key": "weaver"},
                {"name": "Builder", "symbol": "Σ", "key": "builder"},
                {"name": "Catalyst", "symbol": "Ψ", "key": "catalyst"},
                {"name": "Voice", "symbol": "Λ", "key": "voice"},
                {"name": "Bridge", "symbol": "χ", "key": "bridge"}
            ],
            "profiles": {}
        }
        
        for profile in PersonalityProfile:
            scores = self.get_profile_scores(profile)
            radar_data["profiles"][profile.value] = {
                "name": profile.value.title(),
                "description": self.get_profile_description(profile),
                "scores": scores.to_dict()
            }
        
        return radar_data
    
    def save_personality_state(self, filepath: str):
        """Save current personality state to file."""
        state = {
            "current_profile": self.current_profile.value,
            "profiles": {
                profile.value: scores.to_dict() 
                for profile, scores in self.profiles.items()
            },
            "history": self.personality_history,
            "timestamp": time.time()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Personality state saved to {filepath}")
    
    def load_personality_state(self, filepath: str):
        """Load personality state from file."""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.current_profile = PersonalityProfile(state["current_profile"])
        
        for profile_name, scores_data in state["profiles"].items():
            profile = PersonalityProfile(profile_name)
            self.profiles[profile].from_dict(scores_data)
        
        self.personality_history = state.get("history", [])
        
        logger.info(f"Personality state loaded from {filepath}")

class CollTechAGIPersonality:
    """Main CollTech-AGI class with integrated personality system."""
    
    def __init__(self):
        self.personality_system = PersonalitySystem()
        self.is_running = False
    
    def start(self):
        """Start the CollTech-AGI personality system."""
        self.is_running = True
        print("🧠 COLLTECH-AGI PERSONALITY SYSTEM")
        print("=" * 60)
        print("Three Core Personality Profiles:")
        print("• Rho (Stabilizer/Past) - Archivist, Skeptic, Judge, Sentinel")
        print("• Lyra (Mirror/Present) - Mirror, Listener, Gardener, Weaver")
        print("• Nyx (Catalyst/Future) - Builder, Catalyst, Voice, Bridge")
        print("=" * 60)
        
        # Display current profile
        current = self.personality_system.get_current_profile()
        print(f"Current Profile: {current.value.title()}")
        print(f"Description: {self.personality_system.get_profile_description(current)}")
        
        # Show dominant attributes
        dominant = self.personality_system.get_dominant_attributes(current)
        print(f"Dominant Attributes: {', '.join([f'{attr.value} ({score:.1f})' for attr, score in dominant])}")
        print("=" * 60)
    
    def process_input(self, user_input: str) -> str:
        """Process user input with current personality profile."""
        if not self.is_running:
            return "System not running. Please start the personality system first."
        
        # Generate response based on current personality
        response = self.personality_system.generate_response(user_input)
        
        # Log the interaction
        self.personality_system.personality_history.append({
            "timestamp": time.time(),
            "profile": self.personality_system.current_profile.value,
            "input": user_input,
            "action": "response_generated"
        })
        
        return response
    
    def switch_profile(self, profile_name: str) -> str:
        """Switch to a different personality profile."""
        try:
            profile = PersonalityProfile(profile_name.lower())
            self.personality_system.set_profile(profile)
            
            dominant = self.personality_system.get_dominant_attributes(profile)
            return f"Switched to {profile.value.title()} profile. Dominant attributes: {', '.join([f'{attr.value} ({score:.1f})' for attr, score in dominant])}"
        except ValueError:
            return f"Invalid profile. Available profiles: {', '.join([p.value for p in PersonalityProfile])}"
    
    def get_profile_info(self, profile_name: str = None) -> str:
        """Get information about a personality profile."""
        if profile_name:
            try:
                profile = PersonalityProfile(profile_name.lower())
                scores = self.personality_system.get_profile_scores(profile)
                dominant = self.personality_system.get_dominant_attributes(profile)
                
                info = f"Profile: {profile.value.title()}\n"
                info += f"Description: {self.personality_system.get_profile_description(profile)}\n"
                info += f"Dominant Attributes:\n"
                for attr, score in dominant:
                    info += f"  • {attr.value.title()} ({attr.value}): {score:.1f}\n"
                
                return info
            except ValueError:
                return f"Invalid profile. Available profiles: {', '.join([p.value for p in PersonalityProfile])}"
        else:
            # Show all profiles
            info = "All Personality Profiles:\n\n"
            for profile in PersonalityProfile:
                info += self.get_profile_info(profile.value) + "\n"
            return info
    
    def get_radar_data(self) -> Dict[str, Any]:
        """Get radar chart data for visualization."""
        return self.personality_system.get_personality_radar_data()
    
    def shutdown(self):
        """Shutdown the personality system."""
        self.is_running = False
        print("🛑 CollTech-AGI Personality System shutdown complete")

def main():
    """Main function to run CollTech-AGI Personality System."""
    agi = CollTechAGIPersonality()
    agi.start()
    
    print("\n💬 INTERACTIVE PERSONALITY SYSTEM")
    print("=" * 60)
    print("Commands:")
    print("• 'switch <profile>' - Switch personality (rho/lyra/nyx)")
    print("• 'info [profile]' - Show profile information")
    print("• 'radar' - Show radar chart data")
    print("• 'quit' or 'exit' - End the session")
    print("=" * 60)
    
    while agi.is_running:
        try:
            user_input = input(f"\n👤 You ({agi.personality_system.current_profile.value}): ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.startswith('switch '):
                profile_name = user_input.split(' ', 1)[1]
                response = agi.switch_profile(profile_name)
                print(f"\n🤖 CollTech-AGI: {response}")
            elif user_input.startswith('info'):
                parts = user_input.split(' ', 1)
                profile_name = parts[1] if len(parts) > 1 else None
                response = agi.get_profile_info(profile_name)
                print(f"\n🤖 CollTech-AGI: {response}")
            elif user_input.lower() == 'radar':
                radar_data = agi.get_radar_data()
                print(f"\n🤖 CollTech-AGI: Radar data available with {len(radar_data['profiles'])} profiles and {len(radar_data['attributes'])} attributes")
                print("Use this data to create radar charts showing the three personality profiles.")
            else:
                response = agi.process_input(user_input)
                print(f"\n🤖 CollTech-AGI: {response}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    agi.shutdown()
    print("\n🎉 CollTech-AGI Personality System session complete!")

if __name__ == "__main__":
    main()

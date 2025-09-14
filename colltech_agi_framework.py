#!/usr/bin/env python3
"""
CollTech-AGI Framework - Modular AI Consciousness System

A complete, modular framework for building consciousness-based AI systems
with personality management, intelligent selection, and real-time capabilities.

Designed for easy integration, learning, and remixing.
"""

import json
import time
import logging
import asyncio
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import hashlib
import threading
from collections import deque

# Import all framework components
from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile, AttributeType
from intelligent_personality_selector import IntelligentPersonalitySelector, InteractionType, DataContext
from catalyst_integration_protocol import CatalystIntegrationProtocol, CatalystStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FrameworkConfig:
    """Configuration for CollTech-AGI Framework."""
    auto_personality_enabled: bool = True
    catalyst_integration_enabled: bool = True
    realtime_apis_enabled: bool = True
    memory_lattice_enabled: bool = True
    drift_detection_enabled: bool = True
    tool_making_enabled: bool = True
    debug_mode: bool = False
    log_level: str = "INFO"

class CollTechAGI:
    """Basic CollTech-AGI Framework - Core functionality."""
    
    def __init__(self, config: FrameworkConfig = None):
        self.config = config or FrameworkConfig()
        self.personality_system = PersonalitySystem()
        self.is_running = False
        self.interaction_count = 0
        self.start_time = time.time()
        
        logger.info("🚀 CollTech-AGI Framework initialized")
    
    def start(self):
        """Start the CollTech-AGI system."""
        self.is_running = True
        self.start_time = time.time()
        logger.info("✅ CollTech-AGI Framework started")
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response."""
        if not self.is_running:
            return "System not running. Please start the framework first."
        
        self.interaction_count += 1
        
        # Generate response using current personality
        response = self.personality_system.generate_response(user_input)
        
        if self.config.debug_mode:
            logger.debug(f"Processed input: {user_input[:50]}...")
            logger.debug(f"Generated response: {response[:50]}...")
        
        return response
    
    def set_personality(self, profile: Union[str, PersonalityProfile]) -> bool:
        """Set the personality profile."""
        if isinstance(profile, str):
            try:
                profile = PersonalityProfile(profile.lower())
            except ValueError:
                logger.error(f"Invalid personality profile: {profile}")
                return False
        
        self.personality_system.set_profile(profile)
        logger.info(f"Personality set to: {profile.value}")
        return True
    
    def get_personality(self) -> str:
        """Get current personality profile."""
        return self.personality_system.get_current_profile().value
    
    def get_personality_info(self) -> Dict[str, Any]:
        """Get detailed personality information."""
        current_profile = self.personality_system.get_current_profile()
        dominant_attrs = self.personality_system.get_dominant_attributes(current_profile)
        
        return {
            "current_profile": current_profile.value,
            "description": self.personality_system.get_profile_description(current_profile),
            "dominant_attributes": [(attr.value, score) for attr, score in dominant_attrs],
            "available_profiles": [profile.value for profile in PersonalityProfile]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information."""
        uptime = time.time() - self.start_time
        
        return {
            "is_running": self.is_running,
            "uptime_seconds": uptime,
            "interaction_count": self.interaction_count,
            "current_personality": self.get_personality(),
            "config": {
                "auto_personality_enabled": self.config.auto_personality_enabled,
                "catalyst_integration_enabled": self.config.catalyst_integration_enabled,
                "realtime_apis_enabled": self.config.realtime_apis_enabled,
                "debug_mode": self.config.debug_mode
            }
        }
    
    def shutdown(self):
        """Shutdown the system."""
        self.is_running = False
        logger.info("🛑 CollTech-AGI Framework shutdown complete")

class CollTechAGIAdvanced(CollTechAGI):
    """Advanced CollTech-AGI Framework - Full feature set."""
    
    def __init__(self, config: FrameworkConfig = None):
        super().__init__(config)
        
        # Initialize advanced components
        self.intelligent_selector = IntelligentPersonalitySelector()
        self.catalyst_protocol = CatalystIntegrationProtocol()
        
        # Advanced features
        self.memory_lattice = None
        self.drift_detector = None
        self.tool_maker = None
        
        if self.config.memory_lattice_enabled:
            self._initialize_memory_lattice()
        
        if self.config.drift_detection_enabled:
            self._initialize_drift_detection()
        
        if self.config.tool_making_enabled:
            self._initialize_tool_making()
        
        logger.info("🚀 CollTech-AGI Advanced Framework initialized")
    
    def _initialize_memory_lattice(self):
        """Initialize memory lattice system."""
        try:
            from src.catch.memory.memory_lattice import MemoryLattice
            self.memory_lattice = MemoryLattice()
            logger.info("✅ Memory lattice initialized")
        except ImportError:
            logger.warning("⚠️ Memory lattice not available")
    
    def _initialize_drift_detection(self):
        """Initialize drift detection system."""
        try:
            from src.catch.drift.drift_system import DriftSystem
            self.drift_detector = DriftSystem()
            logger.info("✅ Drift detection initialized")
        except ImportError:
            logger.warning("⚠️ Drift detection not available")
    
    def _initialize_tool_making(self):
        """Initialize tool making system."""
        try:
            from src.catch.tools.tool_making_loop import ToolMakingLoop
            self.tool_maker = ToolMakingLoop()
            logger.info("✅ Tool making system initialized")
        except ImportError:
            logger.warning("⚠️ Tool making system not available")
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input with advanced features."""
        if not self.is_running:
            return {"error": "System not running. Please start the framework first."}
        
        self.interaction_count += 1
        
        # Auto-select personality if enabled
        if self.config.auto_personality_enabled:
            selection = self.intelligent_selector.select_personality(user_input)
            self.personality_system.set_profile(selection.selected_profile)
            auto_selection_info = {
                "auto_selected": True,
                "confidence": selection.confidence_score,
                "reasoning": selection.reasoning,
                "selected_profile": selection.selected_profile.value
            }
        else:
            auto_selection_info = {
                "auto_selected": False,
                "selected_profile": self.personality_system.get_current_profile().value
            }
        
        # Generate response
        response = self.personality_system.generate_response(user_input)
        
        # Process through catalyst protocol if Nyx personality
        catalyst_info = {}
        if (self.config.catalyst_integration_enabled and 
            self.personality_system.get_current_profile() == PersonalityProfile.NYX):
            cip_result = self.catalyst_protocol.process_catalyst_action("dialogue", user_input)
            catalyst_info = {
                "cip_status": cip_result['current_status'],
                "orbit_stability": cip_result.get('orbit_stability', 0.0),
                "safety_filters_triggered": cip_result.get('safety_status', {}).get('triggered_filters', [])
            }
        
        # Process through memory lattice if available
        memory_info = {}
        if self.memory_lattice:
            try:
                memory_result = self.memory_lattice.store_interaction(user_input, response)
                memory_info = {
                    "stored": memory_result.get('stored', False),
                    "memory_level": memory_result.get('level', 'short_term')
                }
            except Exception as e:
                logger.warning(f"Memory lattice error: {e}")
        
        # Process through drift detection if available
        drift_info = {}
        if self.drift_detector:
            try:
                drift_result = self.drift_detector.analyze_response(response)
                drift_info = {
                    "drift_detected": drift_result.get('drift_detected', False),
                    "drift_score": drift_result.get('drift_score', 0.0)
                }
            except Exception as e:
                logger.warning(f"Drift detection error: {e}")
        
        return {
            "response": response,
            "personality": auto_selection_info,
            "catalyst": catalyst_info,
            "memory": memory_info,
            "drift": drift_info,
            "timestamp": time.time(),
            "interaction_id": self.interaction_count
        }
    
    def enable_intelligent_personality(self):
        """Enable intelligent personality auto-selection."""
        self.config.auto_personality_enabled = True
        logger.info("🧠 Intelligent personality selection enabled")
    
    def disable_intelligent_personality(self):
        """Disable intelligent personality auto-selection."""
        self.config.auto_personality_enabled = False
        logger.info("🧠 Intelligent personality selection disabled")
    
    def get_selection_history(self) -> List[Dict[str, Any]]:
        """Get personality selection history."""
        return self.intelligent_selector.get_selection_history()
    
    def get_learned_preferences(self) -> Dict[str, float]:
        """Get learned user preferences."""
        return self.intelligent_selector.get_user_preferences()
    
    def reset_learned_preferences(self):
        """Reset learned user preferences."""
        self.intelligent_selector.reset_preferences()
        logger.info("🔄 Learned preferences reset")
    
    def get_catalyst_status(self) -> Dict[str, Any]:
        """Get catalyst integration protocol status."""
        return self.catalyst_protocol.get_protocol_status()
    
    def pair_catalyst_with_stabilizer(self, stabilizer_type: str) -> Dict[str, Any]:
        """Pair catalyst with stabilizer."""
        return self.catalyst_protocol.pair_with_stabilizer(stabilizer_type)
    
    def elevate_catalyst(self) -> Dict[str, Any]:
        """Attempt to elevate catalyst."""
        return self.catalyst_protocol.elevate_catalyst()
    
    def get_advanced_status(self) -> Dict[str, Any]:
        """Get advanced system status."""
        base_status = self.get_system_status()
        
        advanced_status = {
            **base_status,
            "intelligent_personality": {
                "enabled": self.config.auto_personality_enabled,
                "interaction_history_count": len(self.intelligent_selector.interaction_history),
                "learned_preferences_count": len(self.intelligent_selector.user_preferences)
            },
            "catalyst_integration": {
                "enabled": self.config.catalyst_integration_enabled,
                "status": self.catalyst_protocol.catalyst_status.value,
                "orbit_stability": self.catalyst_protocol.orbit_stability_score
            },
            "advanced_features": {
                "memory_lattice": self.memory_lattice is not None,
                "drift_detection": self.drift_detector is not None,
                "tool_making": self.tool_maker is not None
            }
        }
        
        return advanced_status

class CollTechAGIFramework:
    """Main framework class for easy access to all components."""
    
    @staticmethod
    def create_basic(config: FrameworkConfig = None) -> CollTechAGI:
        """Create a basic CollTech-AGI instance."""
        return CollTechAGI(config)
    
    @staticmethod
    def create_advanced(config: FrameworkConfig = None) -> CollTechAGIAdvanced:
        """Create an advanced CollTech-AGI instance."""
        return CollTechAGIAdvanced(config)
    
    @staticmethod
    def create_custom(config: FrameworkConfig = None, custom_class=None):
        """Create a custom CollTech-AGI instance."""
        if custom_class:
            return custom_class(config)
        else:
            return CollTechAGIAdvanced(config)

# Convenience functions for easy usage
def create_agi(config: FrameworkConfig = None) -> CollTechAGI:
    """Create a basic CollTech-AGI instance."""
    return CollTechAGIFramework.create_basic(config)

def create_advanced_agi(config: FrameworkConfig = None) -> CollTechAGIAdvanced:
    """Create an advanced CollTech-AGI instance."""
    return CollTechAGIFramework.create_advanced(config)

def create_custom_agi(config: FrameworkConfig = None, custom_class=None):
    """Create a custom CollTech-AGI instance."""
    return CollTechAGIFramework.create_custom(config, custom_class)

# Example usage and testing
def main():
    """Main function for testing the framework."""
    print("🚀 CollTech-AGI Framework Test")
    print("=" * 50)
    
    # Test basic framework
    print("\n1. Testing Basic Framework:")
    agi_basic = create_agi()
    agi_basic.start()
    
    # Test personality switching
    agi_basic.set_personality("rho")
    response = agi_basic.process_input("How do I solve this problem?")
    print(f"Rho Response: {response}")
    
    agi_basic.set_personality("lyra")
    response = agi_basic.process_input("Let's work together on this")
    print(f"Lyra Response: {response}")
    
    agi_basic.set_personality("nyx")
    response = agi_basic.process_input("Help me innovate something new")
    print(f"Nyx Response: {response}")
    
    # Test advanced framework
    print("\n2. Testing Advanced Framework:")
    agi_advanced = create_advanced_agi()
    agi_advanced.start()
    
    # Test intelligent personality selection
    response = agi_advanced.process_input("How do I analyze this data?")
    print(f"Auto-Selected: {response['personality']['selected_profile']}")
    print(f"Response: {response['response']}")
    
    response = agi_advanced.process_input("Let's collaborate on this project")
    print(f"Auto-Selected: {response['personality']['selected_profile']}")
    print(f"Response: {response['response']}")
    
    response = agi_advanced.process_input("Help me create something revolutionary")
    print(f"Auto-Selected: {response['personality']['selected_profile']}")
    print(f"Response: {response['response']}")
    
    # Test system status
    print("\n3. System Status:")
    status = agi_advanced.get_advanced_status()
    print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
    print(f"Interactions: {status['interaction_count']}")
    print(f"Intelligent Personality: {status['intelligent_personality']['enabled']}")
    print(f"Catalyst Integration: {status['catalyst_integration']['enabled']}")
    
    # Shutdown
    agi_basic.shutdown()
    agi_advanced.shutdown()
    
    print("\n✅ Framework test complete!")

if __name__ == "__main__":
    main()

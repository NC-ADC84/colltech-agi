"""
CollTech-AGI Framework with Agentic Mindsets
Version 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Andre Collier"

# Import main components for easy access
try:
    from .src.agentic_mindsets_integration import (
        AgenticMindsetsIntegration,
        AgenticConfig,
        AgenticMode,
        create_agentic_integration
    )
    
    from .colltech_agi_personality_system import (
        PersonalitySystem,
        PersonalityProfile
    )
    
    __all__ = [
        'AgenticMindsetsIntegration',
        'AgenticConfig',
        'AgenticMode',
        'create_agentic_integration',
        'PersonalitySystem',
        'PersonalityProfile',
    ]
except ImportError as e:
    # Graceful degradation if some modules aren't available
    print(f"Warning: Some CollTech-AGI modules could not be imported: {e}")
    __all__ = []

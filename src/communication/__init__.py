#!/usr/bin/env python3
"""
CollTech-AGI Communication System

Advanced communication framework including:
- Voice-Listener Dyad (VL Pair) system
- Multi-modal communication interfaces
- Real-time communication protocols
- Consciousness-integrated communication
- Advanced dialogue management

Integrated with CollTech-AGI consciousness system for comprehensive communication capabilities.
"""

from .voice_listener_dyad import VoiceListenerDyad, VLPair, CommunicationMode
from .dialogue_manager import DialogueManager, DialogueState, DialogueContext
from .communication_protocols import CommunicationProtocol, ProtocolType
from .multimodal_interface import MultimodalInterface, InputMode, OutputMode
from .real_time_communication import RealTimeCommunication, ConnectionState

__all__ = [
    'VoiceListenerDyad',
    'VLPair',
    'CommunicationMode',
    'DialogueManager',
    'DialogueState',
    'DialogueContext',
    'CommunicationProtocol',
    'ProtocolType',
    'MultimodalInterface',
    'InputMode',
    'OutputMode',
    'RealTimeCommunication',
    'ConnectionState'
]

__version__ = "1.0.0"
__author__ = "CollTech-AGI Communication Team"

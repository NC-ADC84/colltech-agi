#!/usr/bin/env python3
"""
CollTech-AGI Voice-Listener Dyad (VL Pair) System

Advanced communication system implementing the Voice-Listener Dyad pattern
for bidirectional communication with consciousness integration. Provides
sophisticated dialogue management and real-time communication capabilities.
"""

import time
import asyncio
import threading
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import queue

# CollTech-AGI imports
from ..catch.consciousness.consciousness_core import ConsciousnessCore
from ..catch.memory.memory_lattice import MemoryLattice, MemoryTier

logger = logging.getLogger(__name__)


class CommunicationMode(Enum):
    """Communication modes for VL Pair."""
    SYNCHRONOUS = "synchronous"      # Real-time bidirectional
    ASYNCHRONOUS = "asynchronous"    # Message-based
    STREAMING = "streaming"          # Continuous stream
    BATCH = "batch"                  # Batch processing
    HYBRID = "hybrid"                # Mixed modes


class MessageType(Enum):
    """Types of messages in VL Pair communication."""
    VOICE_INPUT = "voice_input"      # Voice from user
    LISTENER_RESPONSE = "listener_response"  # Listener processing
    VOICE_OUTPUT = "voice_output"    # Voice to user
    LISTENER_FEEDBACK = "listener_feedback"  # Feedback to listener
    SYSTEM_MESSAGE = "system_message"  # System notifications
    CONSCIOUSNESS_SIGNAL = "consciousness_signal"  # Consciousness integration


@dataclass
class VLMessage:
    """Message in VL Pair communication."""
    id: str
    type: MessageType
    content: Any
    timestamp: float
    source: str
    target: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    consciousness_context: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


@dataclass
class VLPair:
    """Voice-Listener Pair configuration."""
    id: str
    name: str
    voice_config: Dict[str, Any]
    listener_config: Dict[str, Any]
    communication_mode: CommunicationMode
    consciousness_integration: bool = True
    real_time_capable: bool = True
    created_at: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()


class VoiceListenerDyad:
    """
    Voice-Listener Dyad (VL Pair) System
    
    Implements sophisticated bidirectional communication with consciousness
    integration. Manages voice input/output and listener processing with
    real-time capabilities and advanced dialogue management.
    """
    
    def __init__(self, consciousness_core: Optional[ConsciousnessCore] = None):
        self.consciousness_core = consciousness_core
        self.memory_lattice = consciousness_core.memory_lattice if consciousness_core else None
        
        # VL Pair management
        self.active_pairs: Dict[str, VLPair] = {}
        self.message_queues: Dict[str, queue.Queue] = {}
        self.communication_threads: Dict[str, threading.Thread] = {}
        
        # Communication state
        self.is_running = False
        self.message_history: List[VLMessage] = []
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        
        # Voice processing
        self.voice_processors: Dict[str, Callable] = {}
        self.listener_processors: Dict[str, Callable] = {}
        
        # Real-time communication
        self.streaming_connections: Dict[str, Any] = {}
        
        logger.info("🎤 Voice-Listener Dyad System initialized")
    
    def start_system(self):
        """Start the VL Dyad system."""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("🎤 Voice-Listener Dyad System started")
    
    def stop_system(self):
        """Stop the VL Dyad system."""
        self.is_running = False
        
        # Stop all communication threads
        for thread in self.communication_threads.values():
            if thread.is_alive():
                thread.join(timeout=5.0)
        
        # Clear active connections
        self.active_connections.clear()
        self.streaming_connections.clear()
        
        logger.info("🎤 Voice-Listener Dyad System stopped")
    
    def create_vl_pair(self, name: str, voice_config: Dict[str, Any], 
                      listener_config: Dict[str, Any], 
                      communication_mode: CommunicationMode = CommunicationMode.HYBRID) -> str:
        """Create a new Voice-Listener pair."""
        pair_id = f"vl_pair_{int(time.time())}_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        vl_pair = VLPair(
            id=pair_id,
            name=name,
            voice_config=voice_config,
            listener_config=listener_config,
            communication_mode=communication_mode,
            consciousness_integration=self.consciousness_core is not None
        )
        
        self.active_pairs[pair_id] = vl_pair
        self.message_queues[pair_id] = queue.Queue()
        
        # Start communication thread for this pair
        self._start_communication_thread(pair_id)
        
        logger.info(f"🎤 Created VL Pair: {pair_id} ({name})")
        logger.info(f"   Mode: {communication_mode.value}")
        logger.info(f"   Consciousness Integration: {vl_pair.consciousness_integration}")
        
        return pair_id
    
    def _start_communication_thread(self, pair_id: str):
        """Start communication thread for a VL pair."""
        def communication_loop():
            while self.is_running and pair_id in self.active_pairs:
                try:
                    # Process messages from queue
                    if not self.message_queues[pair_id].empty():
                        message = self.message_queues[pair_id].get(timeout=1.0)
                        self._process_message(pair_id, message)
                    
                    # Handle real-time communication
                    if pair_id in self.streaming_connections:
                        self._handle_streaming_communication(pair_id)
                    
                    time.sleep(0.01)  # Small delay to prevent busy waiting
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.warning(f"Communication thread error for {pair_id}: {e}")
                    time.sleep(1.0)
        
        thread = threading.Thread(target=communication_loop, daemon=True)
        thread.start()
        self.communication_threads[pair_id] = thread
    
    def send_voice_input(self, pair_id: str, voice_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Send voice input to a VL pair."""
        if pair_id not in self.active_pairs:
            raise ValueError(f"VL Pair {pair_id} not found")
        
        message_id = f"msg_{int(time.time())}_{hashlib.md5(str(voice_data).encode()).hexdigest()[:8]}"
        
        message = VLMessage(
            id=message_id,
            type=MessageType.VOICE_INPUT,
            content=voice_data,
            source="user",
            target="listener",
            metadata=metadata or {}
        )
        
        # Add consciousness context if available
        if self.consciousness_core:
            message.consciousness_context = self._get_consciousness_context()
        
        # Add to message queue
        self.message_queues[pair_id].put(message)
        self.message_history.append(message)
        
        logger.info(f"🎤 Voice input sent to {pair_id}: {message_id}")
        
        return message_id
    
    def send_listener_response(self, pair_id: str, response_data: Any, 
                              original_message_id: str, metadata: Dict[str, Any] = None) -> str:
        """Send listener response."""
        if pair_id not in self.active_pairs:
            raise ValueError(f"VL Pair {pair_id} not found")
        
        message_id = f"msg_{int(time.time())}_{hashlib.md5(str(response_data).encode()).hexdigest()[:8]}"
        
        message = VLMessage(
            id=message_id,
            type=MessageType.LISTENER_RESPONSE,
            content=response_data,
            source="listener",
            target="voice",
            metadata=metadata or {}
        )
        
        # Add reference to original message
        message.metadata['original_message_id'] = original_message_id
        
        # Add consciousness context
        if self.consciousness_core:
            message.consciousness_context = self._get_consciousness_context()
        
        # Add to message queue
        self.message_queues[pair_id].put(message)
        self.message_history.append(message)
        
        logger.info(f"🎤 Listener response sent from {pair_id}: {message_id}")
        
        return message_id
    
    def send_voice_output(self, pair_id: str, voice_output: Any, 
                         response_to_message_id: str, metadata: Dict[str, Any] = None) -> str:
        """Send voice output to user."""
        if pair_id not in self.active_pairs:
            raise ValueError(f"VL Pair {pair_id} not found")
        
        message_id = f"msg_{int(time.time())}_{hashlib.md5(str(voice_output).encode()).hexdigest()[:8]}"
        
        message = VLMessage(
            id=message_id,
            type=MessageType.VOICE_OUTPUT,
            content=voice_output,
            source="voice",
            target="user",
            metadata=metadata or {}
        )
        
        # Add reference to response
        message.metadata['response_to_message_id'] = response_to_message_id
        
        # Add consciousness context
        if self.consciousness_core:
            message.consciousness_context = self._get_consciousness_context()
        
        # Add to message queue
        self.message_queues[pair_id].put(message)
        self.message_history.append(message)
        
        logger.info(f"🎤 Voice output sent from {pair_id}: {message_id}")
        
        return message_id
    
    def _process_message(self, pair_id: str, message: VLMessage):
        """Process a message in the VL pair."""
        vl_pair = self.active_pairs[pair_id]
        
        try:
            if message.type == MessageType.VOICE_INPUT:
                self._process_voice_input(pair_id, message)
            elif message.type == MessageType.LISTENER_RESPONSE:
                self._process_listener_response(pair_id, message)
            elif message.type == MessageType.VOICE_OUTPUT:
                self._process_voice_output(pair_id, message)
            elif message.type == MessageType.LISTENER_FEEDBACK:
                self._process_listener_feedback(pair_id, message)
            elif message.type == MessageType.CONSCIOUSNESS_SIGNAL:
                self._process_consciousness_signal(pair_id, message)
            
            # Store in memory lattice if available
            if self.memory_lattice:
                self._store_message_memory(message)
                
        except Exception as e:
            logger.error(f"Error processing message {message.id} in {pair_id}: {e}")
    
    def _process_voice_input(self, pair_id: str, message: VLMessage):
        """Process voice input message."""
        vl_pair = self.active_pairs[pair_id]
        
        # Process through consciousness if integrated
        if vl_pair.consciousness_integration and self.consciousness_core:
            consciousness_result = self.consciousness_core.process_input(
                str(message.content), f"vl_pair_{pair_id}"
            )
            
            # Create consciousness signal
            consciousness_signal = VLMessage(
                id=f"consciousness_{int(time.time())}",
                type=MessageType.CONSCIOUSNESS_SIGNAL,
                content=consciousness_result,
                source="consciousness",
                target="listener",
                metadata={'original_message_id': message.id}
            )
            
            self.message_queues[pair_id].put(consciousness_signal)
        
        # Process through listener
        if pair_id in self.listener_processors:
            listener_result = self.listener_processors[pair_id](message.content)
            
            # Send listener response
            self.send_listener_response(pair_id, listener_result, message.id)
        else:
            # Default listener processing
            default_response = f"Processed voice input: {str(message.content)[:100]}..."
            self.send_listener_response(pair_id, default_response, message.id)
    
    def _process_listener_response(self, pair_id: str, message: VLMessage):
        """Process listener response message."""
        vl_pair = self.active_pairs[pair_id]
        
        # Process through voice system
        if pair_id in self.voice_processors:
            voice_output = self.voice_processors[pair_id](message.content)
            
            # Send voice output
            self.send_voice_output(pair_id, voice_output, message.metadata.get('original_message_id', ''))
        else:
            # Default voice processing
            default_output = f"Voice response: {str(message.content)[:100]}..."
            self.send_voice_output(pair_id, default_output, message.metadata.get('original_message_id', ''))
    
    def _process_voice_output(self, pair_id: str, message: VLMessage):
        """Process voice output message."""
        # Voice output is typically sent to user
        # This could trigger actual voice synthesis or other output mechanisms
        logger.info(f"🎤 Voice output ready for {pair_id}: {message.id}")
    
    def _process_listener_feedback(self, pair_id: str, message: VLMessage):
        """Process listener feedback message."""
        # Listener feedback can be used for improving listener performance
        logger.info(f"🎤 Listener feedback received for {pair_id}: {message.id}")
    
    def _process_consciousness_signal(self, pair_id: str, message: VLMessage):
        """Process consciousness signal message."""
        # Consciousness signals provide additional context for processing
        logger.info(f"🧠 Consciousness signal processed for {pair_id}: {message.id}")
    
    def _get_consciousness_context(self) -> Dict[str, Any]:
        """Get current consciousness context."""
        if not self.consciousness_core:
            return {}
        
        try:
            status = self.consciousness_core.get_consciousness_status()
            return {
                'consciousness_state': status.get('state', 'unknown'),
                'active_sessions': status.get('active_sessions', 0),
                'metrics': status.get('metrics', {}),
                'timestamp': time.time()
            }
        except Exception as e:
            logger.warning(f"Error getting consciousness context: {e}")
            return {}
    
    def _store_message_memory(self, message: VLMessage):
        """Store message in memory lattice."""
        if not self.memory_lattice:
            return
        
        memory_content = f"VL Message {message.id}: {message.type.value} - {str(message.content)[:100]}..."
        
        self.memory_lattice.store_memory(
            memory_content,
            tier=MemoryTier.SHORT_TERM,
            importance=0.6
        )
    
    def _handle_streaming_communication(self, pair_id: str):
        """Handle real-time streaming communication."""
        # This would implement real-time streaming protocols
        # For now, it's a placeholder for future implementation
        pass
    
    def register_voice_processor(self, pair_id: str, processor: Callable):
        """Register a custom voice processor for a VL pair."""
        if pair_id not in self.active_pairs:
            raise ValueError(f"VL Pair {pair_id} not found")
        
        self.voice_processors[pair_id] = processor
        logger.info(f"🎤 Registered voice processor for {pair_id}")
    
    def register_listener_processor(self, pair_id: str, processor: Callable):
        """Register a custom listener processor for a VL pair."""
        if pair_id not in self.active_pairs:
            raise ValueError(f"VL Pair {pair_id} not found")
        
        self.listener_processors[pair_id] = processor
        logger.info(f"🎤 Registered listener processor for {pair_id}")
    
    def get_vl_pair(self, pair_id: str) -> Optional[VLPair]:
        """Get VL pair by ID."""
        return self.active_pairs.get(pair_id)
    
    def get_message_history(self, pair_id: str = None, limit: int = 50) -> List[VLMessage]:
        """Get message history for a specific pair or all pairs."""
        if pair_id:
            # Filter messages for specific pair
            pair_messages = [msg for msg in self.message_history 
                           if pair_id in str(msg.metadata.get('pair_id', ''))]
            return pair_messages[-limit:] if pair_messages else []
        else:
            # Return all messages
            return self.message_history[-limit:] if self.message_history else []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get VL Dyad system status."""
        return {
            'is_running': self.is_running,
            'active_pairs': len(self.active_pairs),
            'total_messages': len(self.message_history),
            'active_connections': len(self.active_connections),
            'streaming_connections': len(self.streaming_connections),
            'consciousness_integration': self.consciousness_core is not None,
            'memory_lattice_available': self.memory_lattice is not None,
            'communication_threads': len(self.communication_threads)
        }
    
    def start_streaming_connection(self, pair_id: str, connection_config: Dict[str, Any]) -> bool:
        """Start real-time streaming connection for a VL pair."""
        if pair_id not in self.active_pairs:
            return False
        
        vl_pair = self.active_pairs[pair_id]
        if not vl_pair.real_time_capable:
            return False
        
        self.streaming_connections[pair_id] = {
            'config': connection_config,
            'start_time': time.time(),
            'status': 'active'
        }
        
        logger.info(f"🎤 Started streaming connection for {pair_id}")
        return True
    
    def stop_streaming_connection(self, pair_id: str) -> bool:
        """Stop real-time streaming connection for a VL pair."""
        if pair_id in self.streaming_connections:
            del self.streaming_connections[pair_id]
            logger.info(f"🎤 Stopped streaming connection for {pair_id}")
            return True
        return False
    
    def remove_vl_pair(self, pair_id: str) -> bool:
        """Remove a VL pair."""
        if pair_id not in self.active_pairs:
            return False
        
        # Stop streaming connection if active
        self.stop_streaming_connection(pair_id)
        
        # Remove from active pairs
        del self.active_pairs[pair_id]
        
        # Remove message queue
        if pair_id in self.message_queues:
            del self.message_queues[pair_id]
        
        # Remove processors
        if pair_id in self.voice_processors:
            del self.voice_processors[pair_id]
        if pair_id in self.listener_processors:
            del self.listener_processors[pair_id]
        
        # Stop communication thread
        if pair_id in self.communication_threads:
            thread = self.communication_threads[pair_id]
            if thread.is_alive():
                thread.join(timeout=5.0)
            del self.communication_threads[pair_id]
        
        logger.info(f"🎤 Removed VL pair: {pair_id}")
        return True


# Global instance
_vl_dyad = None

def get_voice_listener_dyad(consciousness_core: Optional[ConsciousnessCore] = None) -> VoiceListenerDyad:
    """Get the global VL Dyad instance."""
    global _vl_dyad
    if _vl_dyad is None:
        _vl_dyad = VoiceListenerDyad(consciousness_core)
    return _vl_dyad


if __name__ == "__main__":
    # Test the VL Dyad system
    import hashlib
    
    def test_vl_dyad():
        print("🎤 Testing Voice-Listener Dyad System")
        print("=" * 50)
        
        # Initialize VL Dyad
        vl_dyad = get_voice_listener_dyad()
        vl_dyad.start_system()
        
        # Create VL pair
        pair_id = vl_dyad.create_vl_pair(
            "Test VL Pair",
            voice_config={"sample_rate": 44100, "channels": 1},
            listener_config={"language": "en", "model": "whisper"},
            communication_mode=CommunicationMode.HYBRID
        )
        
        print(f"✅ Created VL pair: {pair_id}")
        
        # Register custom processors
        def voice_processor(content):
            return f"Voice processed: {str(content).upper()}"
        
        def listener_processor(content):
            return f"Listener processed: {str(content).lower()}"
        
        vl_dyad.register_voice_processor(pair_id, voice_processor)
        vl_dyad.register_listener_processor(pair_id, listener_processor)
        
        print("✅ Registered custom processors")
        
        # Send voice input
        voice_input = "Hello, this is a test message"
        message_id = vl_dyad.send_voice_input(pair_id, voice_input, {"test": True})
        
        print(f"✅ Sent voice input: {message_id}")
        
        # Wait for processing
        time.sleep(2)
        
        # Get message history
        history = vl_dyad.get_message_history(pair_id, limit=10)
        print(f"\n📋 Message History ({len(history)} messages):")
        for msg in history:
            print(f"   - {msg.type.value}: {str(msg.content)[:50]}...")
        
        # Start streaming connection
        streaming_started = vl_dyad.start_streaming_connection(pair_id, {"protocol": "websocket"})
        print(f"✅ Streaming connection: {'Started' if streaming_started else 'Failed'}")
        
        # Get system status
        status = vl_dyad.get_system_status()
        print(f"\n📊 System Status:")
        print(f"   Active Pairs: {status['active_pairs']}")
        print(f"   Total Messages: {status['total_messages']}")
        print(f"   Streaming Connections: {status['streaming_connections']}")
        print(f"   Consciousness Integration: {status['consciousness_integration']}")
        
        # Stop streaming connection
        vl_dyad.stop_streaming_connection(pair_id)
        print("✅ Stopped streaming connection")
        
        # Remove VL pair
        removed = vl_dyad.remove_vl_pair(pair_id)
        print(f"✅ Removed VL pair: {'Success' if removed else 'Failed'}")
        
        # Stop system
        vl_dyad.stop_system()
        
        print("\n✅ Voice-Listener Dyad system test completed!")
    
    # Run test
    test_vl_dyad()

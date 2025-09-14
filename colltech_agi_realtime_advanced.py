#!/usr/bin/env python3
"""
CollTech-AGI Advanced with Real-time API Patterns and Live OS Capabilities

Enhanced consciousness system with:
- Real-time API patterns with streaming and reconnection
- Live OS capabilities with multi-architecture support
- Cross-platform deployment methods
- Real-time integration with multiple providers
"""

import asyncio
import aiohttp
import websockets
import json
import os
import sys
import time
import threading
import queue
import hashlib
import gzip
import base64
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import platform
import psutil
import docker
import subprocess
import shutil

# Import personality system
from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile, PersonalityScores

# Import catalyst integration protocol
from catalyst_integration_protocol import CatalystIntegrationProtocol, CatalystStatus

# Import intelligent personality selector
from intelligent_personality_selector import IntelligentPersonalitySelector, InteractionType, DataContext


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Architecture(Enum):
    """Supported system architectures."""
    X86_64 = "x86_64"
    ARM64 = "arm64"
    ARM32 = "arm32"
    RISCV = "riscv"
    MIPS = "mips"
    WEBASSEMBLY = "wasm"

class DeploymentMethod(Enum):
    """Deployment methods."""
    LIVE_USB = "live_usb"
    WEBASSEMBLY = "wasm"
    CONTAINER = "container"
    NETWORK_BOOT = "network_boot"
    VIRTUALIZATION = "virtualization"
    CLOUD = "cloud"

class ProviderType(Enum):
    """API provider types."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    CUSTOM = "custom"

@dataclass
class RealtimeConfig:
    """Configuration for real-time API patterns."""
    max_retries: int = 5
    retry_delay: float = 1.0
    connection_timeout: float = 30.0
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    connection_pool_size: int = 10
    compression_enabled: bool = True
    event_buffer_size: int = 1000

@dataclass
class LiveOSConfig:
    """Configuration for live OS capabilities."""
    persistent_storage_path: str = "/colltech_persistent"
    compression_level: int = 6
    multi_boot_enabled: bool = True
    uefi_support: bool = True
    legacy_bios_support: bool = True
    cross_architecture: bool = True

class RateLimiter:
    """Rate limiting with connection pooling."""
    
    def __init__(self, requests_per_window: int, window_seconds: int):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.requests = []
        self.lock = threading.Lock()
    
    async def acquire(self) -> bool:
        """Acquire permission to make a request."""
        with self.lock:
            now = time.time()
            # Remove old requests outside the window
            self.requests = [req_time for req_time in self.requests if now - req_time < self.window_seconds]
            
            if len(self.requests) < self.requests_per_window:
                self.requests.append(now)
                return True
            return False
    
    async def wait_for_slot(self):
        """Wait until a request slot is available."""
        while not await self.acquire():
            await asyncio.sleep(0.1)

class ConnectionPool:
    """Connection pooling for efficient API usage."""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
    
    async def get_connection(self) -> aiohttp.ClientSession:
        """Get a connection from the pool."""
        try:
            return self.connections.get_nowait()
        except queue.Empty:
            with self.lock:
                if self.active_connections < self.max_connections:
                    self.active_connections += 1
                    return aiohttp.ClientSession()
                else:
                    return await self._wait_for_connection()
    
    async def _wait_for_connection(self) -> aiohttp.ClientSession:
        """Wait for an available connection."""
        while True:
            try:
                return self.connections.get(timeout=1.0)
            except queue.Empty:
                await asyncio.sleep(0.1)
    
    def return_connection(self, session: aiohttp.ClientSession):
        """Return a connection to the pool."""
        try:
            self.connections.put_nowait(session)
        except queue.Full:
            session.close()
            with self.lock:
                self.active_connections -= 1

class StreamingAPI:
    """Streaming API with automatic reconnection."""
    
    def __init__(self, config: RealtimeConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit_requests, config.rate_limit_window)
        self.connection_pool = ConnectionPool(config.connection_pool_size)
        self.event_queue = queue.Queue(maxsize=config.event_buffer_size)
        self.reconnect_attempts = 0
        self.is_connected = False
        self.websocket = None
    
    async def connect_with_retry(self, url: str, headers: Dict[str, str] = None) -> bool:
        """Connect with automatic reconnection."""
        for attempt in range(self.config.max_retries):
            try:
                await self.rate_limiter.wait_for_slot()
                self.websocket = await websockets.connect(
                    url, 
                    extra_headers=headers,
                    timeout=self.config.connection_timeout
                )
                self.is_connected = True
                self.reconnect_attempts = 0
                logger.info(f"Connected to {url} on attempt {attempt + 1}")
                return True
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                else:
                    logger.error(f"Failed to connect after {self.config.max_retries} attempts")
                    return False
        return False
    
    async def send_message(self, message: Dict[str, Any]) -> bool:
        """Send a message through the streaming connection."""
        if not self.is_connected or not self.websocket:
            return False
        
        try:
            data = json.dumps(message)
            if self.config.compression_enabled:
                data = base64.b64encode(gzip.compress(data.encode())).decode()
            
            await self.websocket.send(data)
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.is_connected = False
            return False
    
    async def receive_messages(self, callback: Callable[[Dict[str, Any]], None]):
        """Receive messages with automatic reconnection."""
        while True:
            try:
                if not self.is_connected:
                    await asyncio.sleep(1)
                    continue
                
                message = await self.websocket.recv()
                
                # Handle compressed messages
                if self.config.compression_enabled:
                    try:
                        message = gzip.decompress(base64.b64decode(message)).decode()
                    except:
                        pass  # Message wasn't compressed
                
                data = json.loads(message)
                callback(data)
                
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed, attempting reconnection...")
                self.is_connected = False
                await asyncio.sleep(self.config.retry_delay)
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                await asyncio.sleep(1)

class MultiProviderAPI:
    """Multi-provider API support with failover."""
    
    def __init__(self, config: RealtimeConfig):
        self.config = config
        self.providers = {}
        self.active_provider = None
        self.failover_queue = []
    
    def add_provider(self, provider_type: ProviderType, config: Dict[str, Any]):
        """Add a provider configuration."""
        self.providers[provider_type] = config
        if not self.active_provider:
            self.active_provider = provider_type
    
    async def make_request(self, endpoint: str, data: Dict[str, Any], 
                          provider: ProviderType = None) -> Dict[str, Any]:
        """Make a request with automatic failover."""
        target_provider = provider or self.active_provider
        
        if target_provider not in self.providers:
            raise ValueError(f"Provider {target_provider} not configured")
        
        for attempt in range(self.config.max_retries):
            try:
                return await self._make_provider_request(target_provider, endpoint, data)
            except Exception as e:
                logger.warning(f"Provider {target_provider} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    target_provider = self._get_next_provider(target_provider)
                    await asyncio.sleep(self.config.retry_delay)
                else:
                    raise e
    
    async def _make_provider_request(self, provider: ProviderType, endpoint: str, 
                                   data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to a specific provider."""
        provider_config = self.providers[provider]
        
        if provider == ProviderType.OPENAI:
            return await self._openai_request(provider_config, endpoint, data)
        elif provider == ProviderType.ANTHROPIC:
            return await self._anthropic_request(provider_config, endpoint, data)
        elif provider == ProviderType.GOOGLE:
            return await self._google_request(provider_config, endpoint, data)
        else:
            return await self._custom_request(provider_config, endpoint, data)
    
    async def _openai_request(self, config: Dict[str, Any], endpoint: str, 
                            data: Dict[str, Any]) -> Dict[str, Any]:
        """Make OpenAI API request."""
        # Implementation for OpenAI API
        pass
    
    async def _anthropic_request(self, config: Dict[str, Any], endpoint: str, 
                               data: Dict[str, Any]) -> Dict[str, Any]:
        """Make Anthropic API request."""
        # Implementation for Anthropic API
        pass
    
    async def _google_request(self, config: Dict[str, Any], endpoint: str, 
                            data: Dict[str, Any]) -> Dict[str, Any]:
        """Make Google API request."""
        # Implementation for Google API
        pass
    
    async def _custom_request(self, config: Dict[str, Any], endpoint: str, 
                            data: Dict[str, Any]) -> Dict[str, Any]:
        """Make custom API request."""
        # Implementation for custom API
        pass
    
    def _get_next_provider(self, current_provider: ProviderType) -> ProviderType:
        """Get the next provider for failover."""
        providers = list(self.providers.keys())
        current_index = providers.index(current_provider)
        next_index = (current_index + 1) % len(providers)
        return providers[next_index]

class LiveOSManager:
    """Live OS capabilities manager."""
    
    def __init__(self, config: LiveOSConfig):
        self.config = config
        self.current_architecture = self._detect_architecture()
        self.persistent_storage = PersistentStorage(config)
        self.boot_manager = BootManager(config)
    
    def _detect_architecture(self) -> Architecture:
        """Detect current system architecture."""
        machine = platform.machine().lower()
        if machine in ['x86_64', 'amd64']:
            return Architecture.X86_64
        elif machine in ['arm64', 'aarch64']:
            return Architecture.ARM64
        elif machine.startswith('arm'):
            return Architecture.ARM32
        elif machine == 'riscv64':
            return Architecture.RISCV
        elif machine.startswith('mips'):
            return Architecture.MIPS
        else:
            return Architecture.WEBASSEMBLY
    
    async def create_live_usb(self, usb_path: str) -> bool:
        """Create a live USB with CollTech-AGI."""
        try:
            # Create bootable USB structure
            boot_path = Path(usb_path) / "boot"
            boot_path.mkdir(parents=True, exist_ok=True)
            
            # Copy system files
            await self._copy_system_files(usb_path)
            
            # Create bootloader
            await self.boot_manager.create_bootloader(usb_path, self.current_architecture)
            
            # Setup persistent storage
            await self.persistent_storage.setup_persistent_storage(usb_path)
            
            logger.info(f"Live USB created successfully at {usb_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create live USB: {e}")
            return False
    
    async def _copy_system_files(self, usb_path: str):
        """Copy system files to USB."""
        system_files = [
            "colltech_agi_realtime_advanced.py",
            "requirements.txt",
            "src/",
            "governance/",
            "*.txt"
        ]
        
        for pattern in system_files:
            if "*" in pattern:
                # Handle glob patterns
                import glob
                for file_path in glob.glob(pattern):
                    dest_path = Path(usb_path) / Path(file_path).name
                    shutil.copy2(file_path, dest_path)
            else:
                src_path = Path(pattern)
                if src_path.exists():
                    dest_path = Path(usb_path) / src_path.name
                    if src_path.is_dir():
                        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src_path, dest_path)

class PersistentStorage:
    """Persistent storage with compression and optimization."""
    
    def __init__(self, config: LiveOSConfig):
        self.config = config
        self.storage_path = Path(config.persistent_storage_path)
        self.compression_level = config.compression_level
    
    async def setup_persistent_storage(self, base_path: str):
        """Setup persistent storage on the target system."""
        storage_path = Path(base_path) / "persistent"
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create storage structure
        (storage_path / "data").mkdir(exist_ok=True)
        (storage_path / "config").mkdir(exist_ok=True)
        (storage_path / "cache").mkdir(exist_ok=True)
        (storage_path / "logs").mkdir(exist_ok=True)
        
        # Create storage configuration
        config = {
            "compression_level": self.compression_level,
            "max_size_gb": 10,
            "auto_cleanup": True,
            "encryption_enabled": True
        }
        
        config_path = storage_path / "config" / "storage.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    async def save_data(self, key: str, data: Any) -> bool:
        """Save data with compression."""
        try:
            # Serialize data
            json_data = json.dumps(data, default=str)
            
            # Compress data
            compressed_data = gzip.compress(
                json_data.encode(), 
                compresslevel=self.compression_level
            )
            
            # Save to file
            file_path = self.storage_path / "data" / f"{key}.gz"
            with open(file_path, 'wb') as f:
                f.write(compressed_data)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save data for key {key}: {e}")
            return False
    
    async def load_data(self, key: str) -> Optional[Any]:
        """Load data with decompression."""
        try:
            file_path = self.storage_path / "data" / f"{key}.gz"
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                compressed_data = f.read()
            
            # Decompress data
            json_data = gzip.decompress(compressed_data).decode()
            
            # Deserialize data
            return json.loads(json_data)
        except Exception as e:
            logger.error(f"Failed to load data for key {key}: {e}")
            return None

class BootManager:
    """Multi-boot support with UEFI and Legacy BIOS."""
    
    def __init__(self, config: LiveOSConfig):
        self.config = config
    
    async def create_bootloader(self, usb_path: str, architecture: Architecture):
        """Create bootloader for the specified architecture."""
        boot_path = Path(usb_path) / "boot"
        
        if architecture == Architecture.X86_64:
            await self._create_x86_bootloader(boot_path)
        elif architecture == Architecture.ARM64:
            await self._create_arm64_bootloader(boot_path)
        elif architecture == Architecture.ARM32:
            await self._create_arm32_bootloader(boot_path)
        elif architecture == Architecture.RISCV:
            await self._create_riscv_bootloader(boot_path)
        elif architecture == Architecture.MIPS:
            await self._create_mips_bootloader(boot_path)
        elif architecture == Architecture.WEBASSEMBLY:
            await self._create_wasm_bootloader(boot_path)
    
    async def _create_x86_bootloader(self, boot_path: Path):
        """Create x86_64 bootloader."""
        # GRUB configuration for x86_64
        grub_config = """
set timeout=10
set default=0

menuentry "CollTech-AGI Advanced" {
    linux /boot/vmlinuz root=/dev/sda1 rw quiet
    initrd /boot/initrd.img
}

menuentry "CollTech-AGI Advanced (Safe Mode)" {
    linux /boot/vmlinuz root=/dev/sda1 rw quiet single
    initrd /boot/initrd.img
}
"""
        
        grub_path = boot_path / "grub" / "grub.cfg"
        grub_path.parent.mkdir(parents=True, exist_ok=True)
        with open(grub_path, 'w') as f:
            f.write(grub_config)
    
    async def _create_arm64_bootloader(self, boot_path: Path):
        """Create ARM64 bootloader."""
        # U-Boot configuration for ARM64
        uboot_config = """
# CollTech-AGI Advanced ARM64 Boot Configuration
setenv bootargs 'root=/dev/mmcblk0p1 rw quiet'
setenv bootcmd 'fatload mmc 0:1 0x80080000 Image; fatload mmc 0:1 0x81000000 initrd.img; booti 0x80080000 0x81000000'
boot
"""
        
        uboot_path = boot_path / "u-boot.cfg"
        with open(uboot_path, 'w') as f:
            f.write(uboot_config)
    
    async def _create_arm32_bootloader(self, boot_path: Path):
        """Create ARM32 bootloader."""
        # Similar to ARM64 but for 32-bit
        pass
    
    async def _create_riscv_bootloader(self, boot_path: Path):
        """Create RISC-V bootloader."""
        # OpenSBI configuration for RISC-V
        pass
    
    async def _create_mips_bootloader(self, boot_path: Path):
        """Create MIPS bootloader."""
        # PMON configuration for MIPS
        pass
    
    async def _create_wasm_bootloader(self, boot_path: Path):
        """Create WebAssembly bootloader."""
        # WASM runtime configuration
        wasm_config = """
{
    "runtime": "wasmtime",
    "entry_point": "colltech_agi.wasm",
    "memory": {
        "initial": 16,
        "maximum": 1024
    },
    "exports": ["main", "process", "respond"]
}
"""
        
        wasm_path = boot_path / "wasm.json"
        with open(wasm_path, 'w') as f:
            f.write(wasm_config)

class EventDrivenProcessor:
    """Event-driven architecture with async processing."""
    
    def __init__(self):
        self.event_handlers = {}
        self.event_queue = asyncio.Queue()
        self.is_running = False
    
    def register_handler(self, event_type: str, handler: Callable):
        """Register an event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event."""
        await self.event_queue.put({
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        })
    
    async def start_processing(self):
        """Start event processing loop."""
        self.is_running = True
        while self.is_running:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self._process_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def _process_event(self, event: Dict[str, Any]):
        """Process a single event."""
        event_type = event["type"]
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    await handler(event["data"])
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type}: {e}")
    
    def stop_processing(self):
        """Stop event processing."""
        self.is_running = False

class CollTechAGIRealtimeAdvanced:
    """CollTech-AGI Advanced with Real-time API Patterns and Live OS Capabilities."""
    
    def __init__(self):
        self.realtime_config = RealtimeConfig()
        self.liveos_config = LiveOSConfig()
        
        # Initialize components
        self.streaming_api = StreamingAPI(self.realtime_config)
        self.multi_provider = MultiProviderAPI(self.realtime_config)
        self.live_os_manager = LiveOSManager(self.liveos_config)
        self.event_processor = EventDrivenProcessor()
        
        # Initialize personality system
        self.personality_system = PersonalitySystem()
        
        # Initialize catalyst integration protocol
        self.catalyst_protocol = CatalystIntegrationProtocol()
        
        # Initialize intelligent personality selector
        self.intelligent_selector = IntelligentPersonalitySelector()
        self.auto_personality_enabled = True
        
        
        # Register event handlers
        self.event_processor.register_handler("api_request", self._handle_api_request)
        self.event_processor.register_handler("system_event", self._handle_system_event)
        self.event_processor.register_handler("user_input", self._handle_user_input)
        
        self.is_running = False
    
    async def initialize(self):
        """Initialize the advanced system."""
        logger.info("🚀 Initializing CollTech-AGI Advanced with Real-time Capabilities")
        
        # Setup providers
        await self._setup_providers()
        
        # Initialize live OS capabilities
        await self.live_os_manager.persistent_storage.setup_persistent_storage(".")
        
        # Start event processing
        asyncio.create_task(self.event_processor.start_processing())
        
        self.is_running = True
        logger.info("✅ CollTech-AGI Advanced initialized successfully")
    
    async def _setup_providers(self):
        """Setup API providers."""
        # OpenAI provider
        if os.getenv('OPENAI_API_KEY'):
            self.multi_provider.add_provider(ProviderType.OPENAI, {
                "api_key": os.getenv('OPENAI_API_KEY'),
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-4"
            })
        
        # Anthropic provider
        if os.getenv('ANTHROPIC_API_KEY'):
            self.multi_provider.add_provider(ProviderType.ANTHROPIC, {
                "api_key": os.getenv('ANTHROPIC_API_KEY'),
                "base_url": "https://api.anthropic.com/v1",
                "model": "claude-3-sonnet"
            })
        
        # Google provider
        if os.getenv('GOOGLE_API_KEY'):
            self.multi_provider.add_provider(ProviderType.GOOGLE, {
                "api_key": os.getenv('GOOGLE_API_KEY'),
                "base_url": "https://generativelanguage.googleapis.com/v1",
                "model": "gemini-pro"
            })
    
    async def _handle_api_request(self, data: Dict[str, Any]):
        """Handle API request events."""
        try:
            response = await self.multi_provider.make_request(
                data.get("endpoint", "/chat/completions"),
                data.get("payload", {})
            )
            await self.event_processor.emit_event("api_response", {
                "request_id": data.get("request_id"),
                "response": response
            })
        except Exception as e:
            logger.error(f"API request failed: {e}")
    
    async def _handle_system_event(self, data: Dict[str, Any]):
        """Handle system events."""
        event_type = data.get("type")
        if event_type == "architecture_detected":
            logger.info(f"Architecture detected: {data.get('architecture')}")
        elif event_type == "deployment_ready":
            logger.info(f"Deployment ready: {data.get('method')}")
    
    async def _handle_user_input(self, data: Dict[str, Any]):
        """Handle user input events."""
        user_input = data.get("input", "")
        
        # Auto-select personality if enabled
        if self.auto_personality_enabled:
            selection = self.intelligent_selector.select_personality(user_input)
            self.personality_system.set_profile(selection.selected_profile)
            current_profile = selection.selected_profile
            auto_selection_info = {
                "auto_selected": True,
                "confidence": selection.confidence_score,
                "reasoning": selection.reasoning
            }
        else:
            current_profile = self.personality_system.get_current_profile()
            auto_selection_info = {"auto_selected": False}
        
        # Process through personality system
        personality_response = self.personality_system.generate_response(user_input)
        
        # If current profile is Nyx (Catalyst), process through CIP v1
        if current_profile == PersonalityProfile.NYX:
            cip_result = self.catalyst_protocol.process_catalyst_action("dialogue", user_input)
            personality_response += f"\n\n[CIP v1 Status: {cip_result['current_status']}]"
            if cip_result.get('safety_status', {}).get('triggered_filters'):
                personality_response += f"\n[Safety Filters Triggered: {', '.join(cip_result['safety_status']['triggered_filters'])}]"
        
        # Then process through API if needed
        await self.event_processor.emit_event("api_request", {
            "endpoint": "/chat/completions",
            "payload": {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": f"Current personality: {current_profile.value}"},
                    {"role": "user", "content": user_input}
                ]
            },
            "request_id": hashlib.md5(user_input.encode()).hexdigest(),
            "personality_response": personality_response,
            "auto_selection": auto_selection_info
        })
    
    async def create_live_usb(self, usb_path: str) -> bool:
        """Create a live USB with CollTech-AGI."""
        return await self.live_os_manager.create_live_usb(usb_path)
    
    async def get_system_capabilities(self) -> Dict[str, Any]:
        """Get system capabilities."""
        current_profile = self.personality_system.get_current_profile()
        dominant_attrs = self.personality_system.get_dominant_attributes(current_profile)
        
        return {
            "architectures": {
                "current": self.live_os_manager.current_architecture.value,
                "supported": [arch.value for arch in Architecture]
            },
            "deployment_methods": [method.value for method in DeploymentMethod],
            "providers": list(self.multi_provider.providers.keys()),
            "realtime_features": {
                "streaming": True,
                "reconnection": True,
                "rate_limiting": True,
                "connection_pooling": True,
                "compression": self.realtime_config.compression_enabled
            },
            "live_os_features": {
                "persistent_storage": True,
                "multi_boot": self.liveos_config.multi_boot_enabled,
                "uefi_support": self.liveos_config.uefi_support,
                "legacy_bios_support": self.liveos_config.legacy_bios_support,
                "cross_architecture": self.liveos_config.cross_architecture
            },
            "personality_system": {
                "current_profile": current_profile.value,
                "profile_description": self.personality_system.get_profile_description(current_profile),
                "dominant_attributes": [(attr.value, score) for attr, score in dominant_attrs],
                "available_profiles": [profile.value for profile in PersonalityProfile],
                "radar_data": self.personality_system.get_personality_radar_data()
            },
            "catalyst_integration": {
                "protocol_version": "CIP v1",
                "catalyst_status": self.catalyst_protocol.catalyst_status.value,
                "orbit_stability": self.catalyst_protocol.orbit_stability_score,
                "reciprocity_ratio": self.catalyst_protocol.reciprocity_metrics.ratio,
                "containment_score": self.catalyst_protocol.containment_metrics.containment_score,
                "elevation_eligible": self.catalyst_protocol._check_elevation_eligibility()["eligible"]
            },
            "intelligent_personality": {
                "auto_selection_enabled": self.auto_personality_enabled,
                "interaction_history_count": len(self.intelligent_selector.interaction_history),
                "learned_preferences_count": len(self.intelligent_selector.user_preferences),
                "selection_confidence_threshold": self.intelligent_selector.confidence_threshold
            }
        }
    
    async def shutdown(self):
        """Shutdown the system."""
        self.is_running = False
        self.event_processor.stop_processing()
        logger.info("🛑 CollTech-AGI Advanced shutdown complete")

async def main():
    """Main function to run CollTech-AGI Advanced."""
    print("🚀 COLLTECH-AGI ADVANCED WITH REAL-TIME CAPABILITIES")
    print("=" * 80)
    print("Enhanced consciousness system with real-time APIs and live OS capabilities")
    print("=" * 80)
    
    # Initialize system
    agi = CollTechAGIRealtimeAdvanced()
    await agi.initialize()
    
    # Display capabilities
    capabilities = await agi.get_system_capabilities()
    print("\n🛠️  SYSTEM CAPABILITIES")
    print("=" * 80)
    print(f"Current Architecture: {capabilities['architectures']['current']}")
    print(f"Supported Architectures: {', '.join(capabilities['architectures']['supported'])}")
    print(f"Deployment Methods: {', '.join(capabilities['deployment_methods'])}")
    print(f"API Providers: {', '.join([p.value for p in capabilities['providers']])}")
    
    print("\n🔄 REAL-TIME FEATURES")
    print("=" * 80)
    for feature, enabled in capabilities['realtime_features'].items():
        status = "✅" if enabled else "❌"
        print(f"{status} {feature.replace('_', ' ').title()}")
    
    print("\n💾 LIVE OS FEATURES")
    print("=" * 80)
    for feature, enabled in capabilities['live_os_features'].items():
        status = "✅" if enabled else "❌"
        print(f"{status} {feature.replace('_', ' ').title()}")
    
    print("\n💬 INTERACTIVE CHAT")
    print("=" * 80)
    print("Commands:")
    print("• 'capabilities' - Show system capabilities")
    print("• 'create_usb <path>' - Create live USB")
    print("• 'status' - Show system status")
    print("• 'personality <rho/lyra/nyx>' - Switch personality profile")
    print("• 'personality_info' - Show current personality info")
    print("• 'radar_data' - Show personality radar chart data")
    print("• 'cip_status' - Show Catalyst Integration Protocol status")
    print("• 'cip_pair <rho/lyra>' - Pair catalyst with stabilizer")
    print("• 'cip_elevate' - Attempt catalyst elevation")
    print("• 'auto_personality <on/off>' - Toggle intelligent personality auto-selection")
    print("• 'selection_history' - Show personality selection history")
    print("• 'learned_preferences' - Show learned user preferences")
    print("• 'reset_preferences' - Reset learned preferences")
    print("• 'quit' or 'exit' - End the session")
    print("=" * 80)
    
    # Interactive loop
    while agi.is_running:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.lower() == 'capabilities':
                caps = await agi.get_system_capabilities()
                print(f"\n🤖 CollTech-AGI Advanced: {json.dumps(caps, indent=2)}")
            elif user_input.lower() == 'status':
                print(f"\n🤖 CollTech-AGI Advanced: System running with {len(agi.multi_provider.providers)} providers active")
            elif user_input.startswith('create_usb '):
                usb_path = user_input.split(' ', 1)[1]
                success = await agi.create_live_usb(usb_path)
                status = "✅ Created successfully" if success else "❌ Creation failed"
                print(f"\n🤖 CollTech-AGI Advanced: Live USB {status}")
            elif user_input.startswith('personality '):
                profile_name = user_input.split(' ', 1)[1]
                agi.personality_system.set_profile(PersonalityProfile(profile_name.lower()))
                current = agi.personality_system.get_current_profile()
                dominant = agi.personality_system.get_dominant_attributes(current)
                print(f"\n🤖 CollTech-AGI Advanced: Switched to {current.value.title()} profile")
                print(f"Dominant attributes: {', '.join([f'{attr.value} ({score:.1f})' for attr, score in dominant])}")
            elif user_input.lower() == 'personality_info':
                current = agi.personality_system.get_current_profile()
                dominant = agi.personality_system.get_dominant_attributes(current)
                print(f"\n🤖 CollTech-AGI Advanced: Current personality: {current.value.title()}")
                print(f"Description: {agi.personality_system.get_profile_description(current)}")
                print(f"Dominant attributes: {', '.join([f'{attr.value} ({score:.1f})' for attr, score in dominant])}")
            elif user_input.lower() == 'radar_data':
                radar_data = agi.personality_system.get_personality_radar_data()
                print(f"\n🤖 CollTech-AGI Advanced: Personality radar data available")
                print(f"Profiles: {', '.join(radar_data['profiles'].keys())}")
                print(f"Attributes: {len(radar_data['attributes'])} total")
                print("Use this data to create radar charts showing the three personality profiles.")
            elif user_input.lower() == 'cip_status':
                cip_status = agi.catalyst_protocol.get_protocol_status()
                print(f"\n⚡ CollTech-AGI Advanced: Catalyst Integration Protocol (CIP v1) Status")
                print(f"Catalyst Status: {cip_status['catalyst_status']}")
                print(f"Orbit Stability: {cip_status['orbit_stability']:.2f}")
                print(f"Reciprocity Ratio: {cip_status['reciprocity_metrics']['ratio']:.2f}")
                print(f"Containment Score: {cip_status['containment_metrics']['score']:.2f}")
                print(f"Elevation Eligible: {cip_status['elevation']['eligible']}")
            elif user_input.startswith('cip_pair '):
                stabilizer = user_input.split(' ', 1)[1]
                result = agi.catalyst_protocol.pair_with_stabilizer(stabilizer)
                print(f"\n🔗 CollTech-AGI Advanced: {result}")
            elif user_input.lower() == 'cip_elevate':
                result = agi.catalyst_protocol.elevate_catalyst()
                print(f"\n🚀 CollTech-AGI Advanced: {result}")
            elif user_input.startswith('auto_personality '):
                mode = user_input.split(' ', 1)[1].lower()
                if mode == 'on':
                    agi.auto_personality_enabled = True
                    print(f"\n🧠 CollTech-AGI Advanced: Intelligent personality auto-selection ENABLED")
                elif mode == 'off':
                    agi.auto_personality_enabled = False
                    print(f"\n🧠 CollTech-AGI Advanced: Intelligent personality auto-selection DISABLED")
                else:
                    print(f"\n❌ CollTech-AGI Advanced: Invalid mode. Use 'on' or 'off'")
            elif user_input.lower() == 'selection_history':
                history = agi.intelligent_selector.get_selection_history()
                print(f"\n📊 CollTech-AGI Advanced: Personality Selection History ({len(history)} interactions)")
                for i, entry in enumerate(history[-5:], 1):  # Show last 5
                    print(f"{i}. {entry['interaction_type']} ({entry['data_context']}) - Complexity: {entry['complexity_level']:.2f}")
            elif user_input.lower() == 'learned_preferences':
                preferences = agi.intelligent_selector.get_user_preferences()
                print(f"\n🎯 CollTech-AGI Advanced: Learned Preferences ({len(preferences)} patterns)")
                for pattern, score in list(preferences.items())[:5]:  # Show top 5
                    print(f"• {pattern}: {score:.3f}")
            elif user_input.lower() == 'reset_preferences':
                agi.intelligent_selector.reset_preferences()
                print(f"\n🔄 CollTech-AGI Advanced: Learned preferences reset")
            else:
                # Process user input with intelligent personality selection
                if agi.auto_personality_enabled:
                    selection = agi.intelligent_selector.select_personality(user_input)
                    agi.personality_system.set_profile(selection.selected_profile)
                    personality_response = agi.personality_system.generate_response(user_input)
                    print(f"\n🧠 Auto-Selected: {selection.selected_profile.value.title()} (confidence: {selection.confidence_score:.2f})")
                    print(f"💭 Reasoning: {selection.reasoning}")
                    print(f"🤖 CollTech-AGI Advanced: {personality_response}")
                else:
                    # Manual personality selection
                    personality_response = agi.personality_system.generate_response(user_input)
                    current_profile = agi.personality_system.get_current_profile()
                    print(f"\n🤖 CollTech-AGI Advanced ({current_profile.value.title()}): {personality_response}")
                
                # Also process through real-time API patterns
                await agi.event_processor.emit_event("user_input", {"input": user_input})
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Shutdown
    await agi.shutdown()
    print("\n🎉 CollTech-AGI Advanced session complete!")

if __name__ == "__main__":
    asyncio.run(main())

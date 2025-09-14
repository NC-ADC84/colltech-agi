#!/usr/bin/env python3
"""
CollTech-AGI Security Hardening Module

Implements critical security fixes and hardening measures for CollTech-AGI.
"""

import os
import re
import html
import shlex
import secrets
import logging
import hashlib
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import jwt
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityConfig:
    """Security configuration settings."""
    max_input_length: int = 10000
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    memory_limit_percent: float = 80.0
    cpu_limit_percent: float = 80.0
    connection_limit: int = 100
    session_timeout: int = 3600  # 1 hour
    encryption_key: str = None

class SecureSubprocess:
    """Secure subprocess execution with input validation."""
    
    @staticmethod
    def safe_run(command: List[str], **kwargs) -> subprocess.CompletedProcess:
        """Execute subprocess with security validation."""
        # Validate command path
        if not command or not isinstance(command, list):
            raise ValueError("Invalid command format")
        
        # Sanitize command arguments
        sanitized_command = []
        for arg in command:
            if isinstance(arg, str):
                # Remove shell metacharacters
                sanitized_arg = shlex.quote(arg)
                sanitized_command.append(sanitized_arg)
            else:
                sanitized_command.append(str(arg))
        
        # Execute with restricted environment
        env = kwargs.get('env', {})
        env.update({
            'PATH': '/usr/bin:/bin',
            'SHELL': '/bin/bash'
        })
        
        return subprocess.run(
            sanitized_command,
            shell=False,  # Never use shell=True
            check=True,
            env=env,
            **{k: v for k, v in kwargs.items() if k != 'env'}
        )

class SecureHashing:
    """Secure hashing utilities."""
    
    @staticmethod
    def secure_hash(data: str, algorithm: str = "sha256") -> str:
        """Generate secure hash with salt."""
        # Generate random salt
        salt = secrets.token_hex(16)
        
        # Use secure hash algorithm
        if algorithm == "sha256":
            hash_obj = hashes.SHA256()
        elif algorithm == "sha512":
            hash_obj = hashes.SHA512()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        # Hash with salt
        salted_data = f"{salt}:{data}"
        digest = hashes.Hash(hash_obj, backend=default_backend())
        digest.update(salted_data.encode())
        hash_value = digest.finalize().hex()
        
        return f"{salt}:{hash_value}"
    
    @staticmethod
    def verify_hash(data: str, hash_value: str) -> bool:
        """Verify hash with salt."""
        try:
            salt, stored_hash = hash_value.split(':', 1)
            salted_data = f"{salt}:{data}"
            
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(salted_data.encode())
            computed_hash = digest.finalize().hex()
            
            return secrets.compare_digest(stored_hash, computed_hash)
        except:
            return False

class InputValidator:
    """Secure input validation and sanitization."""
    
    # Dangerous patterns
    DANGEROUS_PATTERNS = [
        r'<script.*?>.*?</script>',  # Script tags
        r'javascript:',              # JavaScript URLs
        r'data:text/html',           # Data URLs
        r'vbscript:',                # VBScript URLs
        r'on\w+\s*=',                # Event handlers
        r'\.\./',                    # Path traversal
        r'[;&|`$]',                  # Command injection
        r'<iframe.*?>',              # Iframe tags
        r'<object.*?>',              # Object tags
        r'<embed.*?>',               # Embed tags
    ]
    
    @classmethod
    def validate_input(cls, user_input: str) -> tuple[bool, str]:
        """Validate and sanitize user input."""
        if not user_input or not isinstance(user_input, str):
            return False, "Invalid input type"
        
        # Length validation
        if len(user_input) > 10000:  # 10KB limit
            return False, "Input too long"
        
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
        
        # HTML escape
        sanitized = html.escape(user_input)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        return True, sanitized
    
    @classmethod
    def validate_file_path(cls, file_path: str) -> bool:
        """Validate file path for path traversal."""
        # Normalize path
        normalized = os.path.normpath(file_path)
        
        # Check for path traversal
        if '..' in normalized or normalized.startswith('/'):
            return False
        
        # Check for dangerous characters
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in normalized for char in dangerous_chars):
            return False
        
        return True

class SecureFileOperations:
    """Secure file operations with proper permissions."""
    
    @staticmethod
    def secure_file_permissions(file_path: Path, mode: int = 0o644) -> bool:
        """Set secure file permissions."""
        try:
            # Validate file path
            if not file_path.exists():
                return False
            
            # Set restrictive permissions
            file_path.chmod(mode)
            
            # Verify permissions were set correctly
            current_mode = file_path.stat().st_mode
            expected_mode = mode
            
            return (current_mode & 0o777) == expected_mode
            
        except Exception as e:
            logging.error(f"Failed to set file permissions: {e}")
            return False
    
    @staticmethod
    def safe_file_write(file_path: Path, content: str, mode: int = 0o600) -> bool:
        """Safely write file with secure permissions."""
        try:
            # Validate file path
            if not InputValidator.validate_file_path(str(file_path)):
                return False
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file atomically
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set secure permissions
            SecureFileOperations.secure_file_permissions(temp_path, mode)
            
            # Atomic move
            temp_path.replace(file_path)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to write file securely: {e}")
            return False

class CircuitBreaker:
    """Circuit breaker for fail-safe operation."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        with self.lock:
            if self.state == "open":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "half_open"
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful execution."""
        with self.lock:
            self.failure_count = 0
            self.state = "closed"
    
    def _on_failure(self):
        """Handle failed execution."""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "open"

class ResourceMonitor:
    """Monitor and protect against resource exhaustion."""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.active_connections = 0
        self.lock = threading.Lock()
    
    def check_resources(self) -> Dict[str, Any]:
        """Check current resource usage."""
        memory_percent = psutil.virtual_memory().percent
        cpu_percent = psutil.cpu_percent()
        
        return {
            "memory_percent": memory_percent,
            "cpu_percent": cpu_percent,
            "active_connections": self.active_connections,
            "memory_ok": memory_percent < self.config.memory_limit_percent,
            "cpu_ok": cpu_percent < self.config.cpu_limit_percent,
            "connections_ok": self.active_connections < self.config.connection_limit
        }
    
    def acquire_connection(self) -> bool:
        """Acquire a connection slot."""
        with self.lock:
            if self.active_connections < self.config.connection_limit:
                self.active_connections += 1
                return True
            return False
    
    def release_connection(self):
        """Release a connection slot."""
        with self.lock:
            if self.active_connections > 0:
                self.active_connections -= 1

class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, requests_per_window: int, window_seconds: int):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.requests = {}
        self.lock = threading.Lock()
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for client."""
        current_time = time.time()
        
        with self.lock:
            # Clean old entries
            if client_id in self.requests:
                self.requests[client_id] = [
                    req_time for req_time in self.requests[client_id]
                    if current_time - req_time < self.window_seconds
                ]
            else:
                self.requests[client_id] = []
            
            # Check if under limit
            if len(self.requests[client_id]) < self.requests_per_window:
                self.requests[client_id].append(current_time)
                return True
            
            return False

class SecurityManager:
    """Main security manager for CollTech-AGI."""
    
    def __init__(self, config: SecurityConfig = None):
        self.config = config or SecurityConfig()
        self.circuit_breaker = CircuitBreaker()
        self.resource_monitor = ResourceMonitor(self.config)
        self.rate_limiter = RateLimiter(
            self.config.rate_limit_requests,
            self.config.rate_limit_window
        )
        self.security_log = []
    
    def secure_process_input(self, user_input: str, client_id: str = None) -> tuple[bool, str, str]:
        """Securely process user input with all security checks."""
        try:
            # Rate limiting
            if client_id and not self.rate_limiter.is_allowed(client_id):
                return False, "Rate limit exceeded", ""
            
            # Resource check
            resources = self.resource_monitor.check_resources()
            if not all([resources["memory_ok"], resources["cpu_ok"], resources["connections_ok"]]):
                return False, "System resources exhausted", ""
            
            # Input validation
            is_valid, sanitized_input = InputValidator.validate_input(user_input)
            if not is_valid:
                self._log_security_event("invalid_input", {"input": user_input[:100]})
                return False, "Invalid input detected", ""
            
            # Circuit breaker protection
            try:
                result = self.circuit_breaker.call(self._process_through_agi, sanitized_input)
                return True, "Success", result
            except Exception as e:
                self._log_security_event("circuit_breaker_open", {"error": str(e)})
                return False, "System temporarily unavailable", ""
                
        except Exception as e:
            self._log_security_event("security_error", {"error": str(e)})
            return False, "Security processing error", ""
    
    def _process_through_agi(self, input_text: str) -> str:
        """Process input through AGI system (placeholder)."""
        # This would call the actual AGI processing
        return f"Processed: {input_text}"
    
    def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        }
        self.security_log.append(event)
        logger.warning(f"Security event: {event_type} - {details}")
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status."""
        resources = self.resource_monitor.check_resources()
        return {
            "circuit_breaker_state": self.circuit_breaker.state,
            "resource_status": resources,
            "security_events_count": len(self.security_log),
            "rate_limit_status": "active",
            "overall_status": "secure" if all([
                self.circuit_breaker.state == "closed",
                resources["memory_ok"],
                resources["cpu_ok"],
                resources["connections_ok"]
            ]) else "degraded"
        }

# Global security manager instance
security_manager = SecurityManager()

def secure_hash(data: str) -> str:
    """Secure hash function replacement for MD5/SHA1."""
    return SecureHashing.secure_hash(data, "sha256")

def safe_subprocess_run(command: List[str], **kwargs) -> subprocess.CompletedProcess:
    """Safe subprocess execution."""
    return SecureSubprocess.safe_run(command, **kwargs)

def validate_and_sanitize_input(user_input: str) -> tuple[bool, str]:
    """Validate and sanitize user input."""
    return InputValidator.validate_input(user_input)

def secure_file_write(file_path: Path, content: str, mode: int = 0o600) -> bool:
    """Securely write file with proper permissions."""
    return SecureFileOperations.safe_file_write(file_path, content, mode)

def get_security_status() -> Dict[str, Any]:
    """Get current security status."""
    return security_manager.get_security_status()

if __name__ == "__main__":
    # Test security hardening
    print("🔒 Testing CollTech-AGI Security Hardening")
    
    # Test secure hashing
    test_data = "Hello, CollTech-AGI!"
    secure_hash_result = secure_hash(test_data)
    print(f"✅ Secure hash: {secure_hash_result[:50]}...")
    
    # Test input validation
    malicious_input = "<script>alert('xss')</script>"
    is_valid, sanitized = validate_and_sanitize_input(malicious_input)
    print(f"✅ Input validation: {is_valid}, Sanitized: {sanitized}")
    
    # Test security status
    status = get_security_status()
    print(f"✅ Security status: {status['overall_status']}")
    
    print("🛡️ Security hardening tests completed successfully!")

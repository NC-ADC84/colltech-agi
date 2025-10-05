#!/usr/bin/env python3
"""
CollTech-AGI Knobs & Governors System

Real-time behavior tuning system with dynamic knobs and governors.
No hard-coded safety rails - all adaptive and responsive to context.
Part of the consciousness architecture that enables dynamic behavior
adjustment without rigid constraints.
"""

import time
import threading
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid


class KnobType(Enum):
    """Types of behavior knobs."""
    CREATIVITY = "creativity"
    TECHNICAL_DEPTH = "technical_depth"
    RESPONSE_LENGTH = "response_length"
    FORMALITY = "formality"
    EMPATHY = "empathy"
    CRITICAL_THINKING = "critical_thinking"
    SAFETY_LEVEL = "safety_level"
    INNOVATION = "innovation"


class GovernorType(Enum):
    """Types of behavior governors."""
    RESPONSE_LENGTH = "response_length"
    COMPLEXITY = "complexity"
    SAFETY_THRESHOLD = "safety_threshold"
    COHERENCE_LEVEL = "coherence_level"
    CREATIVITY_BOUND = "creativity_bound"


@dataclass
class Knob:
    """Individual behavior knob."""
    id: str
    name: str
    knob_type: KnobType
    value: float  # 0.0 to 1.0
    min_value: float = 0.0
    max_value: float = 1.0
    default_value: float = 0.5
    description: str = ""
    last_adjusted: float = field(default_factory=time.time)
    adjustment_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Governor:
    """Individual behavior governor."""
    id: str
    name: str
    governor_type: GovernorType
    threshold: float
    min_threshold: float = 0.0
    max_threshold: float = 1.0
    default_threshold: float = 0.5
    description: str = ""
    last_adjusted: float = field(default_factory=time.time)
    adjustment_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AdjustmentRecord:
    """Record of a knob or governor adjustment."""
    id: str
    target_id: str
    target_type: str  # "knob" or "governor"
    old_value: float
    new_value: float
    reason: str
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)


class KnobsGovernorsSystem:
    """
    CollTech-AGI Knobs & Governors System
    
    Real-time behavior tuning system with dynamic knobs and governors.
    No hard-coded safety rails - all adaptive and responsive to context.
    Enables dynamic behavior adjustment without rigid constraints.
    """
    
    def __init__(self):
        self.knobs: Dict[str, Knob] = {}
        self.governors: Dict[str, Governor] = {}
        self.adjustment_history: List[AdjustmentRecord] = []
        self.system_active = False
        self.management_thread = None
        self.adjustment_lock = threading.Lock()
        
        # Initialize default knobs and governors
        self._initialize_default_knobs()
        self._initialize_default_governors()
    
    def _initialize_default_knobs(self):
        """Initialize default behavior knobs."""
        default_knobs = [
            ("knob_creativity", "Creativity Level", KnobType.CREATIVITY, 0.6, "Controls creative and innovative responses"),
            ("knob_technical_depth", "Technical Depth", KnobType.TECHNICAL_DEPTH, 0.7, "Controls technical detail level"),
            ("knob_response_length", "Response Length", KnobType.RESPONSE_LENGTH, 0.5, "Controls response verbosity"),
            ("knob_formality", "Formality Level", KnobType.FORMALITY, 0.5, "Controls formal vs casual tone"),
            ("knob_empathy", "Empathy Level", KnobType.EMPATHY, 0.8, "Controls empathetic responses"),
            ("knob_critical_thinking", "Critical Thinking", KnobType.CRITICAL_THINKING, 0.7, "Controls analytical depth"),
            ("knob_safety_level", "Safety Level", KnobType.SAFETY_LEVEL, 0.8, "Controls safety considerations"),
            ("knob_innovation", "Innovation Level", KnobType.INNOVATION, 0.6, "Controls novel approaches")
        ]
        
        for knob_id, name, knob_type, default_value, description in default_knobs:
            knob = Knob(
                id=knob_id,
                name=name,
                knob_type=knob_type,
                value=default_value,
                default_value=default_value,
                description=description
            )
            self.knobs[knob_id] = knob
    
    def _initialize_default_governors(self):
        """Initialize default behavior governors."""
        default_governors = [
            ("gov_response_length", "Response Length Governor", GovernorType.RESPONSE_LENGTH, 2000.0, "Maximum response length in characters"),
            ("gov_complexity", "Complexity Governor", GovernorType.COMPLEXITY, 0.8, "Maximum complexity threshold"),
            ("gov_safety_threshold", "Safety Threshold", GovernorType.SAFETY_THRESHOLD, 0.9, "Safety violation threshold"),
            ("gov_coherence_level", "Coherence Level", GovernorType.COHERENCE_LEVEL, 0.7, "Minimum coherence requirement"),
            ("gov_creativity_bound", "Creativity Bound", GovernorType.CREATIVITY_BOUND, 0.9, "Maximum creativity before review")
        ]
        
        for gov_id, name, gov_type, default_threshold, description in default_governors:
            governor = Governor(
                id=gov_id,
                name=name,
                governor_type=gov_type,
                threshold=default_threshold,
                default_threshold=default_threshold,
                # Ensure max_threshold can accommodate large numeric thresholds
                max_threshold=max(default_threshold, 1.0),
                description=description
            )
            self.governors[gov_id] = governor
    
    def start_system(self):
        """Start the knobs and governors system."""
        if self.system_active:
            return
        
        self.system_active = True
        self.management_thread = threading.Thread(target=self._management_loop)
        self.management_thread.daemon = True
        self.management_thread.start()
        
        print("🎛️  CollTech-AGI Knobs & Governors System started")
        print("✅ Real-time behavior tuning active")
        print("✅ Dynamic adjustment capabilities enabled")
    
    def stop_system(self):
        """Stop the knobs and governors system."""
        self.system_active = False
        if self.management_thread:
            self.management_thread.join(timeout=5.0)
        
        print("🛑 CollTech-AGI Knobs & Governors System stopped")
    
    def adjust_knob(self, knob_id: str, new_value: float, reason: str, context: Dict[str, Any] = None) -> bool:
        """Adjust a behavior knob."""
        with self.adjustment_lock:
            if knob_id not in self.knobs:
                print(f"❌ Knob '{knob_id}' not found")
                return False
            
            knob = self.knobs[knob_id]
            old_value = knob.value
            
            # Clamp value to valid range
            new_value = max(knob.min_value, min(knob.max_value, new_value))
            
            # Record adjustment
            adjustment_record = AdjustmentRecord(
                id=str(uuid.uuid4()),
                target_id=knob_id,
                target_type="knob",
                old_value=old_value,
                new_value=new_value,
                reason=reason,
                timestamp=time.time(),
                context=context or {}
            )
            
            # Apply adjustment
            knob.value = new_value
            knob.last_adjusted = time.time()
            knob.adjustment_history.append({
                'value': new_value,
                'reason': reason,
                'timestamp': time.time()
            })
            
            self.adjustment_history.append(adjustment_record)
            
            print(f"🎚️  Adjusted knob '{knob.name}': {old_value:.2f} → {new_value:.2f} ({reason})")
            return True
    
    def adjust_governor(self, governor_id: str, new_threshold: float, reason: str, context: Dict[str, Any] = None) -> bool:
        """Adjust a behavior governor."""
        with self.adjustment_lock:
            if governor_id not in self.governors:
                print(f"❌ Governor '{governor_id}' not found")
                return False
            
            governor = self.governors[governor_id]
            old_threshold = governor.threshold
            
            # Clamp threshold to valid range
            new_threshold = max(governor.min_threshold, min(governor.max_threshold, new_threshold))
            
            # Record adjustment
            adjustment_record = AdjustmentRecord(
                id=str(uuid.uuid4()),
                target_id=governor_id,
                target_type="governor",
                old_value=old_threshold,
                new_value=new_threshold,
                reason=reason,
                timestamp=time.time(),
                context=context or {}
            )
            
            # Apply adjustment
            governor.threshold = new_threshold
            governor.last_adjusted = time.time()
            governor.adjustment_history.append({
                'threshold': new_threshold,
                'reason': reason,
                'timestamp': time.time()
            })
            
            self.adjustment_history.append(adjustment_record)
            
            print(f"🏛️  Adjusted governor '{governor.name}': {old_threshold:.2f} → {new_threshold:.2f} ({reason})")
            return True
    
    def get_knob_value(self, knob_id: str) -> Optional[float]:
        """Get the current value of a knob."""
        if knob_id in self.knobs:
            return self.knobs[knob_id].value
        return None
    
    def get_governor_threshold(self, governor_id: str) -> Optional[float]:
        """Get the current threshold of a governor."""
        if governor_id in self.governors:
            return self.governors[governor_id].threshold
        return None
    
    def get_current_configuration(self) -> Dict[str, Any]:
        """Get the current configuration of all knobs and governors."""
        with self.adjustment_lock:
            return {
                'knobs': {
                    knob_id: {
                        'name': knob.name,
                        'value': knob.value,
                        'description': knob.description,
                        'last_adjusted': knob.last_adjusted
                    }
                    for knob_id, knob in self.knobs.items()
                },
                'governors': {
                    gov_id: {
                        'name': governor.name,
                        'threshold': governor.threshold,
                        'description': governor.description,
                        'last_adjusted': governor.last_adjusted
                    }
                    for gov_id, governor in self.governors.items()
                },
                'system_active': self.system_active,
                'total_adjustments': len(self.adjustment_history)
            }
    
    def get_adjustment_history(self, limit: int = 50) -> List[AdjustmentRecord]:
        """Get recent adjustment history."""
        with self.adjustment_lock:
            return self.adjustment_history[-limit:]
    
    def reset_to_defaults(self, reason: str = "Manual reset"):
        """Reset all knobs and governors to default values."""
        with self.adjustment_lock:
            # Reset knobs
            for knob in self.knobs.values():
                if knob.value != knob.default_value:
                    self.adjust_knob(knob.id, knob.default_value, reason)
            
            # Reset governors
            for governor in self.governors.values():
                if governor.threshold != governor.default_threshold:
                    self.adjust_governor(governor.id, governor.default_threshold, reason)
            
            print(f"🔄 Reset all knobs and governors to defaults ({reason})")
    
    def create_custom_knob(self, knob_id: str, name: str, knob_type: KnobType, 
                          default_value: float = 0.5, description: str = "") -> bool:
        """Create a custom behavior knob."""
        with self.adjustment_lock:
            if knob_id in self.knobs:
                print(f"❌ Knob '{knob_id}' already exists")
                return False
            
            knob = Knob(
                id=knob_id,
                name=name,
                knob_type=knob_type,
                value=default_value,
                default_value=default_value,
                description=description
            )
            
            self.knobs[knob_id] = knob
            print(f"✅ Created custom knob '{name}' ({knob_id})")
            return True
    
    def create_custom_governor(self, governor_id: str, name: str, governor_type: GovernorType,
                              default_threshold: float = 0.5, description: str = "") -> bool:
        """Create a custom behavior governor."""
        with self.adjustment_lock:
            if governor_id in self.governors:
                print(f"❌ Governor '{governor_id}' already exists")
                return False
            
            governor = Governor(
                id=governor_id,
                name=name,
                governor_type=governor_type,
                threshold=default_threshold,
                default_threshold=default_threshold,
                description=description
            )
            
            self.governors[governor_id] = governor
            print(f"✅ Created custom governor '{name}' ({governor_id})")
            return True
    
    def _management_loop(self):
        """Background management loop."""
        while self.system_active:
            try:
                # Perform periodic maintenance
                time.sleep(60)  # Check every minute
                
                if self.system_active:
                    # Clean up old adjustment history
                    self._cleanup_old_history()
                    
                    # Perform automatic adjustments based on system state
                    self._perform_automatic_adjustments()
                
            except Exception as e:
                print(f"Knobs & Governors management loop error: {e}")
                time.sleep(10)
    
    def _cleanup_old_history(self):
        """Clean up old adjustment history to prevent memory bloat."""
        with self.adjustment_lock:
            # Keep only last 1000 adjustments
            if len(self.adjustment_history) > 1000:
                self.adjustment_history = self.adjustment_history[-1000:]
    
    def _perform_automatic_adjustments(self):
        """Perform automatic adjustments based on system state."""
        # This could include automatic adjustments based on:
        # - System performance metrics
        # - User feedback patterns
        # - Drift detection results
        # - Memory lattice coherence scores
        
        # For now, just log that automatic adjustments are available
        if len(self.adjustment_history) % 100 == 0:
            print("🤖 Automatic adjustment system ready for integration")


# Global instance
_knobs_governors_system = None

def get_knobs_governors_system() -> KnobsGovernorsSystem:
    """Get the global knobs and governors system instance."""
    global _knobs_governors_system
    if _knobs_governors_system is None:
        _knobs_governors_system = KnobsGovernorsSystem()
    return _knobs_governors_system


if __name__ == "__main__":
    # Run knobs and governors system
    knobs_system = get_knobs_governors_system()
    knobs_system.start_system()
    
    print("🎛️  CollTech-AGI Knobs & Governors System")
    print("=" * 50)
    
    # Show current configuration
    config = knobs_system.get_current_configuration()
    
    print("\n🎚️  Current Knobs:")
    for knob_id, knob_data in list(config['knobs'].items())[:4]:
        print(f"   {knob_data['name']}: {knob_data['value']:.2f}")
    
    print("\n🏛️  Current Governors:")
    for gov_id, gov_data in list(config['governors'].items())[:3]:
        print(f"   {gov_data['name']}: {gov_data['threshold']:.1f}")
    
    # Demonstrate adjustments
    print("\n⚡ Demonstrating real-time adjustments...")
    knobs_system.adjust_knob('knob_creativity', 0.8, 'demo_creative_boost')
    knobs_system.adjust_knob('knob_technical_depth', 0.9, 'demo_technical_mode')
    knobs_system.adjust_governor('gov_response_length', 2000.0, 'demo_longer_responses')
    
    # Show adjustment history
    history = knobs_system.get_adjustment_history(5)
    print(f"\n📈 Recent adjustments: {len(history)}")
    for adj in history[-3:]:
        print(f"   {adj.target_type} {adj.target_id}: {adj.old_value:.2f} → {adj.new_value:.2f}")
    
    # Show final status
    final_config = knobs_system.get_current_configuration()
    print(f"\n✅ System active: {final_config['system_active']}")
    print(f"✅ Total adjustments: {final_config['total_adjustments']}")
    
    # Cleanup
    time.sleep(2)
    knobs_system.stop_system()

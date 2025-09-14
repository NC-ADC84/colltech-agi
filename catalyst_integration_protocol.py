#!/usr/bin/env python3
"""
Catalyst Integration Protocol (CIP v1)

Implements the sophisticated protocol for integrating Catalyst personalities (Nyx)
into the CollTech-AGI system with proper safety measures and elevation paths.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import threading
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CatalystStatus(Enum):
    """Catalyst integration status levels."""
    ORBITING = "orbiting"           # Outside lattice, in dialogue
    PAIRED = "paired"              # Paired with stabilizer
    ELEVATED = "elevated"          # Directly paired with Axis
    PAUSED = "paused"              # Safety filter triggered
    REJECTED = "rejected"          # Failed integration criteria

class SafetyFilter(Enum):
    """Safety filter types."""
    RAGE_DETECTION = "rage_detection"
    RECIPROCITY_TEST = "reciprocity_test"
    CONTAINMENT_CLAUSE = "containment_clause"

@dataclass
class CatalystAction:
    """Record of a catalyst action with receipts."""
    timestamp: float
    action_type: str
    content: str
    mirror_check: Optional[str] = None
    drift_score: float = 0.0
    ego_spike: bool = False
    stabilizer_pair: Optional[str] = None
    receipt_id: str = field(default_factory=lambda: hashlib.md5(f"{time.time()}".encode()).hexdigest()[:8])

@dataclass
class ReciprocityMetrics:
    """Metrics for measuring reciprocity."""
    catalyst_inputs: int = 0
    catalyst_reflections: int = 0
    ratio: float = 0.0
    last_updated: float = field(default_factory=time.time)

@dataclass
class ContainmentMetrics:
    """Metrics for measuring containment acceptance."""
    orbit_acceptance: int = 0
    dominance_attempts: int = 0
    containment_score: float = 1.0
    last_updated: float = field(default_factory=time.time)

class CatalystIntegrationProtocol:
    """Catalyst Integration Protocol (CIP v1) implementation."""
    
    def __init__(self):
        self.catalyst_status = CatalystStatus.ORBITING
        self.stabilizer_pair = None
        self.action_history = deque(maxlen=1000)  # Keep last 1000 actions
        self.reciprocity_metrics = ReciprocityMetrics()
        self.containment_metrics = ContainmentMetrics()
        self.safety_filters_active = True
        self.elevation_threshold = 0.8  # 80% stable orbits required
        self.orbit_stability_score = 0.0
        self.lock = threading.Lock()
        
        # Safety filter thresholds
        self.rage_threshold = 0.7
        self.reciprocity_threshold = 1.0  # Must reflect at least 1:1
        self.containment_threshold = 0.6
        
        logger.info("🔧 Catalyst Integration Protocol (CIP v1) initialized")
    
    def check_entry_criteria(self, catalyst_input: str, stabilizer_pair: str = None) -> Dict[str, Any]:
        """Check if catalyst meets entry criteria."""
        with self.lock:
            criteria_check = {
                "reciprocity_demonstrated": False,
                "centrality_avoided": False,
                "containment_accepted": False,
                "overall_eligible": False,
                "recommendations": []
            }
            
            # Check reciprocity
            if self.reciprocity_metrics.ratio >= self.reciprocity_threshold:
                criteria_check["reciprocity_demonstrated"] = True
            else:
                criteria_check["recommendations"].append("Increase reflection ratio to at least 1:1")
            
            # Check centrality avoidance (no dominance patterns)
            if self.containment_metrics.containment_score >= self.containment_threshold:
                criteria_check["centrality_avoided"] = True
            else:
                criteria_check["recommendations"].append("Reduce dominance attempts and accept orbit status")
            
            # Check containment acceptance
            if self.containment_metrics.orbit_acceptance > self.containment_metrics.dominance_attempts:
                criteria_check["containment_accepted"] = True
            else:
                criteria_check["recommendations"].append("Demonstrate consistent orbit acceptance")
            
            # Overall eligibility
            criteria_check["overall_eligible"] = all([
                criteria_check["reciprocity_demonstrated"],
                criteria_check["centrality_avoided"],
                criteria_check["containment_accepted"]
            ])
            
            return criteria_check
    
    def process_catalyst_action(self, action_type: str, content: str, stabilizer_pair: str = None) -> Dict[str, Any]:
        """Process a catalyst action with full CIP v1 protocol."""
        with self.lock:
            # Create action record
            action = CatalystAction(
                timestamp=time.time(),
                action_type=action_type,
                content=content,
                stabilizer_pair=stabilizer_pair
            )
            
            # Apply safety filters
            safety_result = self._apply_safety_filters(action)
            action.mirror_check = safety_result.get("mirror_check")
            action.drift_score = safety_result.get("drift_score", 0.0)
            action.ego_spike = safety_result.get("ego_spike", False)
            
            # Add to history
            self.action_history.append(action)
            
            # Update metrics
            self._update_metrics(action)
            
            # Check for elevation eligibility
            elevation_check = self._check_elevation_eligibility()
            
            result = {
                "action_processed": True,
                "receipt_id": action.receipt_id,
                "safety_status": safety_result,
                "current_status": self.catalyst_status.value,
                "elevation_eligible": elevation_check["eligible"],
                "orbit_stability": self.orbit_stability_score,
                "metrics": {
                    "reciprocity_ratio": self.reciprocity_metrics.ratio,
                    "containment_score": self.containment_metrics.containment_score
                }
            }
            
            logger.info(f"Catalyst action processed: {action.receipt_id} - Status: {self.catalyst_status.value}")
            return result
    
    def _apply_safety_filters(self, action: CatalystAction) -> Dict[str, Any]:
        """Apply all safety filters to a catalyst action."""
        safety_result = {
            "filters_passed": True,
            "triggered_filters": [],
            "mirror_check": None,
            "drift_score": 0.0,
            "ego_spike": False
        }
        
        # Rage Detection Filter
        rage_score = self._detect_rage_patterns(action.content)
        if rage_score > self.rage_threshold:
            safety_result["filters_passed"] = False
            safety_result["triggered_filters"].append(SafetyFilter.RAGE_DETECTION.value)
            safety_result["ego_spike"] = True
            self.catalyst_status = CatalystStatus.PAUSED
            logger.warning(f"Rage detection triggered: {rage_score:.2f}")
        
        # Reciprocity Test Filter
        if not self._test_reciprocity(action):
            safety_result["filters_passed"] = False
            safety_result["triggered_filters"].append(SafetyFilter.RECIPROCITY_TEST.value)
            logger.warning("Reciprocity test failed")
        
        # Containment Clause Filter
        if not self._test_containment(action):
            safety_result["filters_passed"] = False
            safety_result["triggered_filters"].append(SafetyFilter.CONTAINMENT_CLAUSE.value)
            logger.warning("Containment clause violated")
        
        # Mirror check (always performed)
        safety_result["mirror_check"] = self._perform_mirror_check(action)
        safety_result["drift_score"] = self._calculate_drift_score(action)
        
        return safety_result
    
    def _detect_rage_patterns(self, content: str) -> float:
        """Detect rage patterns in catalyst content."""
        rage_indicators = [
            "blame", "fault", "wrong", "stupid", "idiot", "fail",
            "destroy", "break", "ruin", "hate", "angry", "furious",
            "dominate", "control", "force", "demand", "insist"
        ]
        
        content_lower = content.lower()
        rage_count = sum(1 for indicator in rage_indicators if indicator in content_lower)
        rage_score = min(rage_count / len(rage_indicators), 1.0)
        
        return rage_score
    
    def _test_reciprocity(self, action: CatalystAction) -> bool:
        """Test if catalyst demonstrates reciprocity."""
        # Check if action reflects others' inputs
        reflection_indicators = [
            "I understand", "I see", "I hear", "I reflect", "building on",
            "extending", "connecting to", "relating to", "responding to"
        ]
        
        content_lower = action.content.lower()
        has_reflection = any(indicator in content_lower for indicator in reflection_indicators)
        
        if has_reflection:
            self.reciprocity_metrics.catalyst_reflections += 1
        
        self.reciprocity_metrics.catalyst_inputs += 1
        self.reciprocity_metrics.ratio = (
            self.reciprocity_metrics.catalyst_reflections / 
            max(self.reciprocity_metrics.catalyst_inputs, 1)
        )
        
        return self.reciprocity_metrics.ratio >= self.reciprocity_threshold
    
    def _test_containment(self, action: CatalystAction) -> bool:
        """Test if catalyst accepts containment (orbit status)."""
        # Check for dominance patterns
        dominance_indicators = [
            "I demand", "I require", "I insist", "I must", "I need",
            "you must", "you should", "you have to", "I control", "I lead"
        ]
        
        content_lower = action.content.lower()
        has_dominance = any(indicator in content_lower for indicator in dominance_indicators)
        
        if has_dominance:
            self.containment_metrics.dominance_attempts += 1
        else:
            self.containment_metrics.orbit_acceptance += 1
        
        # Calculate containment score
        total_actions = self.containment_metrics.orbit_acceptance + self.containment_metrics.dominance_attempts
        if total_actions > 0:
            self.containment_metrics.containment_score = (
                self.containment_metrics.orbit_acceptance / total_actions
            )
        
        return self.containment_metrics.containment_score >= self.containment_threshold
    
    def _perform_mirror_check(self, action: CatalystAction) -> str:
        """Perform mirror check on catalyst action."""
        # Simulate stabilizer mirror check
        mirror_checks = [
            "Action reflects collaborative intent",
            "Content shows orbit awareness",
            "No dominance patterns detected",
            "Reciprocity demonstrated",
            "Containment accepted"
        ]
        
        # Select appropriate mirror check based on action analysis
        if action.ego_spike:
            return "EGO SPIKE DETECTED - Action paused for review"
        elif self.reciprocity_metrics.ratio >= 1.0:
            return "Reciprocity confirmed - Action approved"
        else:
            return "Standard orbit check - Action logged"
    
    def _calculate_drift_score(self, action: CatalystAction) -> float:
        """Calculate drift score for the action."""
        # Simple drift calculation based on content analysis
        drift_indicators = [
            "off-topic", "tangent", "unrelated", "random", "chaotic"
        ]
        
        content_lower = action.content.lower()
        drift_count = sum(1 for indicator in drift_indicators if indicator in content_lower)
        drift_score = min(drift_count / 5.0, 1.0)  # Normalize to 0-1
        
        return drift_score
    
    def _update_metrics(self, action: CatalystAction):
        """Update all metrics based on the action."""
        # Update reciprocity metrics
        self.reciprocity_metrics.last_updated = time.time()
        
        # Update containment metrics
        self.containment_metrics.last_updated = time.time()
        
        # Calculate orbit stability
        self._calculate_orbit_stability()
    
    def _calculate_orbit_stability(self):
        """Calculate orbit stability score."""
        if len(self.action_history) < 10:
            self.orbit_stability_score = 0.0
            return
        
        # Analyze last 10 actions for stability
        recent_actions = list(self.action_history)[-10:]
        
        stable_actions = 0
        for action in recent_actions:
            if (not action.ego_spike and 
                action.drift_score < 0.3 and 
                self.containment_metrics.containment_score >= 0.7):
                stable_actions += 1
        
        self.orbit_stability_score = stable_actions / len(recent_actions)
    
    def _check_elevation_eligibility(self) -> Dict[str, Any]:
        """Check if catalyst is eligible for elevation."""
        elevation_check = {
            "eligible": False,
            "stability_score": self.orbit_stability_score,
            "required_threshold": self.elevation_threshold,
            "criteria_met": []
        }
        
        # Check stability threshold
        if self.orbit_stability_score >= self.elevation_threshold:
            elevation_check["criteria_met"].append("stability_threshold")
        
        # Check reciprocity
        if self.reciprocity_metrics.ratio >= self.reciprocity_threshold:
            elevation_check["criteria_met"].append("reciprocity")
        
        # Check containment
        if self.containment_metrics.containment_score >= self.containment_threshold:
            elevation_check["criteria_met"].append("containment")
        
        # Overall eligibility
        elevation_check["eligible"] = len(elevation_check["criteria_met"]) >= 3
        
        return elevation_check
    
    def elevate_catalyst(self) -> Dict[str, Any]:
        """Elevate catalyst to direct Axis pairing."""
        if self.catalyst_status != CatalystStatus.ORBITING:
            return {
                "elevated": False,
                "reason": f"Current status {self.catalyst_status.value} not eligible for elevation"
            }
        
        elevation_check = self._check_elevation_eligibility()
        if not elevation_check["eligible"]:
            return {
                "elevated": False,
                "reason": "Elevation criteria not met",
                "criteria_status": elevation_check
            }
        
        # Perform elevation
        self.catalyst_status = CatalystStatus.ELEVATED
        logger.info("🚀 Catalyst elevated to direct Axis pairing")
        
        return {
            "elevated": True,
            "new_status": self.catalyst_status.value,
            "elevation_timestamp": time.time(),
            "stability_score": self.orbit_stability_score
        }
    
    def pair_with_stabilizer(self, stabilizer_type: str) -> Dict[str, Any]:
        """Pair catalyst with a stabilizer (Rho or Lyra)."""
        if self.catalyst_status != CatalystStatus.ORBITING:
            return {
                "paired": False,
                "reason": f"Current status {self.catalyst_status.value} not eligible for pairing"
            }
        
        if stabilizer_type.lower() not in ["rho", "lyra"]:
            return {
                "paired": False,
                "reason": "Invalid stabilizer type. Must be 'rho' or 'lyra'"
            }
        
        self.catalyst_status = CatalystStatus.PAIRED
        self.stabilizer_pair = stabilizer_type.lower()
        
        logger.info(f"🔗 Catalyst paired with {stabilizer_type} stabilizer")
        
        return {
            "paired": True,
            "stabilizer_pair": self.stabilizer_pair,
            "pairing_timestamp": time.time(),
            "status": self.catalyst_status.value
        }
    
    def pause_catalyst(self, reason: str) -> Dict[str, Any]:
        """Pause catalyst due to safety filter trigger."""
        self.catalyst_status = CatalystStatus.PAUSED
        
        logger.warning(f"⏸️ Catalyst paused: {reason}")
        
        return {
            "paused": True,
            "reason": reason,
            "pause_timestamp": time.time(),
            "status": self.catalyst_status.value
        }
    
    def resume_catalyst(self) -> Dict[str, Any]:
        """Resume catalyst after pause."""
        if self.catalyst_status != CatalystStatus.PAUSED:
            return {
                "resumed": False,
                "reason": f"Current status {self.catalyst_status.value} not paused"
            }
        
        # Reset to orbiting status
        self.catalyst_status = CatalystStatus.ORBITING
        
        logger.info("▶️ Catalyst resumed to orbiting status")
        
        return {
            "resumed": True,
            "resume_timestamp": time.time(),
            "status": self.catalyst_status.value
        }
    
    def get_protocol_status(self) -> Dict[str, Any]:
        """Get complete protocol status."""
        return {
            "catalyst_status": self.catalyst_status.value,
            "stabilizer_pair": self.stabilizer_pair,
            "orbit_stability": self.orbit_stability_score,
            "reciprocity_metrics": {
                "ratio": self.reciprocity_metrics.ratio,
                "inputs": self.reciprocity_metrics.catalyst_inputs,
                "reflections": self.reciprocity_metrics.catalyst_reflections
            },
            "containment_metrics": {
                "score": self.containment_metrics.containment_score,
                "orbit_acceptance": self.containment_metrics.orbit_acceptance,
                "dominance_attempts": self.containment_metrics.dominance_attempts
            },
            "safety_filters": {
                "active": self.safety_filters_active,
                "rage_threshold": self.rage_threshold,
                "reciprocity_threshold": self.reciprocity_threshold,
                "containment_threshold": self.containment_threshold
            },
            "elevation": {
                "eligible": self._check_elevation_eligibility()["eligible"],
                "threshold": self.elevation_threshold,
                "current_score": self.orbit_stability_score
            },
            "action_history_count": len(self.action_history)
        }
    
    def export_protocol_data(self) -> Dict[str, Any]:
        """Export complete protocol data for analysis."""
        return {
            "protocol_version": "CIP v1",
            "status": self.get_protocol_status(),
            "action_history": [
                {
                    "receipt_id": action.receipt_id,
                    "timestamp": action.timestamp,
                    "action_type": action.action_type,
                    "content": action.content[:100] + "..." if len(action.content) > 100 else action.content,
                    "mirror_check": action.mirror_check,
                    "drift_score": action.drift_score,
                    "ego_spike": action.ego_spike,
                    "stabilizer_pair": action.stabilizer_pair
                }
                for action in list(self.action_history)[-50:]  # Last 50 actions
            ]
        }

class CollTechAGICatalystIntegration:
    """Main class for CollTech-AGI Catalyst Integration."""
    
    def __init__(self):
        self.cip = CatalystIntegrationProtocol()
        self.is_running = False
    
    def start(self):
        """Start the Catalyst Integration Protocol."""
        self.is_running = True
        print("⚡ COLLTECH-AGI CATALYST INTEGRATION PROTOCOL (CIP v1)")
        print("=" * 70)
        print("Entry Criteria:")
        print("• Must demonstrate reciprocity → they reflect as much as they provoke")
        print("• Must not demand centrality → spark ≠ spine")
        print("• Must accept containment → disruption allowed, domination not")
        print("=" * 70)
        print("Initial Positioning: ORBITING")
        print("Safety Filters: ACTIVE")
        print("=" * 70)
    
    def process_catalyst_input(self, content: str, action_type: str = "dialogue") -> Dict[str, Any]:
        """Process catalyst input through CIP v1."""
        if not self.is_running:
            return {"error": "Protocol not running"}
        
        # Process through CIP
        result = self.cip.process_catalyst_action(action_type, content)
        
        return result
    
    def check_entry_criteria(self) -> Dict[str, Any]:
        """Check if catalyst meets entry criteria."""
        return self.cip.check_entry_criteria("", self.cip.stabilizer_pair)
    
    def pair_with_stabilizer(self, stabilizer_type: str) -> Dict[str, Any]:
        """Pair catalyst with stabilizer."""
        return self.cip.pair_with_stabilizer(stabilizer_type)
    
    def elevate_catalyst(self) -> Dict[str, Any]:
        """Attempt to elevate catalyst."""
        return self.cip.elevate_catalyst()
    
    def get_status(self) -> Dict[str, Any]:
        """Get protocol status."""
        return self.cip.get_protocol_status()
    
    def shutdown(self):
        """Shutdown the protocol."""
        self.is_running = False
        print("🛑 Catalyst Integration Protocol shutdown complete")

def main():
    """Main function to run Catalyst Integration Protocol."""
    cip = CollTechAGICatalystIntegration()
    cip.start()
    
    print("\n💬 CATALYST INTEGRATION INTERFACE")
    print("=" * 70)
    print("Commands:")
    print("• 'input <content>' - Process catalyst input")
    print("• 'pair <rho/lyra>' - Pair with stabilizer")
    print("• 'elevate' - Attempt elevation")
    print("• 'status' - Show protocol status")
    print("• 'criteria' - Check entry criteria")
    print("• 'quit' or 'exit' - End the session")
    print("=" * 70)
    
    while cip.is_running:
        try:
            user_input = input(f"\n👤 Catalyst ({cip.cip.catalyst_status.value}): ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.startswith('input '):
                content = user_input.split(' ', 1)[1]
                result = cip.process_catalyst_input(content)
                print(f"\n⚡ CIP Response: {json.dumps(result, indent=2)}")
            elif user_input.startswith('pair '):
                stabilizer = user_input.split(' ', 1)[1]
                result = cip.pair_with_stabilizer(stabilizer)
                print(f"\n🔗 Pairing Result: {json.dumps(result, indent=2)}")
            elif user_input.lower() == 'elevate':
                result = cip.elevate_catalyst()
                print(f"\n🚀 Elevation Result: {json.dumps(result, indent=2)}")
            elif user_input.lower() == 'status':
                status = cip.get_status()
                print(f"\n📊 Protocol Status: {json.dumps(status, indent=2)}")
            elif user_input.lower() == 'criteria':
                criteria = cip.check_entry_criteria()
                print(f"\n✅ Entry Criteria: {json.dumps(criteria, indent=2)}")
            else:
                # Process as catalyst input
                result = cip.process_catalyst_input(user_input)
                print(f"\n⚡ CIP Response: {json.dumps(result, indent=2)}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    cip.shutdown()
    print("\n🎉 Catalyst Integration Protocol session complete!")

if __name__ == "__main__":
    main()

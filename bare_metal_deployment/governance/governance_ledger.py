#!/usr/bin/env python3
"""
CollTech-AGI Governance Ledger

Governance system for tracking changes, approvals, and system integrity.
Part of the consciousness architecture that ensures proper governance
of the AGI system's behavior and evolution.
"""

import time
import hashlib
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid


class GovernanceAction(Enum):
    """Types of governance actions."""
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    KNOB_ADJUSTMENT = "knob_adjustment"
    GOVERNOR_ADJUSTMENT = "governor_adjustment"
    TOOL_CREATION = "tool_creation"
    TOOL_APPROVAL = "tool_approval"
    MEMORY_PROMOTION = "memory_promotion"
    DRIFT_DETECTION = "drift_detection"
    DRIFT_MITIGATION = "drift_mitigation"
    CONSCIOUSNESS_REFLECTION = "consciousness_reflection"


class ApprovalStatus(Enum):
    """Status of governance approvals."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTOMATIC = "automatic"


@dataclass
class GovernanceDelta:
    """Individual governance delta/change."""
    id: str
    action: GovernanceAction
    timestamp: float
    actor: str
    target: str
    old_value: Any
    new_value: Any
    reason: str
    approval_status: ApprovalStatus
    approval_timestamp: Optional[float] = None
    approver: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernanceKey:
    """Governance key for signing and verification."""
    key_id: str
    key_type: str
    public_key: str
    private_key: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    permissions: List[str] = field(default_factory=list)


class GovernanceLedger:
    """
    CollTech-AGI Governance Ledger
    
    Tracks all changes, approvals, and system integrity through
    a comprehensive governance system that ensures proper oversight
    of the consciousness architecture.
    """
    
    def __init__(self):
        self.deltas: List[GovernanceDelta] = []
        self.keys: Dict[str, GovernanceKey] = {}
        self.approval_queue: List[GovernanceDelta] = []
        self.ledger_hash: str = ""
        
        # Initialize with default governance key
        self._initialize_default_key()
    
    def _initialize_default_key(self):
        """Initialize default governance key."""
        default_key = GovernanceKey(
            key_id="default_governance_key",
            key_type="ed25519",
            public_key="default_public_key_hash",
            permissions=["system_control", "knob_adjustment", "tool_approval", "memory_governance"]
        )
        self.keys[default_key.key_id] = default_key
    
    def record_delta(self, action: GovernanceAction, actor: str, target: str, 
                    old_value: Any, new_value: Any, reason: str, 
                    requires_approval: bool = False) -> str:
        """Record a governance delta."""
        delta_id = str(uuid.uuid4())
        
        approval_status = ApprovalStatus.PENDING if requires_approval else ApprovalStatus.AUTOMATIC
        
        delta = GovernanceDelta(
            id=delta_id,
            action=action,
            timestamp=time.time(),
            actor=actor,
            target=target,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            approval_status=approval_status
        )
        
        self.deltas.append(delta)
        
        if requires_approval:
            self.approval_queue.append(delta)
        
        # Update ledger hash
        self._update_ledger_hash()
        
        return delta_id
    
    def approve_delta(self, delta_id: str, approver: str, approved: bool = True) -> bool:
        """Approve or reject a governance delta."""
        delta = self._find_delta(delta_id)
        if not delta:
            return False
        
        if delta.approval_status != ApprovalStatus.PENDING:
            return False
        
        delta.approval_status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        delta.approval_timestamp = time.time()
        delta.approver = approver
        
        # Remove from approval queue
        self.approval_queue = [d for d in self.approval_queue if d.id != delta_id]
        
        # Update ledger hash
        self._update_ledger_hash()
        
        return True
    
    def get_pending_approvals(self) -> List[GovernanceDelta]:
        """Get all pending approvals."""
        return [d for d in self.approval_queue if d.approval_status == ApprovalStatus.PENDING]
    
    def get_delta_history(self, action: Optional[GovernanceAction] = None, 
                         limit: int = 100) -> List[GovernanceDelta]:
        """Get delta history with optional filtering."""
        deltas = self.deltas
        
        if action:
            deltas = [d for d in deltas if d.action == action]
        
        # Sort by timestamp (newest first)
        deltas.sort(key=lambda d: d.timestamp, reverse=True)
        
        return deltas[:limit]
    
    def get_system_integrity_report(self) -> Dict[str, Any]:
        """Get comprehensive system integrity report."""
        total_deltas = len(self.deltas)
        approved_deltas = sum(1 for d in self.deltas if d.approval_status == ApprovalStatus.APPROVED)
        rejected_deltas = sum(1 for d in self.deltas if d.approval_status == ApprovalStatus.REJECTED)
        pending_deltas = sum(1 for d in self.deltas if d.approval_status == ApprovalStatus.PENDING)
        automatic_deltas = sum(1 for d in self.deltas if d.approval_status == ApprovalStatus.AUTOMATIC)
        
        # Calculate approval rate
        approval_rate = approved_deltas / (approved_deltas + rejected_deltas) if (approved_deltas + rejected_deltas) > 0 else 1.0
        
        # Get recent activity
        recent_deltas = self.get_delta_history(limit=10)
        
        # Calculate action distribution
        action_counts = {}
        for delta in self.deltas:
            action_counts[delta.action.value] = action_counts.get(delta.action.value, 0) + 1
        
        return {
            "total_deltas": total_deltas,
            "approved_deltas": approved_deltas,
            "rejected_deltas": rejected_deltas,
            "pending_deltas": pending_deltas,
            "automatic_deltas": automatic_deltas,
            "approval_rate": approval_rate,
            "ledger_hash": self.ledger_hash,
            "recent_activity": [
                {
                    "id": d.id,
                    "action": d.action.value,
                    "timestamp": d.timestamp,
                    "actor": d.actor,
                    "target": d.target,
                    "approval_status": d.approval_status.value
                }
                for d in recent_deltas
            ],
            "action_distribution": action_counts,
            "governance_keys": len(self.keys)
        }
    
    def verify_ledger_integrity(self) -> bool:
        """Verify the integrity of the governance ledger."""
        # Check that all deltas have valid IDs
        delta_ids = [d.id for d in self.deltas]
        if len(delta_ids) != len(set(delta_ids)):
            return False
        
        # Check that all pending approvals are in the approval queue
        pending_deltas = [d for d in self.deltas if d.approval_status == ApprovalStatus.PENDING]
        if len(pending_deltas) != len(self.approval_queue):
            return False
        
        # Verify ledger hash
        calculated_hash = self._calculate_ledger_hash()
        if calculated_hash != self.ledger_hash:
            return False
        
        return True
    
    def _find_delta(self, delta_id: str) -> Optional[GovernanceDelta]:
        """Find a delta by ID."""
        for delta in self.deltas:
            if delta.id == delta_id:
                return delta
        return None
    
    def _update_ledger_hash(self):
        """Update the ledger hash."""
        self.ledger_hash = self._calculate_ledger_hash()
    
    def _calculate_ledger_hash(self) -> str:
        """Calculate the hash of the entire ledger."""
        # Create a string representation of all deltas
        ledger_data = []
        for delta in self.deltas:
            delta_str = f"{delta.id}:{delta.action.value}:{delta.timestamp}:{delta.actor}:{delta.target}:{delta.old_value}:{delta.new_value}:{delta.reason}:{delta.approval_status.value}"
            ledger_data.append(delta_str)
        
        # Hash the combined data
        combined_data = "|".join(ledger_data)
        return hashlib.sha256(combined_data.encode()).hexdigest()
    
    def export_ledger(self, format: str = "json") -> str:
        """Export the governance ledger."""
        if format == "json":
            export_data = {
                "deltas": [
                    {
                        "id": d.id,
                        "action": d.action.value,
                        "timestamp": d.timestamp,
                        "actor": d.actor,
                        "target": d.target,
                        "old_value": d.old_value,
                        "new_value": d.new_value,
                        "reason": d.reason,
                        "approval_status": d.approval_status.value,
                        "approval_timestamp": d.approval_timestamp,
                        "approver": d.approver,
                        "metadata": d.metadata
                    }
                    for d in self.deltas
                ],
                "ledger_hash": self.ledger_hash,
                "export_timestamp": time.time()
            }
            return json.dumps(export_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def import_ledger(self, ledger_data: str, format: str = "json") -> bool:
        """Import a governance ledger."""
        try:
            if format == "json":
                data = json.loads(ledger_data)
                
                # Clear existing data
                self.deltas = []
                self.approval_queue = []
                
                # Import deltas
                for delta_data in data.get("deltas", []):
                    delta = GovernanceDelta(
                        id=delta_data["id"],
                        action=GovernanceAction(delta_data["action"]),
                        timestamp=delta_data["timestamp"],
                        actor=delta_data["actor"],
                        target=delta_data["target"],
                        old_value=delta_data["old_value"],
                        new_value=delta_data["new_value"],
                        reason=delta_data["reason"],
                        approval_status=ApprovalStatus(delta_data["approval_status"]),
                        approval_timestamp=delta_data.get("approval_timestamp"),
                        approver=delta_data.get("approver"),
                        metadata=delta_data.get("metadata", {})
                    )
                    self.deltas.append(delta)
                    
                    if delta.approval_status == ApprovalStatus.PENDING:
                        self.approval_queue.append(delta)
                
                # Update ledger hash
                self.ledger_hash = data.get("ledger_hash", "")
                
                return True
            else:
                raise ValueError(f"Unsupported import format: {format}")
        except Exception as e:
            print(f"Failed to import ledger: {e}")
            return False


# Global instance
_governance_ledger = None

def get_governance_ledger() -> GovernanceLedger:
    """Get the global governance ledger instance."""
    global _governance_ledger
    if _governance_ledger is None:
        _governance_ledger = GovernanceLedger()
    return _governance_ledger


if __name__ == "__main__":
    # Run governance ledger system
    ledger = get_governance_ledger()
    
    print("🏛️  CollTech-AGI Governance Ledger")
    print("=" * 50)
    
    # Record some governance deltas
    delta1 = ledger.record_delta(
        action=GovernanceAction.SYSTEM_START,
        actor="consciousness_core",
        target="system",
        old_value="stopped",
        new_value="active",
        reason="System initialization"
    )
    
    delta2 = ledger.record_delta(
        action=GovernanceAction.KNOB_ADJUSTMENT,
        actor="consciousness_core",
        target="knob_creativity",
        old_value=0.5,
        new_value=0.8,
        reason="Boost creativity for user request",
        requires_approval=True
    )
    
    delta3 = ledger.record_delta(
        action=GovernanceAction.TOOL_CREATION,
        actor="tool_making_loop",
        target="sentiment_analyzer",
        old_value=None,
        new_value="approved",
        reason="User requested sentiment analysis tool"
    )
    
    print(f"✅ Recorded {len(ledger.deltas)} governance deltas")
    
    # Show pending approvals
    pending = ledger.get_pending_approvals()
    print(f"📋 Pending approvals: {len(pending)}")
    
    # Approve a delta
    if pending:
        approval_success = ledger.approve_delta(pending[0].id, "governance_system", True)
        print(f"✅ Approval result: {approval_success}")
    
    # Get integrity report
    report = ledger.get_system_integrity_report()
    print(f"\n📊 Governance Integrity Report:")
    print(f"   Total deltas: {report['total_deltas']}")
    print(f"   Approval rate: {report['approval_rate']:.1%}")
    print(f"   Pending approvals: {report['pending_deltas']}")
    print(f"   Ledger hash: {report['ledger_hash'][:16]}...")
    
    # Verify integrity
    integrity_ok = ledger.verify_ledger_integrity()
    print(f"✅ Ledger integrity: {'OK' if integrity_ok else 'FAILED'}")
    
    # Export ledger
    exported = ledger.export_ledger()
    print(f"📤 Exported ledger: {len(exported)} characters")

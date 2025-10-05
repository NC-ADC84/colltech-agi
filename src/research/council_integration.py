#!/usr/bin/env python3
"""
CollTech-AGI Council Integration System

Advanced council integration framework implementing the CRT (Continuum Research Tester)
council-aligned protocol. Provides council status management, decision tracking,
and integration with the consciousness system.
"""

import time
import hashlib
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CouncilStatus(Enum):
    """Council operational status."""
    ACTIVE = "active"
    DELIBERATING = "deliberating"
    VOTING = "voting"
    DECIDED = "decided"
    SUSPENDED = "suspended"
    MAINTENANCE = "maintenance"


class DecisionType(Enum):
    """Types of council decisions."""
    RESEARCH_APPROVAL = "research_approval"
    PROTOCOL_CHANGE = "protocol_change"
    RESOURCE_ALLOCATION = "resource_allocation"
    SAFETY_OVERRIDE = "safety_override"
    CONTINUITY_ASSESSMENT = "continuity_assessment"
    EVIDENCE_VALIDATION = "evidence_validation"


class CouncilMember(Enum):
    """Council member roles."""
    CHAIR = "chair"
    RESEARCH_LEAD = "research_lead"
    SAFETY_OFFICER = "safety_officer"
    CONTINUITY_GUARDIAN = "continuity_guardian"
    EVIDENCE_ARCHIVIST = "evidence_archivist"
    PROTOCOL_SPECIALIST = "protocol_specialist"


@dataclass
class CouncilDecision:
    """Council decision record."""
    id: str
    decision_type: DecisionType
    subject: str
    description: str
    decision: str  # "approved", "rejected", "deferred", "requires_review"
    rationale: str
    voting_record: Dict[CouncilMember, str] = field(default_factory=dict)  # "yes", "no", "abstain"
    timestamp: float = 0.0
    effective_date: Optional[float] = None
    review_date: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


@dataclass
class CouncilSession:
    """Council session record."""
    id: str
    session_type: str
    agenda: List[str]
    decisions: List[str] = field(default_factory=list)  # Decision IDs
    start_time: float = 0.0
    end_time: Optional[float] = None
    status: CouncilStatus = CouncilStatus.ACTIVE
    participants: List[CouncilMember] = field(default_factory=list)
    session_notes: str = ""
    
    def __post_init__(self):
        if not self.start_time:
            self.start_time = time.time()


class CouncilIntegration:
    """
    Council Integration System
    
    Implements the CRT council-aligned protocol with comprehensive
    decision tracking, status management, and consciousness integration.
    """
    
    def __init__(self):
        self.status = CouncilStatus.ACTIVE
        self.active_sessions: Dict[str, CouncilSession] = {}
        self.decisions: Dict[str, CouncilDecision] = {}
        self.decision_history: List[str] = []
        self.council_members = list(CouncilMember)
        
        # Council configuration
        self.quorum_required = 0.6  # 60% of members required for decisions
        self.consensus_threshold = 0.75  # 75% agreement required for approval
        
        logger.info("🏛️ Council Integration System initialized")
        logger.info(f"   Status: {self.status.value}")
        logger.info(f"   Members: {len(self.council_members)}")
        logger.info(f"   Quorum: {self.quorum_required:.0%}")
        logger.info(f"   Consensus: {self.consensus_threshold:.0%}")
    
    def start_session(self, session_type: str, agenda: List[str], 
                     participants: List[CouncilMember] = None) -> str:
        """Start a new council session."""
        session_id = f"session_{int(time.time())}_{hashlib.md5(session_type.encode()).hexdigest()[:8]}"
        
        if participants is None:
            participants = self.council_members
        
        session = CouncilSession(
            id=session_id,
            session_type=session_type,
            agenda=agenda,
            participants=participants,
            status=CouncilStatus.ACTIVE
        )
        
        self.active_sessions[session_id] = session
        self.status = CouncilStatus.DELIBERATING
        
        logger.info(f"🏛️ Started council session: {session_id}")
        logger.info(f"   Type: {session_type}")
        logger.info(f"   Participants: {len(participants)}")
        logger.info(f"   Agenda items: {len(agenda)}")
        
        return session_id
    
    def end_session(self, session_id: str, session_notes: str = "") -> bool:
        """End a council session."""
        if session_id not in self.active_sessions:
            logger.warning(f"Session {session_id} not found")
            return False
        
        session = self.active_sessions[session_id]
        session.end_time = time.time()
        session.status = CouncilStatus.DECIDED
        session.session_notes = session_notes
        
        # Update council status
        if not self.active_sessions:
            self.status = CouncilStatus.ACTIVE
        
        logger.info(f"🏛️ Ended council session: {session_id}")
        logger.info(f"   Duration: {session.end_time - session.start_time:.2f}s")
        logger.info(f"   Decisions made: {len(session.decisions)}")
        
        return True
    
    def make_decision(self, session_id: str, decision_type: DecisionType, 
                     subject: str, description: str, voting_record: Dict[CouncilMember, str],
                     rationale: str = "") -> str:
        """Make a council decision."""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        # Validate voting record
        if not self._validate_voting_record(voting_record, session.participants):
            raise ValueError("Invalid voting record")
        
        # Determine decision based on voting
        decision = self._determine_decision(voting_record, session.participants)
        
        # Create decision record
        decision_id = f"decision_{int(time.time())}_{hashlib.md5(subject.encode()).hexdigest()[:8]}"
        
        council_decision = CouncilDecision(
            id=decision_id,
            decision_type=decision_type,
            subject=subject,
            description=description,
            decision=decision,
            rationale=rationale,
            voting_record=voting_record,
            effective_date=time.time() + 3600  # Effective in 1 hour
        )
        
        # Store decision
        self.decisions[decision_id] = council_decision
        self.decision_history.append(decision_id)
        
        # Add to session
        session.decisions.append(decision_id)
        
        logger.info(f"🏛️ Council decision made: {decision_id}")
        logger.info(f"   Type: {decision_type.value}")
        logger.info(f"   Subject: {subject}")
        logger.info(f"   Decision: {decision}")
        logger.info(f"   Votes: {len(voting_record)}")
        
        return decision_id
    
    def _validate_voting_record(self, voting_record: Dict[CouncilMember, str], 
                               participants: List[CouncilMember]) -> bool:
        """Validate voting record."""
        # Check if all participants voted
        for participant in participants:
            if participant not in voting_record:
                return False
            
            vote = voting_record[participant]
            if vote not in ["yes", "no", "abstain"]:
                return False
        
        # Check quorum
        total_participants = len(participants)
        total_votes = len(voting_record)
        quorum_met = total_votes >= (total_participants * self.quorum_required)
        
        return quorum_met
    
    def _determine_decision(self, voting_record: Dict[CouncilMember, str], 
                           participants: List[CouncilMember]) -> str:
        """Determine decision based on voting record."""
        yes_votes = sum(1 for vote in voting_record.values() if vote == "yes")
        no_votes = sum(1 for vote in voting_record.values() if vote == "no")
        abstain_votes = sum(1 for vote in voting_record.values() if vote == "abstain")
        
        total_votes = len(voting_record)
        
        # Calculate approval percentage
        approval_percentage = yes_votes / total_votes if total_votes > 0 else 0.0
        
        if approval_percentage >= self.consensus_threshold:
            return "approved"
        elif no_votes > yes_votes:
            return "rejected"
        else:
            return "requires_review"
    
    def get_decision(self, decision_id: str) -> Optional[CouncilDecision]:
        """Get decision by ID."""
        return self.decisions.get(decision_id)
    
    def get_session(self, session_id: str) -> Optional[CouncilSession]:
        """Get session by ID."""
        return self.active_sessions.get(session_id)
    
    def get_decisions_by_type(self, decision_type: DecisionType) -> List[CouncilDecision]:
        """Get all decisions of a specific type."""
        return [decision for decision in self.decisions.values() 
                if decision.decision_type == decision_type]
    
    def get_recent_decisions(self, limit: int = 10) -> List[CouncilDecision]:
        """Get recent decisions."""
        recent_ids = self.decision_history[-limit:] if self.decision_history else []
        return [self.decisions[decision_id] for decision_id in recent_ids 
                if decision_id in self.decisions]
    
    def get_council_status(self) -> Dict[str, Any]:
        """Get comprehensive council status."""
        active_sessions = [session for session in self.active_sessions.values() 
                          if session.status == CouncilStatus.ACTIVE]
        
        recent_decisions = self.get_recent_decisions(5)
        
        # Decision statistics
        total_decisions = len(self.decisions)
        approved_decisions = sum(1 for d in self.decisions.values() if d.decision == "approved")
        rejected_decisions = sum(1 for d in self.decisions.values() if d.decision == "rejected")
        review_decisions = sum(1 for d in self.decisions.values() if d.decision == "requires_review")
        
        return {
            'status': self.status.value,
            'active_sessions': len(active_sessions),
            'total_sessions': len(self.active_sessions),
            'total_decisions': total_decisions,
            'decision_statistics': {
                'approved': approved_decisions,
                'rejected': rejected_decisions,
                'requires_review': review_decisions,
                'approval_rate': approved_decisions / total_decisions if total_decisions > 0 else 0.0
            },
            'council_members': len(self.council_members),
            'quorum_required': self.quorum_required,
            'consensus_threshold': self.consensus_threshold,
            'recent_activity': {
                'recent_decisions': len(recent_decisions),
                'last_decision_time': max(d.timestamp for d in recent_decisions) if recent_decisions else 0
            }
        }
    
    def schedule_review(self, decision_id: str, review_date: float) -> bool:
        """Schedule a decision for review."""
        if decision_id not in self.decisions:
            return False
        
        decision = self.decisions[decision_id]
        decision.review_date = review_date
        
        logger.info(f"🏛️ Scheduled review for decision {decision_id} at {review_date}")
        
        return True
    
    def update_decision_status(self, decision_id: str, new_status: str, 
                              rationale: str = "") -> bool:
        """Update decision status."""
        if decision_id not in self.decisions:
            return False
        
        decision = self.decisions[decision_id]
        decision.decision = new_status
        if rationale:
            decision.rationale += f"\nStatus update: {rationale}"
        
        logger.info(f"🏛️ Updated decision {decision_id} status to {new_status}")
        
        return True
    
    def get_decision_analytics(self) -> Dict[str, Any]:
        """Get decision analytics and patterns."""
        if not self.decisions:
            return {}
        
        # Decision type distribution
        type_distribution = {}
        for decision in self.decisions.values():
            decision_type = decision.decision_type.value
            type_distribution[decision_type] = type_distribution.get(decision_type, 0) + 1
        
        # Decision outcome distribution
        outcome_distribution = {}
        for decision in self.decisions.values():
            outcome = decision.decision
            outcome_distribution[outcome] = outcome_distribution.get(outcome, 0) + 1
        
        # Voting pattern analysis
        voting_patterns = {}
        for decision in self.decisions.values():
            for member, vote in decision.voting_record.items():
                member_name = member.value
                if member_name not in voting_patterns:
                    voting_patterns[member_name] = {'yes': 0, 'no': 0, 'abstain': 0}
                voting_patterns[member_name][vote] += 1
        
        # Temporal analysis
        timestamps = [decision.timestamp for decision in self.decisions.values()]
        if timestamps:
            time_span = max(timestamps) - min(timestamps)
            decision_rate = len(timestamps) / time_span if time_span > 0 else 0
        else:
            time_span = 0
            decision_rate = 0
        
        return {
            'total_decisions': len(self.decisions),
            'type_distribution': type_distribution,
            'outcome_distribution': outcome_distribution,
            'voting_patterns': voting_patterns,
            'temporal_analysis': {
                'time_span_seconds': time_span,
                'decision_rate_per_second': decision_rate,
                'earliest_decision': min(timestamps) if timestamps else 0,
                'latest_decision': max(timestamps) if timestamps else 0
            },
            'consensus_analysis': {
                'average_approval_rate': sum(1 for d in self.decisions.values() if d.decision == "approved") / len(self.decisions),
                'high_consensus_decisions': sum(1 for d in self.decisions.values() 
                                              if sum(1 for v in d.voting_record.values() if v == "yes") / len(d.voting_record) >= 0.9),
                'controversial_decisions': sum(1 for d in self.decisions.values() 
                                             if abs(sum(1 for v in d.voting_record.values() if v == "yes") - 
                                                   sum(1 for v in d.voting_record.values() if v == "no")) <= 1)
            }
        }
    
    def export_council_data(self) -> Dict[str, Any]:
        """Export council data for external use."""
        return {
            'export_timestamp': time.time(),
            'council_status': self.get_council_status(),
            'sessions': [
                {
                    'id': session.id,
                    'session_type': session.session_type,
                    'agenda': session.agenda,
                    'decisions': session.decisions,
                    'start_time': session.start_time,
                    'end_time': session.end_time,
                    'status': session.status.value,
                    'participants': [member.value for member in session.participants],
                    'session_notes': session.session_notes
                }
                for session in self.active_sessions.values()
            ],
            'decisions': [
                {
                    'id': decision.id,
                    'decision_type': decision.decision_type.value,
                    'subject': decision.subject,
                    'description': decision.description,
                    'decision': decision.decision,
                    'rationale': decision.rationale,
                    'voting_record': {member.value: vote for member, vote in decision.voting_record.items()},
                    'timestamp': decision.timestamp,
                    'effective_date': decision.effective_date,
                    'review_date': decision.review_date,
                    'metadata': decision.metadata
                }
                for decision in self.decisions.values()
            ],
            'analytics': self.get_decision_analytics()
        }


# Global instance
_council_integration = None

def get_council_integration() -> CouncilIntegration:
    """Get the global council integration instance."""
    global _council_integration
    if _council_integration is None:
        _council_integration = CouncilIntegration()
    return _council_integration


if __name__ == "__main__":
    # Test the council integration system
    def test_council_integration():
        print("🏛️ Testing Council Integration System")
        print("=" * 50)
        
        # Initialize council
        council = get_council_integration()
        
        # Start a session
        session_id = council.start_session(
            "Research Approval Session",
            [
                "Approve new research protocol",
                "Review safety measures",
                "Allocate resources for testing"
            ],
            [CouncilMember.CHAIR, CouncilMember.RESEARCH_LEAD, CouncilMember.SAFETY_OFFICER]
        )
        
        print(f"✅ Started council session: {session_id}")
        
        # Make decisions
        decision1_id = council.make_decision(
            session_id,
            DecisionType.RESEARCH_APPROVAL,
            "New Research Protocol",
            "Approval for new research protocol implementation",
            {
                CouncilMember.CHAIR: "yes",
                CouncilMember.RESEARCH_LEAD: "yes",
                CouncilMember.SAFETY_OFFICER: "yes"
            },
            "Protocol meets all safety and research standards"
        )
        
        decision2_id = council.make_decision(
            session_id,
            DecisionType.RESOURCE_ALLOCATION,
            "Resource Allocation",
            "Allocation of computational resources for testing",
            {
                CouncilMember.CHAIR: "yes",
                CouncilMember.RESEARCH_LEAD: "yes",
                CouncilMember.SAFETY_OFFICER: "abstain"
            },
            "Resources are available and properly allocated"
        )
        
        print(f"✅ Made decisions: {decision1_id}, {decision2_id}")
        
        # End session
        council.end_session(session_id, "Successful session with all agenda items addressed")
        
        # Get council status
        status = council.get_council_status()
        print(f"\n📊 Council Status:")
        print(f"   Status: {status['status']}")
        print(f"   Total Decisions: {status['total_decisions']}")
        print(f"   Approval Rate: {status['decision_statistics']['approval_rate']:.2%}")
        print(f"   Active Sessions: {status['active_sessions']}")
        
        # Get decision analytics
        analytics = council.get_decision_analytics()
        print(f"\n📈 Decision Analytics:")
        print(f"   Type Distribution: {analytics.get('type_distribution', {})}")
        print(f"   Outcome Distribution: {analytics.get('outcome_distribution', {})}")
        print(f"   Decision Rate: {analytics.get('temporal_analysis', {}).get('decision_rate_per_second', 0):.2f}/sec")
        
        # Get recent decisions
        recent = council.get_recent_decisions(2)
        print(f"\n📋 Recent Decisions:")
        for decision in recent:
            print(f"   - {decision.subject}: {decision.decision}")
        
        # Export council data
        exported = council.export_council_data()
        print(f"\n📤 Exported council data: {len(exported['decisions'])} decisions, {len(exported['sessions'])} sessions")
        
        print("\n✅ Council integration system test completed!")
    
    # Run test
    test_council_integration()

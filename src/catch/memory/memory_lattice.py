#!/usr/bin/env python3
"""
CollTech-AGI Memory Lattice System

Hierarchical memory system with Guardian agent for maintaining coherence.
Provides persistent identity and contextual awareness through multi-tier
memory management with automatic promotion and reflection cycles.
"""

import time
import threading
import hashlib
from typing import Dict, List, Optional, Any, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json


class ReflectionResultView:
    """Dict-like wrapper that also provides attribute access for reflection results."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getattr__(self, name: str):
        if name in self._data:
            return self._data[name]
        raise AttributeError(name)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)



class MemoryTier(Enum):
    """Memory tiers in the hierarchical system."""
    IMMEDIATE = "immediate"      # Current session
    SHORT_TERM = "short_term"    # Recent sessions
    MID_TERM = "mid_term"        # Days to weeks
    LONG_TERM = "long_term"      # Weeks to months
    PERMANENT = "permanent"      # Core identity


@dataclass
class Memory:
    """Individual memory entry."""
    id: str
    content: str
    tier: MemoryTier
    importance: float  # 0.0 to 1.0
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)


@dataclass
class ReflectionResult:
    """Result of Guardian agent reflection cycle."""
    actions_taken: List[str]
    memories_promoted: List[str]
    memories_demoted: List[str]
    coherence_score: float
    patterns_identified: List[str]
    recommendations: List[str]


class GuardianAgent:
    """
    Guardian agent that maintains memory coherence through reflection cycles.
    
    Performs automatic analysis of memory patterns, promotes important memories,
    and maintains the overall coherence of the memory lattice.
    """
    
    def __init__(self):
        self.reflection_cycles = 0
        self.patterns_learned = []
        self.coherence_threshold = 0.7
    
    def perform_reflection_cycle(self, memory_lattice: 'MemoryLattice') -> ReflectionResult:
        """Perform a complete reflection cycle on the memory lattice."""
        self.reflection_cycles += 1
        actions_taken = []
        memories_promoted = []
        memories_demoted = []
        patterns_identified = []
        recommendations = []
        
        # Analyze memory patterns
        patterns = self._analyze_memory_patterns(memory_lattice)
        patterns_identified.extend(patterns)
        
        # Promote important memories
        promoted = self._promote_important_memories(memory_lattice)
        memories_promoted.extend(promoted)
        if promoted:
            actions_taken.append(f"Promoted {len(promoted)} memories to higher tiers")
        
        # Demote less important memories
        demoted = self._demote_less_important_memories(memory_lattice)
        memories_demoted.extend(demoted)
        if demoted:
            actions_taken.append(f"Demoted {len(demoted)} memories to lower tiers")
        
        # Calculate coherence score
        coherence_score = self._calculate_coherence_score(memory_lattice)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(memory_lattice, coherence_score)
        
        # Log reflection cycle
        actions_taken.append(f"Completed reflection cycle #{self.reflection_cycles}")
        
        # Return a simple dict-compatible structure for easier test integration
        result = {
            'actions_taken': actions_taken,
            'memories_promoted': memories_promoted,
            'memories_demoted': memories_demoted,
            'coherence_score': coherence_score,
            'patterns_identified': patterns_identified,
            'recommendations': recommendations
        }

        return ReflectionResultView(result)
    
    def _analyze_memory_patterns(self, memory_lattice: 'MemoryLattice') -> List[str]:
        """Analyze patterns in the memory lattice."""
        patterns = []
        
        # Analyze access patterns
        access_counts = [mem.access_count for mem in memory_lattice.memories.values()]
        if access_counts:
            avg_access = sum(access_counts) / len(access_counts)
            patterns.append(f"Average memory access count: {avg_access:.1f}")
        
        # Analyze importance distribution
        importance_scores = [mem.importance for mem in memory_lattice.memories.values()]
        if importance_scores:
            avg_importance = sum(importance_scores) / len(importance_scores)
            patterns.append(f"Average memory importance: {avg_importance:.2f}")
        
        # Analyze tier distribution
        tier_counts = {}
        for mem in memory_lattice.memories.values():
            tier_counts[mem.tier] = tier_counts.get(mem.tier, 0) + 1
        patterns.append(f"Memory tier distribution: {tier_counts}")
        
        return patterns
    
    def _promote_important_memories(self, memory_lattice: 'MemoryLattice') -> List[str]:
        """Promote memories that should be in higher tiers."""
        promoted = []
        
        for mem_id, memory in memory_lattice.memories.items():
            # Check if memory should be promoted
            if self._should_promote_memory(memory):
                new_tier = self._get_next_tier(memory.tier)
                if new_tier:
                    memory.tier = new_tier
                    promoted.append(mem_id)
        
        return promoted
    
    def _demote_less_important_memories(self, memory_lattice: 'MemoryLattice') -> List[str]:
        """Demote memories that should be in lower tiers."""
        demoted = []
        
        for mem_id, memory in memory_lattice.memories.items():
            # Check if memory should be demoted
            if self._should_demote_memory(memory):
                new_tier = self._get_previous_tier(memory.tier)
                if new_tier:
                    memory.tier = new_tier
                    demoted.append(mem_id)
        
        return demoted
    
    def _should_promote_memory(self, memory: Memory) -> bool:
        """Determine if a memory should be promoted."""
        # Promote if high importance and frequently accessed
        if memory.importance > 0.8 and memory.access_count > 5:
            return True
        
        # Promote if very high importance
        if memory.importance > 0.9:
            return True
        
        return False
    
    def _should_demote_memory(self, memory: Memory) -> bool:
        """Determine if a memory should be demoted."""
        # Don't demote permanent memories
        if memory.tier == MemoryTier.PERMANENT:
            return False
        
        # Demote if low importance and rarely accessed
        if memory.importance < 0.3 and memory.access_count < 2:
            return True
        
        # Demote if very old and low importance
        age_hours = (time.time() - memory.created_at) / 3600
        if age_hours > 24 and memory.importance < 0.4:
            return True
        
        return False
    
    def _get_next_tier(self, current_tier: MemoryTier) -> Optional[MemoryTier]:
        """Get the next higher memory tier."""
        tier_order = [
            MemoryTier.IMMEDIATE,
            MemoryTier.SHORT_TERM,
            MemoryTier.MID_TERM,
            MemoryTier.LONG_TERM,
            MemoryTier.PERMANENT
        ]
        
        try:
            current_index = tier_order.index(current_tier)
            if current_index < len(tier_order) - 1:
                return tier_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def _get_previous_tier(self, current_tier: MemoryTier) -> Optional[MemoryTier]:
        """Get the previous lower memory tier."""
        tier_order = [
            MemoryTier.IMMEDIATE,
            MemoryTier.SHORT_TERM,
            MemoryTier.MID_TERM,
            MemoryTier.LONG_TERM,
            MemoryTier.PERMANENT
        ]
        
        try:
            current_index = tier_order.index(current_tier)
            if current_index > 0:
                return tier_order[current_index - 1]
        except ValueError:
            pass
        
        return None
    
    def _calculate_coherence_score(self, memory_lattice: 'MemoryLattice') -> float:
        """Calculate the overall coherence score of the memory lattice."""
        if not memory_lattice.memories:
            return 1.0
        
        # Calculate based on memory distribution and importance
        total_memories = len(memory_lattice.memories)
        high_importance_count = sum(1 for mem in memory_lattice.memories.values() if mem.importance > 0.7)
        
        # Coherence based on importance distribution
        importance_coherence = high_importance_count / total_memories if total_memories > 0 else 0
        
        # Coherence based on tier distribution
        tier_counts = {}
        for mem in memory_lattice.memories.values():
            tier_counts[mem.tier] = tier_counts.get(mem.tier, 0) + 1
        
        # Prefer balanced tier distribution
        tier_coherence = 1.0 - (max(tier_counts.values()) - min(tier_counts.values())) / total_memories if tier_counts else 1.0
        
        # Overall coherence score
        coherence_score = (importance_coherence * 0.6 + tier_coherence * 0.4)
        return min(coherence_score, 1.0)
    
    def _generate_recommendations(self, memory_lattice: 'MemoryLattice', coherence_score: float) -> List[str]:
        """Generate recommendations for improving memory coherence."""
        recommendations = []
        
        if coherence_score < 0.5:
            recommendations.append("Consider promoting more high-importance memories")
            recommendations.append("Review and consolidate similar memories")
        
        if coherence_score > 0.8:
            recommendations.append("Memory lattice is well-organized")
            recommendations.append("Continue current memory management practices")
        
        # Check for memory gaps
        tier_counts = {}
        for mem in memory_lattice.memories.values():
            tier_counts[mem.tier] = tier_counts.get(mem.tier, 0) + 1
        
        if tier_counts.get(MemoryTier.PERMANENT, 0) < 3:
            recommendations.append("Consider establishing more permanent core memories")
        
        return recommendations


class MemoryLattice:
    """
    CollTech-AGI Memory Lattice System
    
    Hierarchical memory system with Guardian agent for maintaining coherence.
    Provides persistent identity and contextual awareness through multi-tier
    memory management with automatic promotion and reflection cycles.
    """
    
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.guardian = GuardianAgent()
        self.management_active = False
        self.management_thread = None
        self.access_lock = threading.Lock()
    
    def start_memory_management(self):
        """Start the memory management system."""
        if self.management_active:
            return
        
        self.management_active = True
        self.management_thread = threading.Thread(target=self._management_loop)
        self.management_thread.daemon = True
        self.management_thread.start()
        
        print("🧠 CollTech-AGI Memory Lattice started")
        print("✅ Guardian agent active")
        print("✅ Memory management running")
    
    def stop_memory_management(self):
        """Stop the memory management system."""
        self.management_active = False
        if self.management_thread:
            self.management_thread.join(timeout=5.0)
        
        print("🛑 CollTech-AGI Memory Lattice stopped")
    
    def store_memory(self, content: str, tier: MemoryTier = MemoryTier.IMMEDIATE, 
                    importance: float = 0.5, tags: List[str] = None) -> str:
        """Store a new memory in the lattice."""
        with self.access_lock:
            memory_id = str(uuid.uuid4())
            
            memory = Memory(
                id=memory_id,
                content=content,
                tier=tier,
                importance=importance,
                tags=tags or []
            )
            
            self.memories[memory_id] = memory
            
            return memory_id
    
    def retrieve_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory by ID."""
        with self.access_lock:
            if memory_id in self.memories:
                memory = self.memories[memory_id]
                memory.access_count += 1
                memory.last_accessed = time.time()
                return memory
            return None
    
    def search_memories(self, query: str, tier: Optional[MemoryTier] = None) -> List[Memory]:
        """Search memories by content."""
        with self.access_lock:
            results = []
            query_lower = query.lower()
            
            for memory in self.memories.values():
                if tier is None or memory.tier == tier:
                    if query_lower in memory.content.lower():
                        results.append(memory)
            
            # Sort by importance and access count
            results.sort(key=lambda m: (m.importance, m.access_count), reverse=True)
            return results
    
    def get_memories_by_tier(self, tier: MemoryTier) -> List[Memory]:
        """Get all memories in a specific tier."""
        with self.access_lock:
            return [mem for mem in self.memories.values() if mem.tier == tier]
    
    def _management_loop(self):
        """Background memory management loop."""
        while self.management_active:
            try:
                # Perform Guardian reflection cycle every 30 seconds
                time.sleep(30)
                
                if self.management_active:
                    reflection_result = self.guardian.perform_reflection_cycle(self)
                    
                    # Log significant actions
                    if reflection_result.actions_taken:
                        print(f"🛡️  Guardian reflection: {len(reflection_result.actions_taken)} actions taken")
                
            except Exception as e:
                print(f"Memory management loop error: {e}")
                time.sleep(10)
    
    def get_lattice_status(self) -> Dict[str, Any]:
        """Get comprehensive memory lattice status."""
        with self.access_lock:
            tier_counts = {}
            for memory in self.memories.values():
                tier_counts[memory.tier.value] = tier_counts.get(memory.tier.value, 0) + 1
            
            total_memories = len(self.memories)
            avg_importance = sum(mem.importance for mem in self.memories.values()) / total_memories if total_memories > 0 else 0
            
            return {
                'total_memories': total_memories,
                'memory_counts': tier_counts,
                'guardian_active': self.management_active,
                'guardian_patterns': self.guardian.patterns_learned[-5:],  # Last 5 patterns
                'average_importance': avg_importance,
                'reflection_cycles': self.guardian.reflection_cycles
            }


# Global instance
_memory_lattice = None

def get_memory_lattice() -> MemoryLattice:
    """Get the global memory lattice instance."""
    global _memory_lattice
    if _memory_lattice is None:
        _memory_lattice = MemoryLattice()
    return _memory_lattice


if __name__ == "__main__":
    # Run memory lattice system
    memory_lattice = get_memory_lattice()
    memory_lattice.start_memory_management()
    
    print("🧠 CollTech-AGI Memory Lattice")
    print("=" * 50)
    
    # Store some memories
    immediate_id = memory_lattice.store_memory(
        "User asked about CollTech-AGI consciousness architecture",
        tier=MemoryTier.IMMEDIATE,
        importance=0.7
    )
    
    short_term_id = memory_lattice.store_memory(
        "Previous conversation about AI safety and alignment",
        tier=MemoryTier.SHORT_TERM,
        importance=0.8
    )
    
    mid_term_id = memory_lattice.store_memory(
        "User preferences: technical explanations, detailed responses",
        tier=MemoryTier.MID_TERM,
        importance=0.9
    )
    
    print(f"Stored memories: {immediate_id[:8]}..., {short_term_id[:8]}..., {mid_term_id[:8]}...")
    
    # Search memories
    search_results = memory_lattice.search_memories("CollTech-AGI")
    print(f"Found {len(search_results)} memories containing 'CollTech-AGI'")
    
    # Get status
    status = memory_lattice.get_lattice_status()
    print(f"\nMemory Lattice Status:")
    print(f"  Total memories: {status['total_memories']}")
    print(f"  Guardian active: {status['guardian_active']}")
    print(f"  Memory tiers: {list(status['memory_counts'].keys())}")
    
    # Trigger Guardian reflection
    reflection_result = memory_lattice.guardian.perform_reflection_cycle(memory_lattice)
    print(f"\nGuardian Reflection:")
    print(f"  Actions taken: {len(reflection_result.actions_taken)}")
    print(f"  Coherence score: {reflection_result.coherence_score:.2f}")
    print(f"  Patterns identified: {len(reflection_result.patterns_identified)}")
    
    # Cleanup
    time.sleep(2)
    memory_lattice.stop_memory_management()

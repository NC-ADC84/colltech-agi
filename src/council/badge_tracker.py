#!/usr/bin/env python3
"""
CollTech-AGI Council Badge Tracker

Advanced badge tracking system for monitoring user progress,
achievements, and badge management in the CollTech-AGI ecosystem.
"""

import time
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

from .badge_system import BadgeSystem, Badge, BadgeCategory, BadgeProgression

logger = logging.getLogger(__name__)


class BadgeStatus(Enum):
    """Badge status."""
    LOCKED = "locked"          # Not yet available
    AVAILABLE = "available"    # Can be earned
    IN_PROGRESS = "in_progress"  # Partially completed
    EARNED = "earned"          # Fully earned
    MASTERED = "mastered"      # Fully mastered


@dataclass
class BadgeProgress:
    """Badge progress tracking."""
    badge_id: str
    user_id: str
    status: BadgeStatus
    progress_percentage: float
    current_values: Dict[str, Any] = field(default_factory=dict)
    earned_at: Optional[float] = None
    mastered_at: Optional[float] = None
    last_updated: float = 0.0
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = time.time()


@dataclass
class UserBadge:
    """User badge record."""
    user_id: str
    badge_id: str
    earned_at: float
    progression_level: BadgeProgression
    experience_points: int
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.earned_at:
            self.earned_at = time.time()


@dataclass
class UserStats:
    """User statistics for badge tracking."""
    user_id: str
    stats: Dict[str, Any] = field(default_factory=dict)
    last_updated: float = 0.0
    total_experience: int = 0
    badges_earned: int = 0
    badges_mastered: int = 0
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = time.time()


class BadgeTracker:
    """
    Council Badge Tracker
    
    Tracks user progress, manages badge earning, and provides
    comprehensive badge management for the CollTech-AGI system.
    """
    
    def __init__(self, badge_system: BadgeSystem, data_file: str = "data/badge_tracker.json"):
        self.badge_system = badge_system
        self.data_file = Path(data_file)
        
        # User data
        self.user_stats: Dict[str, UserStats] = {}
        self.user_badges: Dict[str, List[UserBadge]] = {}  # user_id -> badges
        self.badge_progress: Dict[str, List[BadgeProgress]] = {}  # user_id -> progress
        
        # Load existing data
        self._load_data()
        
        logger.info("📊 Badge Tracker initialized")
        logger.info(f"   Tracking {len(self.user_stats)} users")
        logger.info(f"   Total badges earned: {sum(len(badges) for badges in self.user_badges.values())}")
    
    def _load_data(self):
        """Load badge tracking data from file."""
        try:
            if not self.data_file.exists():
                logger.info("No existing badge data found, starting fresh")
                return
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load user stats
            for user_id, stats_data in data.get('user_stats', {}).items():
                self.user_stats[user_id] = UserStats(
                    user_id=user_id,
                    stats=stats_data.get('stats', {}),
                    last_updated=stats_data.get('last_updated', time.time()),
                    total_experience=stats_data.get('total_experience', 0),
                    badges_earned=stats_data.get('badges_earned', 0),
                    badges_mastered=stats_data.get('badges_mastered', 0)
                )
            
            # Load user badges
            for user_id, badges_data in data.get('user_badges', {}).items():
                user_badges = []
                for badge_data in badges_data:
                    user_badge = UserBadge(
                        user_id=user_id,
                        badge_id=badge_data['badge_id'],
                        earned_at=badge_data['earned_at'],
                        progression_level=BadgeProgression(badge_data['progression_level']),
                        experience_points=badge_data['experience_points'],
                        is_active=badge_data.get('is_active', True),
                        metadata=badge_data.get('metadata', {})
                    )
                    user_badges.append(user_badge)
                self.user_badges[user_id] = user_badges
            
            # Load badge progress
            for user_id, progress_data in data.get('badge_progress', {}).items():
                user_progress = []
                for progress_item in progress_data:
                    progress = BadgeProgress(
                        badge_id=progress_item['badge_id'],
                        user_id=user_id,
                        status=BadgeStatus(progress_item['status']),
                        progress_percentage=progress_item['progress_percentage'],
                        current_values=progress_item.get('current_values', {}),
                        earned_at=progress_item.get('earned_at'),
                        mastered_at=progress_item.get('mastered_at'),
                        last_updated=progress_item.get('last_updated', time.time())
                    )
                    user_progress.append(progress)
                self.badge_progress[user_id] = user_progress
            
            logger.info("✅ Badge tracking data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading badge tracking data: {e}")
    
    def _save_data(self):
        """Save badge tracking data to file."""
        try:
            # Ensure data directory exists
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'user_stats': {},
                'user_badges': {},
                'badge_progress': {},
                'last_saved': time.time()
            }
            
            # Save user stats
            for user_id, user_stats in self.user_stats.items():
                data['user_stats'][user_id] = {
                    'stats': user_stats.stats,
                    'last_updated': user_stats.last_updated,
                    'total_experience': user_stats.total_experience,
                    'badges_earned': user_stats.badges_earned,
                    'badges_mastered': user_stats.badges_mastered
                }
            
            # Save user badges
            for user_id, badges in self.user_badges.items():
                data['user_badges'][user_id] = []
                for badge in badges:
                    data['user_badges'][user_id].append({
                        'badge_id': badge.badge_id,
                        'earned_at': badge.earned_at,
                        'progression_level': badge.progression_level.value,
                        'experience_points': badge.experience_points,
                        'is_active': badge.is_active,
                        'metadata': badge.metadata
                    })
            
            # Save badge progress
            for user_id, progress_list in self.badge_progress.items():
                data['badge_progress'][user_id] = []
                for progress in progress_list:
                    data['badge_progress'][user_id].append({
                        'badge_id': progress.badge_id,
                        'status': progress.status.value,
                        'progress_percentage': progress.progress_percentage,
                        'current_values': progress.current_values,
                        'earned_at': progress.earned_at,
                        'mastered_at': progress.mastered_at,
                        'last_updated': progress.last_updated
                    })
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info("✅ Badge tracking data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving badge tracking data: {e}")
    
    def get_user_stats(self, user_id: str) -> UserStats:
        """Get or create user stats."""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = UserStats(user_id=user_id)
        return self.user_stats[user_id]
    
    def update_user_stat(self, user_id: str, stat_name: str, value: Any):
        """Update a user statistic."""
        user_stats = self.get_user_stats(user_id)
        user_stats.stats[stat_name] = value
        user_stats.last_updated = time.time()
        
        # Check for new badges
        self._check_badge_progress(user_id)
        
        logger.info(f"📊 Updated stat for {user_id}: {stat_name} = {value}")
    
    def increment_user_stat(self, user_id: str, stat_name: str, increment: int = 1):
        """Increment a user statistic."""
        user_stats = self.get_user_stats(user_id)
        current_value = user_stats.stats.get(stat_name, 0)
        new_value = current_value + increment
        self.update_user_stat(user_id, stat_name, new_value)
    
    def _check_badge_progress(self, user_id: str):
        """Check and update badge progress for a user."""
        user_stats = self.get_user_stats(user_id)
        
        # Get all badges
        all_badges = list(self.badge_system.badges.values())
        
        # Initialize progress tracking if needed
        if user_id not in self.badge_progress:
            self.badge_progress[user_id] = []
        
        # Check each badge
        for badge in all_badges:
            progress = self._get_or_create_progress(user_id, badge.id)
            
            # Check if badge is already earned
            if progress.status == BadgeStatus.EARNED:
                continue
            
            # Check requirements
            if self.badge_system.check_requirements(badge.id, user_stats.stats):
                # Badge can be earned
                if progress.status != BadgeStatus.EARNED:
                    self._award_badge(user_id, badge)
                    progress.status = BadgeStatus.EARNED
                    progress.earned_at = time.time()
                    progress.progress_percentage = 100.0
            else:
                # Calculate progress
                progress_percentage = self._calculate_progress(badge, user_stats.stats)
                progress.progress_percentage = progress_percentage
                progress.current_values = user_stats.stats.copy()
                
                if progress_percentage > 0:
                    progress.status = BadgeStatus.IN_PROGRESS
                else:
                    progress.status = BadgeStatus.AVAILABLE
            
            progress.last_updated = time.time()
    
    def _get_or_create_progress(self, user_id: str, badge_id: str) -> BadgeProgress:
        """Get or create badge progress for a user."""
        progress_list = self.badge_progress.get(user_id, [])
        
        for progress in progress_list:
            if progress.badge_id == badge_id:
                return progress
        
        # Create new progress
        progress = BadgeProgress(
            badge_id=badge_id,
            user_id=user_id,
            status=BadgeStatus.AVAILABLE,
            progress_percentage=0.0
        )
        
        if user_id not in self.badge_progress:
            self.badge_progress[user_id] = []
        self.badge_progress[user_id].append(progress)
        
        return progress
    
    def _calculate_progress(self, badge: Badge, user_stats: Dict[str, Any]) -> float:
        """Calculate progress percentage for a badge."""
        if not badge.requirements:
            return 0.0
        
        total_progress = 0.0
        for requirement in badge.requirements:
            user_value = user_stats.get(requirement.name, 0)
            requirement_value = requirement.value
            
            if requirement_value > 0:
                progress = min(user_value / requirement_value, 1.0)
                total_progress += progress
        
        return (total_progress / len(badge.requirements)) * 100.0
    
    def _award_badge(self, user_id: str, badge: Badge):
        """Award a badge to a user."""
        # Create user badge record
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge.id,
            progression_level=badge.progression,
            experience_points=badge.rewards.experience_points
        )
        
        # Add to user badges
        if user_id not in self.user_badges:
            self.user_badges[user_id] = []
        self.user_badges[user_id].append(user_badge)
        
        # Update user stats
        user_stats = self.get_user_stats(user_id)
        user_stats.badges_earned += 1
        user_stats.total_experience += badge.rewards.experience_points
        
        logger.info(f"🏆 Awarded badge {badge.name} to user {user_id}")
    
    def get_user_badges(self, user_id: str) -> List[UserBadge]:
        """Get all badges earned by a user."""
        return self.user_badges.get(user_id, [])
    
    def get_user_progress(self, user_id: str) -> List[BadgeProgress]:
        """Get all badge progress for a user."""
        return self.badge_progress.get(user_id, [])
    
    def get_user_badge_progress(self, user_id: str, badge_id: str) -> Optional[BadgeProgress]:
        """Get specific badge progress for a user."""
        progress_list = self.badge_progress.get(user_id, [])
        for progress in progress_list:
            if progress.badge_id == badge_id:
                return progress
        return None
    
    def get_user_available_badges(self, user_id: str) -> List[Badge]:
        """Get badges that user can earn."""
        user_stats = self.get_user_stats(user_id)
        return self.badge_system.get_available_badges(user_stats.stats)
    
    def get_user_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user leaderboard by experience points."""
        leaderboard = []
        
        for user_id, user_stats in self.user_stats.items():
            badges_count = len(self.user_badges.get(user_id, []))
            leaderboard.append({
                'user_id': user_id,
                'total_experience': user_stats.total_experience,
                'badges_earned': badges_count,
                'last_updated': user_stats.last_updated
            })
        
        # Sort by experience points
        leaderboard.sort(key=lambda x: x['total_experience'], reverse=True)
        
        return leaderboard[:limit]
    
    def get_badge_statistics(self) -> Dict[str, Any]:
        """Get badge system statistics."""
        total_users = len(self.user_stats)
        total_badges_earned = sum(len(badges) for badges in self.user_badges.values())
        
        # Category distribution
        category_distribution = {}
        for user_id, badges in self.user_badges.items():
            for badge in badges:
                badge_def = self.badge_system.get_badge(badge.badge_id)
                if badge_def:
                    category = badge_def.category.value
                    category_distribution[category] = category_distribution.get(category, 0) + 1
        
        # Progression distribution
        progression_distribution = {}
        for user_id, badges in self.user_badges.items():
            for badge in badges:
                progression = badge.progression_level.value
                progression_distribution[progression] = progression_distribution.get(progression, 0) + 1
        
        return {
            'total_users': total_users,
            'total_badges_earned': total_badges_earned,
            'average_badges_per_user': total_badges_earned / total_users if total_users > 0 else 0,
            'category_distribution': category_distribution,
            'progression_distribution': progression_distribution,
            'most_earned_badge': self._get_most_earned_badge(),
            'least_earned_badge': self._get_least_earned_badge()
        }
    
    def _get_most_earned_badge(self) -> Optional[str]:
        """Get the most earned badge."""
        badge_counts = {}
        for user_id, badges in self.user_badges.items():
            for badge in badges:
                badge_counts[badge.badge_id] = badge_counts.get(badge.badge_id, 0) + 1
        
        if badge_counts:
            return max(badge_counts, key=badge_counts.get)
        return None
    
    def _get_least_earned_badge(self) -> Optional[str]:
        """Get the least earned badge."""
        badge_counts = {}
        for user_id, badges in self.user_badges.items():
            for badge in badges:
                badge_counts[badge.badge_id] = badge_counts.get(badge.badge_id, 0) + 1
        
        if badge_counts:
            return min(badge_counts, key=badge_counts.get)
        return None
    
    def save_data(self):
        """Save badge tracking data."""
        self._save_data()
    
    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user summary."""
        user_stats = self.get_user_stats(user_id)
        badges = self.get_user_badges(user_id)
        progress = self.get_user_progress(user_id)
        
        # Calculate additional metrics
        in_progress_count = sum(1 for p in progress if p.status == BadgeStatus.IN_PROGRESS)
        available_count = sum(1 for p in progress if p.status == BadgeStatus.AVAILABLE)
        
        # Category breakdown
        category_breakdown = {}
        for badge in badges:
            badge_def = self.badge_system.get_badge(badge.badge_id)
            if badge_def:
                category = badge_def.category.value
                category_breakdown[category] = category_breakdown.get(category, 0) + 1
        
        return {
            'user_id': user_id,
            'total_experience': user_stats.total_experience,
            'badges_earned': len(badges),
            'badges_in_progress': in_progress_count,
            'badges_available': available_count,
            'category_breakdown': category_breakdown,
            'last_updated': user_stats.last_updated,
            'recent_badges': [b.badge_id for b in sorted(badges, key=lambda x: x.earned_at, reverse=True)[:5]]
        }


# Global instance
_badge_tracker = None

def get_badge_tracker(badge_system: BadgeSystem = None, data_file: str = "data/badge_tracker.json") -> BadgeTracker:
    """Get the global badge tracker instance."""
    global _badge_tracker
    if _badge_tracker is None:
        if badge_system is None:
            from .badge_system import get_badge_system
            badge_system = get_badge_system()
        _badge_tracker = BadgeTracker(badge_system, data_file)
    return _badge_tracker


if __name__ == "__main__":
    # Test the badge tracker
    def test_badge_tracker():
        print("📊 Testing Badge Tracker")
        print("=" * 50)
        
        # Initialize badge system and tracker
        from .badge_system import get_badge_system
        badge_system = get_badge_system()
        tracker = get_badge_tracker(badge_system)
        
        # Test user
        test_user_id = "test_user_123"
        
        # Update user stats
        tracker.update_user_stat(test_user_id, "tests_completed", 50)
        tracker.update_user_stat(test_user_id, "success_rate", 0.95)
        tracker.update_user_stat(test_user_id, "continuity_score", 0.90)
        
        print(f"✅ Updated stats for {test_user_id}")
        
        # Get user summary
        summary = tracker.get_user_summary(test_user_id)
        print(f"\n📊 User Summary:")
        print(f"   Total Experience: {summary['total_experience']}")
        print(f"   Badges Earned: {summary['badges_earned']}")
        print(f"   Badges In Progress: {summary['badges_in_progress']}")
        print(f"   Badges Available: {summary['badges_available']}")
        
        # Get user badges
        badges = tracker.get_user_badges(test_user_id)
        print(f"\n🏆 User Badges ({len(badges)}):")
        for badge in badges:
            badge_def = badge_system.get_badge(badge.badge_id)
            if badge_def:
                print(f"   - {badge_def.icon} {badge_def.name} ({badge_def.category.value})")
        
        # Get user progress
        progress = tracker.get_user_progress(test_user_id)
        print(f"\n📈 User Progress ({len(progress)} badges tracked):")
        for prog in progress[:5]:  # Show first 5
            badge_def = badge_system.get_badge(prog.badge_id)
            if badge_def:
                print(f"   - {badge_def.icon} {badge_def.name}: {prog.progress_percentage:.1f}% ({prog.status.value})")
        
        # Get leaderboard
        leaderboard = tracker.get_user_leaderboard(5)
        print(f"\n🏅 Top 5 Users:")
        for i, user in enumerate(leaderboard, 1):
            print(f"   {i}. User {user['user_id']}: {user['total_experience']} XP, {user['badges_earned']} badges")
        
        # Get badge statistics
        stats = tracker.get_badge_statistics()
        print(f"\n📊 Badge Statistics:")
        print(f"   Total Users: {stats['total_users']}")
        print(f"   Total Badges Earned: {stats['total_badges_earned']}")
        print(f"   Average Badges per User: {stats['average_badges_per_user']:.1f}")
        print(f"   Category Distribution: {stats['category_distribution']}")
        
        # Save data
        tracker.save_data()
        print(f"\n💾 Badge tracking data saved")
        
        print("\n✅ Badge tracker test completed!")
    
    # Run test
    test_badge_tracker()

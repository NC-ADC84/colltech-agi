#!/usr/bin/env python3
"""
CollTech-AGI Council System

Advanced council management system including:
- Council Badge System
- Badge Management and Tracking
- Discord Integration
- Achievement System
- Role Management

Integrated with CollTech-AGI consciousness system for comprehensive council capabilities.
"""

from .badge_system import BadgeSystem, Badge, BadgeCategory, BadgeProgression
from .badge_tracker import BadgeTracker, UserBadge, BadgeProgress
from .discord_integration import DiscordBadgeIntegration, BadgeDisplay
from .achievement_system import AchievementSystem, Achievement, AchievementType

__all__ = [
    'BadgeSystem',
    'Badge',
    'BadgeCategory', 
    'BadgeProgression',
    'BadgeTracker',
    'UserBadge',
    'BadgeProgress',
    'DiscordBadgeIntegration',
    'BadgeDisplay',
    'AchievementSystem',
    'Achievement',
    'AchievementType'
]

__version__ = "1.0.0"
__author__ = "CollTech-AGI Council Team"

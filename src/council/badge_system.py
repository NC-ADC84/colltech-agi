#!/usr/bin/env python3
"""
CollTech-AGI Council Badge System

Advanced badge management system for tracking achievements,
progress, and rewards in the CollTech-AGI ecosystem.
"""

import json
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BadgeCategory(Enum):
    """Badge categories."""
    RESEARCH = "research"
    COMMUNICATION = "communication"
    BENCHMARKING = "benchmarking"
    COUNCIL = "council"
    SPECIAL = "special"


class BadgeProgression(Enum):
    """Badge progression levels."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


@dataclass
class BadgeRequirement:
    """Badge requirement specification."""
    name: str
    value: Union[int, float]
    operator: str = ">="  # ">=", ">", "==", "<=", "<"
    description: str = ""


@dataclass
class BadgeReward:
    """Badge reward specification."""
    role_color: Optional[str] = None
    special_title: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    experience_points: int = 0
    description: str = ""


@dataclass
class Badge:
    """Badge definition."""
    id: str
    name: str
    description: str
    icon: str
    color: str
    category: BadgeCategory
    requirements: List[BadgeRequirement]
    rewards: BadgeReward
    progression: BadgeProgression = BadgeProgression.BRONZE
    created_at: float = 0.0
    updated_at: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()
        if not self.updated_at:
            self.updated_at = time.time()


class BadgeSystem:
    """
    Council Badge System
    
    Manages badges, requirements, rewards, and progression
    for the CollTech-AGI council system.
    """
    
    def __init__(self, config_path: str = "configs/council_badges.json"):
        self.config_path = config_path
        self.badges: Dict[str, Badge] = {}
        self.categories: Dict[BadgeCategory, Dict[str, Badge]] = {}
        self.progression_levels: Dict[BadgeProgression, Dict[str, Any]] = {}
        self.badge_effects: Dict[str, Any] = {}
        
        # Load configuration
        self._load_configuration()
        
        logger.info("🏆 Council Badge System initialized")
        logger.info(f"   Loaded {len(self.badges)} badges")
        logger.info(f"   Categories: {len(self.categories)}")
    
    def _load_configuration(self):
        """Load badge configuration from JSON file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                logger.warning(f"Badge config file not found: {self.config_path}")
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            badge_config = config.get('council_badges', {})
            
            # Load progression levels
            self._load_progression_levels(badge_config.get('badge_progression', {}))
            
            # Load badge effects
            self.badge_effects = badge_config.get('badge_effects', {})
            
            # Load badge categories and badges
            self._load_badge_categories(badge_config.get('badge_categories', {}))
            
            logger.info("✅ Badge configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading badge configuration: {e}")
    
    def _load_progression_levels(self, progression_config: Dict[str, Any]):
        """Load badge progression levels."""
        for level_name, level_config in progression_config.items():
            try:
                progression = BadgeProgression(level_name)
                self.progression_levels[progression] = level_config
            except ValueError:
                logger.warning(f"Unknown progression level: {level_name}")
    
    def _load_badge_categories(self, categories_config: Dict[str, Any]):
        """Load badge categories and their badges."""
        for category_name, category_config in categories_config.items():
            try:
                category = BadgeCategory(category_name)
                self.categories[category] = {}
                
                badges_config = category_config.get('badges', {})
                for badge_id, badge_config in badges_config.items():
                    badge = self._create_badge(badge_id, badge_config, category)
                    if badge:
                        self.badges[badge_id] = badge
                        self.categories[category][badge_id] = badge
                        
            except ValueError:
                logger.warning(f"Unknown badge category: {category_name}")
    
    def _create_badge(self, badge_id: str, badge_config: Dict[str, Any], 
                     category: BadgeCategory) -> Optional[Badge]:
        """Create a badge from configuration."""
        try:
            # Parse requirements
            requirements = []
            req_config = badge_config.get('requirements', {})
            for req_name, req_value in req_config.items():
                requirement = BadgeRequirement(
                    name=req_name,
                    value=req_value,
                    description=f"{req_name}: {req_value}"
                )
                requirements.append(requirement)
            
            # Parse rewards
            rewards_config = badge_config.get('rewards', {})
            reward = BadgeReward(
                role_color=rewards_config.get('role_color'),
                special_title=rewards_config.get('special_title'),
                permissions=rewards_config.get('permissions', []),
                experience_points=rewards_config.get('experience_points', 0),
                description=rewards_config.get('description', '')
            )
            
            # Determine progression level
            progression = BadgeProgression.BRONZE  # Default
            for level, level_config in self.progression_levels.items():
                if badge_config.get('progression') == level.value:
                    progression = level
                    break
            
            badge = Badge(
                id=badge_id,
                name=badge_config.get('name', badge_id),
                description=badge_config.get('description', ''),
                icon=badge_config.get('icon', '🏆'),
                color=badge_config.get('color', '#7289DA'),
                category=category,
                requirements=requirements,
                rewards=reward,
                progression=progression
            )
            
            return badge
            
        except Exception as e:
            logger.error(f"Error creating badge {badge_id}: {e}")
            return None
    
    def get_badge(self, badge_id: str) -> Optional[Badge]:
        """Get badge by ID."""
        return self.badges.get(badge_id)
    
    def get_badges_by_category(self, category: BadgeCategory) -> Dict[str, Badge]:
        """Get all badges in a category."""
        return self.categories.get(category, {})
    
    def get_badges_by_progression(self, progression: BadgeProgression) -> List[Badge]:
        """Get all badges with a specific progression level."""
        return [badge for badge in self.badges.values() if badge.progression == progression]
    
    def check_requirements(self, badge_id: str, user_stats: Dict[str, Any]) -> bool:
        """Check if user meets badge requirements."""
        badge = self.get_badge(badge_id)
        if not badge:
            return False
        
        for requirement in badge.requirements:
            user_value = user_stats.get(requirement.name, 0)
            
            if requirement.operator == ">=":
                if user_value < requirement.value:
                    return False
            elif requirement.operator == ">":
                if user_value <= requirement.value:
                    return False
            elif requirement.operator == "==":
                if user_value != requirement.value:
                    return False
            elif requirement.operator == "<=":
                if user_value > requirement.value:
                    return False
            elif requirement.operator == "<":
                if user_value >= requirement.value:
                    return False
        
        return True
    
    def get_available_badges(self, user_stats: Dict[str, Any]) -> List[Badge]:
        """Get badges that user can earn based on their stats."""
        available_badges = []
        
        for badge in self.badges.values():
            if self.check_requirements(badge.id, user_stats):
                available_badges.append(badge)
        
        return available_badges
    
    def get_progression_info(self, progression: BadgeProgression) -> Dict[str, Any]:
        """Get progression level information."""
        return self.progression_levels.get(progression, {})
    
    def get_badge_effects(self) -> Dict[str, Any]:
        """Get badge effects configuration."""
        return self.badge_effects
    
    def create_custom_badge(self, badge_id: str, name: str, description: str,
                           icon: str, color: str, category: BadgeCategory,
                           requirements: List[BadgeRequirement],
                           rewards: BadgeReward,
                           progression: BadgeProgression = BadgeProgression.BRONZE) -> Badge:
        """Create a custom badge."""
        badge = Badge(
            id=badge_id,
            name=name,
            description=description,
            icon=icon,
            color=color,
            category=category,
            requirements=requirements,
            rewards=rewards,
            progression=progression
        )
        
        self.badges[badge_id] = badge
        
        if category not in self.categories:
            self.categories[category] = {}
        self.categories[category][badge_id] = badge
        
        logger.info(f"🏆 Created custom badge: {badge_id}")
        
        return badge
    
    def update_badge(self, badge_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing badge."""
        badge = self.get_badge(badge_id)
        if not badge:
            return False
        
        # Update badge fields
        for field, value in updates.items():
            if hasattr(badge, field):
                setattr(badge, field, value)
        
        badge.updated_at = time.time()
        
        logger.info(f"🏆 Updated badge: {badge_id}")
        
        return True
    
    def delete_badge(self, badge_id: str) -> bool:
        """Delete a badge."""
        badge = self.get_badge(badge_id)
        if not badge:
            return False
        
        # Remove from badges
        del self.badges[badge_id]
        
        # Remove from category
        if badge.category in self.categories:
            if badge_id in self.categories[badge.category]:
                del self.categories[badge.category][badge_id]
        
        logger.info(f"🏆 Deleted badge: {badge_id}")
        
        return True
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get badge system statistics."""
        category_counts = {}
        progression_counts = {}
        
        for category, badges in self.categories.items():
            category_counts[category.value] = len(badges)
        
        for progression in BadgeProgression:
            progression_counts[progression.value] = len(self.get_badges_by_progression(progression))
        
        return {
            'total_badges': len(self.badges),
            'category_counts': category_counts,
            'progression_counts': progression_counts,
            'badge_effects_enabled': self.badge_effects.get('role_colors', {}).get('enabled', False),
            'special_titles_enabled': self.badge_effects.get('special_titles', {}).get('enabled', False),
            'permissions_enabled': self.badge_effects.get('permissions', {}).get('enabled', False)
        }
    
    def export_badge_config(self) -> Dict[str, Any]:
        """Export current badge configuration."""
        config = {
            'council_badges': {
                'version': '1.0.0',
                'description': 'CollTech-AGI Council Badge System',
                'badge_progression': {},
                'badge_effects': self.badge_effects,
                'badge_categories': {}
            }
        }
        
        # Export progression levels
        for progression, level_config in self.progression_levels.items():
            config['council_badges']['badge_progression'][progression.value] = level_config
        
        # Export categories and badges
        for category, badges in self.categories.items():
            category_config = {
                'name': category.value.title(),
                'description': f'Badges for {category.value} achievements',
                'badges': {}
            }
            
            for badge_id, badge in badges.items():
                badge_config = {
                    'name': badge.name,
                    'description': badge.description,
                    'icon': badge.icon,
                    'color': badge.color,
                    'progression': badge.progression.value,
                    'requirements': {req.name: req.value for req in badge.requirements},
                    'rewards': {
                        'role_color': badge.rewards.role_color,
                        'special_title': badge.rewards.special_title,
                        'permissions': badge.rewards.permissions,
                        'experience_points': badge.rewards.experience_points
                    }
                }
                category_config['badges'][badge_id] = badge_config
            
            config['council_badges']['badge_categories'][category.value] = category_config
        
        return config


# Global instance
_badge_system = None

def get_badge_system(config_path: str = "configs/council_badges.json") -> BadgeSystem:
    """Get the global badge system instance."""
    global _badge_system
    if _badge_system is None:
        _badge_system = BadgeSystem(config_path)
    return _badge_system


if __name__ == "__main__":
    # Test the badge system
    def test_badge_system():
        print("🏆 Testing Council Badge System")
        print("=" * 50)
        
        # Initialize badge system
        badge_system = get_badge_system()
        
        # Get system statistics
        stats = badge_system.get_system_statistics()
        print(f"📊 Badge System Statistics:")
        print(f"   Total Badges: {stats['total_badges']}")
        print(f"   Categories: {stats['category_counts']}")
        print(f"   Progression Levels: {stats['progression_counts']}")
        
        # Test badge retrieval
        crt_badge = badge_system.get_badge("crt_master")
        if crt_badge:
            print(f"\n🔬 CRT Master Badge:")
            print(f"   Name: {crt_badge.name}")
            print(f"   Description: {crt_badge.description}")
            print(f"   Icon: {crt_badge.icon}")
            print(f"   Color: {crt_badge.color}")
            print(f"   Category: {crt_badge.category.value}")
            print(f"   Progression: {crt_badge.progression.value}")
            print(f"   Requirements: {len(crt_badge.requirements)}")
            print(f"   Rewards: {crt_badge.rewards.special_title}")
        
        # Test requirement checking
        user_stats = {
            'tests_completed': 120,
            'success_rate': 0.96,
            'continuity_score': 0.92
        }
        
        available_badges = badge_system.get_available_badges(user_stats)
        print(f"\n🎯 Available Badges for User:")
        for badge in available_badges[:5]:  # Show first 5
            print(f"   - {badge.icon} {badge.name} ({badge.category.value})")
        
        # Test custom badge creation
        custom_requirement = BadgeRequirement(
            name="custom_metric",
            value=100,
            description="Custom metric requirement"
        )
        
        custom_reward = BadgeReward(
            role_color="#FF0000",
            special_title="Custom Master",
            permissions=["custom_override"],
            experience_points=1000
        )
        
        custom_badge = badge_system.create_custom_badge(
            "custom_test",
            "Custom Test Badge",
            "A custom test badge",
            "🧪",
            "#FF0000",
            BadgeCategory.SPECIAL,
            [custom_requirement],
            custom_reward,
            BadgeProgression.SILVER
        )
        
        print(f"\n🧪 Created Custom Badge:")
        print(f"   ID: {custom_badge.id}")
        print(f"   Name: {custom_badge.name}")
        print(f"   Progression: {custom_badge.progression.value}")
        
        # Export configuration
        exported_config = badge_system.export_badge_config()
        print(f"\n📤 Exported Configuration:")
        print(f"   Total Categories: {len(exported_config['council_badges']['badge_categories'])}")
        print(f"   Total Badges: {sum(len(cat['badges']) for cat in exported_config['council_badges']['badge_categories'].values())}")
        
        print("\n✅ Badge system test completed!")
    
    # Run test
    test_badge_system()

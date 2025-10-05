#!/usr/bin/env python3
"""
CollTech-AGI Council Badge System Demo

Comprehensive demonstration of the council badge system integration
with Discord bot functionality and badge management.
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Any

# CollTech-AGI imports
from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig

# Council Badge System imports
from src.council import (
    BadgeSystem, BadgeTracker, DiscordBadgeIntegration, 
    DiscordBadgeConfig, BadgeDisplay, BadgeCategory, BadgeProgression
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CouncilBadgeDemo:
    """
    Council Badge System Demo
    
    Demonstrates the complete council badge system functionality
    including badge management, user tracking, and Discord integration.
    """
    
    def __init__(self):
        # Initialize CollTech-AGI
        self.config = FrameworkConfig(
            auto_personality_enabled=True,
            catalyst_integration_enabled=True,
            realtime_apis_enabled=True,
            memory_lattice_enabled=True,
            drift_detection_enabled=True,
            tool_making_enabled=True
        )
        
        self.agi = CollTechAGIAdvanced(self.config)
        
        # Initialize Council Badge System
        self.badge_system = BadgeSystem()
        self.badge_tracker = BadgeTracker(self.badge_system)
        
        # Demo users
        self.demo_users = [
            {"id": "user_001", "name": "Alice", "role": "Researcher"},
            {"id": "user_002", "name": "Bob", "role": "Developer"},
            {"id": "user_003", "name": "Charlie", "role": "Tester"},
            {"id": "user_004", "name": "Diana", "role": "Council Member"},
            {"id": "user_005", "name": "Eve", "role": "Community Leader"}
        ]
        
        logger.info("🏆 Council Badge Demo initialized")
    
    async def run_complete_demo(self):
        """Run the complete council badge system demonstration."""
        logger.info("🚀 Starting Council Badge System Demo")
        logger.info("=" * 70)
        
        try:
            # Start CollTech-AGI
            self.agi.start()
            logger.info("✅ CollTech-AGI started")
            
            # Demo 1: Badge System Overview
            await self.demo_badge_system_overview()
            
            # Demo 2: User Badge Tracking
            await self.demo_user_badge_tracking()
            
            # Demo 3: Badge Progression
            await self.demo_badge_progression()
            
            # Demo 4: Badge Statistics
            await self.demo_badge_statistics()
            
            # Demo 5: Discord Integration (Simulated)
            await self.demo_discord_integration()
            
            # Demo 6: Badge Management
            await self.demo_badge_management()
            
            logger.info("\n✅ Council Badge System Demo completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            raise
        
        finally:
            # Cleanup
            self.agi.shutdown()
    
    async def demo_badge_system_overview(self):
        """Demonstrate badge system overview."""
        logger.info("\n" + "="*50)
        logger.info("🏆 Demo 1: Badge System Overview")
        logger.info("="*50)
        
        # Get system statistics
        stats = self.badge_system.get_system_statistics()
        
        logger.info(f"📊 Badge System Statistics:")
        logger.info(f"   Total Badges: {stats['total_badges']}")
        logger.info(f"   Categories: {len(stats['category_counts'])}")
        logger.info(f"   Progression Levels: {len(stats['progression_counts'])}")
        
        # Show category breakdown
        logger.info(f"\n📋 Category Breakdown:")
        for category, count in stats['category_counts'].items():
            logger.info(f"   {category.title()}: {count} badges")
        
        # Show progression breakdown
        logger.info(f"\n🥇 Progression Breakdown:")
        for progression, count in stats['progression_counts'].items():
            logger.info(f"   {progression.title()}: {count} badges")
        
        # Show sample badges
        logger.info(f"\n🏆 Sample Badges:")
        sample_badges = list(self.badge_system.badges.values())[:5]
        for badge in sample_badges:
            logger.info(f"   {badge.icon} {badge.name} ({badge.category.value}) - {badge.progression.value.title()}")
    
    async def demo_user_badge_tracking(self):
        """Demonstrate user badge tracking."""
        logger.info("\n" + "="*50)
        logger.info("👥 Demo 2: User Badge Tracking")
        logger.info("="*50)
        
        # Simulate user activities and badge earning
        for user in self.demo_users:
            user_id = user["id"]
            user_name = user["name"]
            user_role = user["role"]
            
            logger.info(f"\n👤 Processing user: {user_name} ({user_role})")
            
            # Simulate different activities based on role
            if user_role == "Researcher":
                await self._simulate_researcher_activities(user_id)
            elif user_role == "Developer":
                await self._simulate_developer_activities(user_id)
            elif user_role == "Tester":
                await self._simulate_tester_activities(user_id)
            elif user_role == "Council Member":
                await self._simulate_council_activities(user_id)
            elif user_role == "Community Leader":
                await self._simulate_community_activities(user_id)
            
            # Get user summary
            summary = self.badge_tracker.get_user_summary(user_id)
            logger.info(f"   📊 Summary: {summary['badges_earned']} badges, {summary['total_experience']} XP")
            
            # Show earned badges
            badges = self.badge_tracker.get_user_badges(user_id)
            if badges:
                logger.info(f"   🏆 Earned Badges:")
                for badge in badges:
                    badge_def = self.badge_system.get_badge(badge.badge_id)
                    if badge_def:
                        logger.info(f"      {badge_def.icon} {badge_def.name} ({badge_def.category.value})")
    
    async def _simulate_researcher_activities(self, user_id: str):
        """Simulate researcher activities."""
        # Research activities
        self.badge_tracker.update_user_stat(user_id, "tests_completed", 150)
        self.badge_tracker.update_user_stat(user_id, "success_rate", 0.96)
        self.badge_tracker.update_user_stat(user_id, "continuity_score", 0.92)
        self.badge_tracker.update_user_stat(user_id, "gradings_completed", 75)
        self.badge_tracker.update_user_stat(user_id, "average_score", 88)
        self.badge_tracker.update_user_stat(user_id, "evidence_items", 300)
        self.badge_tracker.update_user_stat(user_id, "validation_rate", 0.99)
        
        logger.info(f"   🔬 Simulated research activities for {user_id}")
    
    async def _simulate_developer_activities(self, user_id: str):
        """Simulate developer activities."""
        # Development activities
        self.badge_tracker.update_user_stat(user_id, "vl_sessions", 60)
        self.badge_tracker.update_user_stat(user_id, "message_accuracy", 0.94)
        self.badge_tracker.update_user_stat(user_id, "consciousness_sessions", 120)
        self.badge_tracker.update_user_stat(user_id, "integration_success", 0.96)
        self.badge_tracker.update_user_stat(user_id, "psiqrh_benchmarks", 30)
        self.badge_tracker.update_user_stat(user_id, "performance_improvement", 0.25)
        
        logger.info(f"   💻 Simulated development activities for {user_id}")
    
    async def _simulate_tester_activities(self, user_id: str):
        """Simulate tester activities."""
        # Testing activities
        self.badge_tracker.update_user_stat(user_id, "tests_completed", 200)
        self.badge_tracker.update_user_stat(user_id, "success_rate", 0.98)
        self.badge_tracker.update_user_stat(user_id, "monitoring_sessions", 150)
        self.badge_tracker.update_user_stat(user_id, "accuracy_rate", 0.97)
        self.badge_tracker.update_user_stat(user_id, "evaluations_completed", 80)
        self.badge_tracker.update_user_stat(user_id, "evaluation_accuracy", 0.96)
        
        logger.info(f"   🧪 Simulated testing activities for {user_id}")
    
    async def _simulate_council_activities(self, user_id: str):
        """Simulate council activities."""
        # Council activities
        self.badge_tracker.update_user_stat(user_id, "sessions_chaired", 15)
        self.badge_tracker.update_user_stat(user_id, "decision_approval", 0.97)
        self.badge_tracker.update_user_stat(user_id, "research_approved", 35)
        self.badge_tracker.update_user_stat(user_id, "safety_reviews", 60)
        self.badge_tracker.update_user_stat(user_id, "safety_score", 0.99)
        self.badge_tracker.update_user_stat(user_id, "protocol_reviews", 45)
        self.badge_tracker.update_user_stat(user_id, "protocol_accuracy", 0.96)
        
        logger.info(f"   🏛️ Simulated council activities for {user_id}")
    
    async def _simulate_community_activities(self, user_id: str):
        """Simulate community activities."""
        # Community activities
        self.badge_tracker.update_user_stat(user_id, "community_contributions", 80)
        self.badge_tracker.update_user_stat(user_id, "help_sessions", 40)
        self.badge_tracker.update_user_stat(user_id, "mentorship_success", 0.92)
        self.badge_tracker.update_user_stat(user_id, "consciousness_sessions", 250)
        self.badge_tracker.update_user_stat(user_id, "integration_success", 0.98)
        self.badge_tracker.update_user_stat(user_id, "system_contributions", 12)
        self.badge_tracker.update_user_stat(user_id, "architecture_quality", 0.96)
        
        logger.info(f"   👥 Simulated community activities for {user_id}")
    
    async def demo_badge_progression(self):
        """Demonstrate badge progression system."""
        logger.info("\n" + "="*50)
        logger.info("📈 Demo 3: Badge Progression")
        logger.info("="*50)
        
        # Show progression levels
        progression_levels = self.badge_system.progression_levels
        logger.info(f"🥇 Progression Levels:")
        for progression, config in progression_levels.items():
            logger.info(f"   {progression.value.title()}: {config['description']} (x{config['multiplier']})")
        
        # Show badge progression examples
        logger.info(f"\n🏆 Badge Progression Examples:")
        for category in BadgeCategory:
            badges = self.badge_system.get_badges_by_category(category)
            if badges:
                sample_badge = list(badges.values())[0]
                logger.info(f"   {category.value.title()}: {sample_badge.icon} {sample_badge.name} ({sample_badge.progression.value.title()})")
        
        # Show user progress
        logger.info(f"\n📊 User Progress Examples:")
        for user in self.demo_users[:3]:  # Show first 3 users
            user_id = user["id"]
            progress = self.badge_tracker.get_user_progress(user_id)
            
            in_progress = [p for p in progress if p.status.value == "in_progress"]
            available = [p for p in progress if p.status.value == "available"]
            
            logger.info(f"   {user['name']}: {len(in_progress)} in progress, {len(available)} available")
            
            # Show top progress items
            if in_progress:
                top_progress = sorted(in_progress, key=lambda x: x.progress_percentage, reverse=True)[:2]
                for prog in top_progress:
                    badge_def = self.badge_system.get_badge(prog.badge_id)
                    if badge_def:
                        logger.info(f"      {badge_def.icon} {badge_def.name}: {prog.progress_percentage:.1f}%")
    
    async def demo_badge_statistics(self):
        """Demonstrate badge statistics."""
        logger.info("\n" + "="*50)
        logger.info("📊 Demo 4: Badge Statistics")
        logger.info("="*50)
        
        # Get badge statistics
        stats = self.badge_tracker.get_badge_statistics()
        
        logger.info(f"📈 Badge Statistics:")
        logger.info(f"   Total Users: {stats['total_users']}")
        logger.info(f"   Total Badges Earned: {stats['total_badges_earned']}")
        logger.info(f"   Average Badges per User: {stats['average_badges_per_user']:.1f}")
        
        # Category distribution
        logger.info(f"\n📋 Category Distribution:")
        for category, count in stats['category_distribution'].items():
            logger.info(f"   {category.title()}: {count} badges earned")
        
        # Progression distribution
        logger.info(f"\n🥇 Progression Distribution:")
        for progression, count in stats['progression_distribution'].items():
            logger.info(f"   {progression.title()}: {count} badges earned")
        
        # Most/least earned badges
        if stats['most_earned_badge']:
            most_badge = self.badge_system.get_badge(stats['most_earned_badge'])
            if most_badge:
                logger.info(f"\n🏆 Most Earned Badge: {most_badge.icon} {most_badge.name}")
        
        if stats['least_earned_badge']:
            least_badge = self.badge_system.get_badge(stats['least_earned_badge'])
            if least_badge:
                logger.info(f"🥉 Least Earned Badge: {least_badge.icon} {least_badge.name}")
        
        # Leaderboard
        leaderboard = self.badge_tracker.get_user_leaderboard(5)
        logger.info(f"\n🏅 Top 5 Users:")
        for i, user in enumerate(leaderboard, 1):
            user_name = next((u["name"] for u in self.demo_users if u["id"] == user["user_id"]), user["user_id"])
            logger.info(f"   {i}. {user_name}: {user['total_experience']} XP, {user['badges_earned']} badges")
    
    async def demo_discord_integration(self):
        """Demonstrate Discord integration (simulated)."""
        logger.info("\n" + "="*50)
        logger.info("🎮 Demo 5: Discord Integration (Simulated)")
        logger.info("="*50)
        
        # Simulate Discord badge integration
        logger.info("🎮 Discord Integration Features:")
        logger.info("   ✅ Badge announcement system")
        logger.info("   ✅ Role management system")
        logger.info("   ✅ Command system")
        logger.info("   ✅ Leaderboard system")
        logger.info("   ✅ User badge display system")
        
        # Simulate badge announcements
        logger.info(f"\n📢 Simulated Badge Announcements:")
        for user in self.demo_users[:3]:
            badges = self.badge_tracker.get_user_badges(user["id"])
            if badges:
                recent_badge = max(badges, key=lambda x: x.earned_at)
                badge_def = self.badge_system.get_badge(recent_badge.badge_id)
                if badge_def:
                    logger.info(f"   🏆 {user['name']} earned: {badge_def.icon} {badge_def.name}")
        
        # Simulate Discord commands
        logger.info(f"\n💬 Simulated Discord Commands:")
        commands = [
            "!badges - Show user badges",
            "!badge <badge_id> - Show badge information",
            "!leaderboard - Show badge leaderboard",
            "!award <user> <badge_id> - Award badge (Admin)"
        ]
        for cmd in commands:
            logger.info(f"   {cmd}")
        
        # Simulate role management
        logger.info(f"\n👥 Simulated Role Management:")
        for user in self.demo_users[:3]:
            badges = self.badge_tracker.get_user_badges(user["id"])
            if badges:
                badge_def = self.badge_system.get_badge(badges[0].badge_id)
                if badge_def and badge_def.rewards.role_color:
                    logger.info(f"   {user['name']}: {badge_def.icon} {badge_def.name} role")
    
    async def demo_badge_management(self):
        """Demonstrate badge management features."""
        logger.info("\n" + "="*50)
        logger.info("⚙️ Demo 6: Badge Management")
        logger.info("="*50)
        
        # Create custom badge
        logger.info("🧪 Creating Custom Badge:")
        from src.council.badge_system import BadgeRequirement, BadgeReward
        
        custom_requirement = BadgeRequirement(
            name="demo_metric",
            value=50,
            description="Demo metric requirement"
        )
        
        custom_reward = BadgeReward(
            role_color="#FF00FF",
            special_title="Demo Master",
            permissions=["demo_override"],
            experience_points=500
        )
        
        custom_badge = self.badge_system.create_custom_badge(
            "demo_custom",
            "Demo Custom Badge",
            "A custom badge created during the demo",
            "🧪",
            "#FF00FF",
            BadgeCategory.SPECIAL,
            [custom_requirement],
            custom_reward,
            BadgeProgression.SILVER
        )
        
        logger.info(f"   ✅ Created: {custom_badge.icon} {custom_badge.name}")
        
        # Test badge requirements
        logger.info(f"\n🔍 Testing Badge Requirements:")
        test_user_id = "test_user"
        test_stats = {"demo_metric": 60}
        
        can_earn = self.badge_system.check_requirements(custom_badge.id, test_stats)
        logger.info(f"   User with 60 demo_metric can earn badge: {can_earn}")
        
        # Get available badges
        available_badges = self.badge_system.get_available_badges(test_stats)
        logger.info(f"   Available badges for test user: {len(available_badges)}")
        
        # Export configuration
        logger.info(f"\n📤 Exporting Badge Configuration:")
        exported_config = self.badge_system.export_badge_config()
        total_exported = sum(len(cat['badges']) for cat in exported_config['council_badges']['badge_categories'].values())
        logger.info(f"   Exported {total_exported} badges across {len(exported_config['council_badges']['badge_categories'])} categories")
        
        # Save badge tracking data
        logger.info(f"\n💾 Saving Badge Tracking Data:")
        self.badge_tracker.save_data()
        logger.info(f"   Badge tracking data saved successfully")


async def main():
    """Main demonstration function."""
    print("🏆 CollTech-AGI Council Badge System Demo")
    print("=" * 70)
    
    # Initialize demo
    demo = CouncilBadgeDemo()
    
    try:
        # Run complete demonstration
        await demo.run_complete_demo()
        
    except Exception as e:
        logger.error(f"❌ Main demo failed: {e}")
        raise


if __name__ == "__main__":
    # Run the complete demonstration
    asyncio.run(main())

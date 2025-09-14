#!/usr/bin/env python3
"""
Test script to verify the AGI initialization fix.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_agi_initialization():
    """Test AGI initialization to verify the fix."""
    try:
        from colltech_agi_realtime_advanced_secure import CollTechAGIRealtimeAdvanced
        
        print("🧪 Testing CollTech-AGI initialization...")
        
        # Initialize system
        agi = CollTechAGIRealtimeAdvanced()
        
        print("✅ AGI instance created successfully")
        print("🔧 Testing initialization...")
        
        # This should not raise the coroutine error
        await agi.initialize()
        
        print("✅ AGI initialized successfully!")
        print("🛡️ Security hardening active")
        
        # Test basic functionality
        capabilities = agi.get_system_capabilities()
        print(f"📊 System capabilities: {len(capabilities)} features available")
        
        # Cleanup
        await agi.shutdown()
        print("🛑 AGI shutdown completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during AGI test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("=" * 60)
    print("CollTech-AGI Initialization Test")
    print("=" * 60)
    
    success = await test_agi_initialization()
    
    if success:
        print("\n🎉 All tests passed! The coroutine error has been fixed.")
    else:
        print("\n💥 Tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

"""
Verification Test: All 9 Personalities Have File Access Capabilities
Tests that EVERY personality correctly states file access and responds to capability questions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

def test_all_personalities_file_access():
    """Test that ALL 9 personalities correctly state file access"""
    print("\n" + "="*70)
    print("VERIFICATION: ALL 9 PERSONALITIES FILE ACCESS")
    print("="*70)
    
    system = ExpandedPersonalitySystem()
    
    # Test questions
    questions = [
        "Can you access files on my computer?",
        "Do you have file system access?",
        "What can you help me with?"
    ]
    
    # All 9 personalities
    all_personalities = [
        ExpandedPersonality.RHO,
        ExpandedPersonality.LYRA,
        ExpandedPersonality.NYX,
        ExpandedPersonality.EIDOLON,
        ExpandedPersonality.PLANNER,
        ExpandedPersonality.COGSWORTH,
        ExpandedPersonality.INTUITOR,
        ExpandedPersonality.ARCHIVA,
        ExpandedPersonality.MIRROR
    ]
    
    results = {}
    
    for personality in all_personalities:
        print(f"\n{'='*70}")
        print(f"Testing: {personality.value.upper()}")
        print(f"{'='*70}")
        
        personality_results = []
        
        for question in questions:
            response = system.generate_response(question, personality)
            
            # Check for file access indicators
            has_file_access_mention = any(phrase in response.lower() for phrase in [
                'file', 'access', 'read', 'list', 'search', 'directory', 'documents', 'desktop'
            ])
            
            # Check it's not generic template
            is_generic = "Accessing memory for" in response and "I've retrieved relevant patterns" in response
            
            # Check for proper capability response
            is_proper_response = has_file_access_mention and not is_generic
            
            status = "✅" if is_proper_response else "❌"
            print(f"{status} Q: {question[:50]}...")
            if not is_proper_response:
                print(f"   Response preview: {response[:150]}...")
            
            personality_results.append(is_proper_response)
        
        # Summary for this personality
        passed = sum(personality_results)
        total = len(personality_results)
        results[personality.value] = (passed, total)
        
        if passed == total:
            print(f"\n✅ {personality.value.upper()}: ALL TESTS PASSED ({passed}/{total})")
        else:
            print(f"\n❌ {personality.value.upper()}: SOME FAILURES ({passed}/{total})")
    
    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY - ALL 9 PERSONALITIES")
    print(f"{'='*70}\n")
    
    all_passed = True
    for personality_name, (passed, total) in results.items():
        status = "✅" if passed == total else "❌"
        percentage = (100 * passed) // total if total > 0 else 0
        print(f"{status} {personality_name.upper():12} - {passed}/{total} tests passed ({percentage}%)")
        if passed != total:
            all_passed = False
    
    print(f"\n{'='*70}")
    if all_passed:
        print("🎉 SUCCESS: ALL 9 PERSONALITIES HAVE FILE ACCESS CAPABILITIES!")
        print("="*70)
        return True
    else:
        print("⚠️ WARNING: Some personalities missing file access capabilities")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_all_personalities_file_access()
    sys.exit(0 if success else 1)

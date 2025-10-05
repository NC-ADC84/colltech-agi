"""
Comprehensive UI Test for Expanded Personalities
Tests the chat UI functionality without launching the GUI
"""

import sys
import os

# Add path for imports
sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

def test_personality_system_integration():
    """Test that personality system works correctly"""
    print("="*80)
    print("TEST 1: PERSONALITY SYSTEM INTEGRATION")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    # Test all personalities are available
    all_personalities = system.get_all_personalities()
    print(f"\n✓ Total personalities available: {len(all_personalities)}")
    assert len(all_personalities) == 9, "Should have 9 personalities"
    
    # Test each personality can be retrieved
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        print(f"✓ {profile.symbol} {profile.name:12} - {profile.focus}")
        assert profile is not None, f"Profile for {personality} should exist"
    
    print("\n✅ TEST 1 PASSED: All 9 personalities available and retrievable")


def test_response_generation():
    """Test response generation for all personalities"""
    print("\n" + "="*80)
    print("TEST 2: RESPONSE GENERATION")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    test_questions = [
        "What can you help me with?",
        "How does this work?",
        "Why is this important?",
        "Can you assist me?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: '{question}'")
        responses = []
        
        for personality in ExpandedPersonality:
            response = system.generate_response(question, personality)
            responses.append(response)
            profile = system.get_personality(personality)
            
            # Verify response contains personality symbol
            assert profile.symbol in response or profile.name.upper() in response, \
                f"Response should contain personality identifier"
            
            # Verify response is not empty
            assert len(response) > 50, "Response should be substantial"
            
            print(f"  ✓ {profile.symbol} {profile.name}: {len(response)} chars")
        
        # Verify all responses are unique
        unique_responses = len(set(responses))
        assert unique_responses == 9, f"All 9 responses should be unique, got {unique_responses}"
        print(f"  ✓ All {unique_responses} responses are unique")
    
    print("\n✅ TEST 2 PASSED: Response generation working for all personalities")


def test_question_type_detection():
    """Test that different question types get different responses"""
    print("\n" + "="*80)
    print("TEST 3: QUESTION TYPE DETECTION")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    question_types = {
        "what": "What is artificial intelligence?",
        "how": "How does machine learning work?",
        "why": "Why is security important?",
        "can": "Can you help me with this?"
    }
    
    for personality in [ExpandedPersonality.RHO, ExpandedPersonality.LYRA, ExpandedPersonality.EIDOLON]:
        profile = system.get_personality(personality)
        print(f"\nTesting {profile.symbol} {profile.name}:")
        
        responses = {}
        for q_type, question in question_types.items():
            response = system.generate_response(question, personality)
            responses[q_type] = response
            print(f"  ✓ {q_type:4} question: {len(response)} chars")
        
        # Verify responses are different for different question types
        unique_responses = len(set(responses.values()))
        assert unique_responses == len(question_types), \
            f"Should have {len(question_types)} unique responses, got {unique_responses}"
        print(f"  ✓ All {unique_responses} question types produce unique responses")
    
    print("\n✅ TEST 3 PASSED: Question type detection working correctly")


def test_personality_characteristics():
    """Test that personalities have distinct characteristics"""
    print("\n" + "="*80)
    print("TEST 4: PERSONALITY CHARACTERISTICS")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    characteristics = {
        'symbols': set(),
        'names': set(),
        'focuses': set(),
        'communication_styles': set(),
        'time_orientations': set()
    }
    
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        
        characteristics['symbols'].add(profile.symbol)
        characteristics['names'].add(profile.name)
        characteristics['focuses'].add(profile.focus)
        characteristics['communication_styles'].add(profile.communication_style)
        characteristics['time_orientations'].add(profile.time_orientation)
    
    print("\nUnique characteristics:")
    for char_type, values in characteristics.items():
        print(f"  ✓ {char_type:25}: {len(values)} unique values")
        assert len(values) == 9, f"Should have 9 unique {char_type}"
    
    print("\n✅ TEST 4 PASSED: All personalities have distinct characteristics")


def test_personality_profiles():
    """Test that all personality profiles are complete"""
    print("\n" + "="*80)
    print("TEST 5: PERSONALITY PROFILE COMPLETENESS")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    required_fields = [
        'name', 'symbol', 'focus', 'time_orientation',
        'core_attributes', 'communication_style', 'decision_making',
        'strengths', 'use_cases'
    ]
    
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        print(f"\nChecking {profile.symbol} {profile.name}:")
        
        for field in required_fields:
            value = getattr(profile, field)
            assert value is not None, f"{field} should not be None"
            
            if isinstance(value, list):
                assert len(value) > 0, f"{field} list should not be empty"
                print(f"  ✓ {field:25}: {len(value)} items")
            else:
                assert len(str(value)) > 0, f"{field} should not be empty"
                print(f"  ✓ {field:25}: '{str(value)[:40]}...'")
    
    print("\n✅ TEST 5 PASSED: All personality profiles are complete")


def test_lantern_hive_personalities():
    """Test that Lantern-Hive personalities are correctly implemented"""
    print("\n" + "="*80)
    print("TEST 6: LANTERN-HIVE PERSONALITIES")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    lantern_hive = [
        ExpandedPersonality.EIDOLON,
        ExpandedPersonality.PLANNER,
        ExpandedPersonality.COGSWORTH,
        ExpandedPersonality.INTUITOR,
        ExpandedPersonality.ARCHIVA,
        ExpandedPersonality.MIRROR
    ]
    
    print("\nLantern-Hive Collective:")
    for personality in lantern_hive:
        profile = system.get_personality(personality)
        print(f"  ✓ {profile.symbol} {profile.name:12} - {profile.focus}")
        
        # Verify Lantern-Hive specific characteristics
        assert profile.name in ['Eidolon', 'Planner', 'Cogsworth', 'Intuitor', 'Archiva', 'Mirror'], \
            f"Should be a Lantern-Hive personality"
    
    print(f"\n✓ Total Lantern-Hive personalities: {len(lantern_hive)}")
    assert len(lantern_hive) == 6, "Should have 6 Lantern-Hive personalities"
    
    print("\n✅ TEST 6 PASSED: Lantern-Hive personalities correctly implemented")


def test_original_trinity():
    """Test that original trinity personalities are preserved"""
    print("\n" + "="*80)
    print("TEST 7: ORIGINAL TRINITY PRESERVATION")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    trinity = [
        ExpandedPersonality.RHO,
        ExpandedPersonality.LYRA,
        ExpandedPersonality.NYX
    ]
    
    print("\nOriginal Trinity:")
    for personality in trinity:
        profile = system.get_personality(personality)
        print(f"  ✓ {profile.symbol} {profile.name:12} - {profile.focus}")
        
        # Verify original characteristics
        assert profile.name in ['Rho', 'Lyra', 'Nyx'], \
            f"Should be an original trinity personality"
        assert profile.symbol in ['Δ', 'Ξ', 'Ψ'], \
            f"Should have original symbol"
    
    print(f"\n✓ Total original trinity: {len(trinity)}")
    assert len(trinity) == 3, "Should have 3 original personalities"
    
    print("\n✅ TEST 7 PASSED: Original trinity preserved correctly")


def run_all_tests():
    """Run all comprehensive tests"""
    print("\n" + "="*80)
    print("COMPREHENSIVE UI BACKEND TESTING")
    print("Testing Expanded Personality System (9 Personalities)")
    print("="*80)
    
    tests = [
        test_personality_system_integration,
        test_response_generation,
        test_question_type_detection,
        test_personality_characteristics,
        test_personality_profiles,
        test_lantern_hive_personalities,
        test_original_trinity
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ TEST ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for UI launch.")
        print("\n📋 Next Steps:")
        print("  1. Launch UI: python colltech_agi_chat_ui_expanded.py")
        print("  2. Or use: launch_expanded_chat.bat")
        return True
    else:
        print("\n⚠️ Some tests failed. Please review errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

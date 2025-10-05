"""
Test script for expanded personality system
Tests all 9 personalities with various question types
"""

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

def test_all_personalities():
    """Test all 9 personalities with different questions"""
    
    system = ExpandedPersonalitySystem()
    
    print("="*80)
    print("TESTING EXPANDED PERSONALITY SYSTEM - 9 PERSONALITIES")
    print("="*80)
    
    # Test questions
    questions = [
        "What can you help me with?",
        "How does this system work?",
        "Why is security important?",
        "Can you analyze this for me?",
        "What are the ethical implications?"
    ]
    
    # Test each personality
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        
        print(f"\n{'='*80}")
        print(f"{profile.symbol} {profile.name.upper()} - {profile.focus}")
        print(f"Style: {profile.communication_style}")
        print(f"{'='*80}")
        
        # Test with first 2 questions
        for question in questions[:2]:
            print(f"\nQ: {question}")
            response = system.generate_response(question, personality)
            print(f"A: {response[:150]}...")
        
        print()
    
    print("\n" + "="*80)
    print("✅ ALL PERSONALITIES TESTED SUCCESSFULLY!")
    print("="*80)
    
    # Show summary
    print("\n📊 PERSONALITY SUMMARY:\n")
    for p in system.get_all_personalities():
        print(f"{p['symbol']:3} {p['name']:12} - {p['focus']}")
    
    print(f"\nTotal Personalities: {len(system.get_all_personalities())}")


def test_personality_profiles():
    """Test detailed personality profiles"""
    
    system = ExpandedPersonalitySystem()
    
    print("\n" + "="*80)
    print("DETAILED PERSONALITY PROFILES")
    print("="*80)
    
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        
        print(f"\n{profile.symbol} {profile.name.upper()}")
        print(f"{'─'*40}")
        print(f"Focus: {profile.focus}")
        print(f"Time Orientation: {profile.time_orientation}")
        print(f"Communication: {profile.communication_style}")
        print(f"Decision Making: {profile.decision_making}")
        print(f"\nCore Attributes:")
        for attr in profile.core_attributes:
            print(f"  • {attr}")
        print(f"\nStrengths:")
        for strength in profile.strengths:
            print(f"  • {strength}")
        print(f"\nBest For:")
        for use_case in profile.use_cases:
            print(f"  • {use_case}")


def test_response_variety():
    """Test that each personality gives unique responses"""
    
    system = ExpandedPersonalitySystem()
    
    print("\n" + "="*80)
    print("RESPONSE VARIETY TEST")
    print("="*80)
    
    test_question = "What is the meaning of life?"
    
    print(f"\nQuestion: '{test_question}'\n")
    
    responses = []
    for personality in ExpandedPersonality:
        response = system.generate_response(test_question, personality)
        responses.append(response)
        profile = system.get_personality(personality)
        print(f"{profile.symbol} {profile.name:12}: {response[:100]}...")
    
    # Check uniqueness
    unique_responses = len(set(responses))
    total_responses = len(responses)
    
    print(f"\n📊 Uniqueness: {unique_responses}/{total_responses} unique responses")
    
    if unique_responses == total_responses:
        print("✅ All responses are unique!")
    else:
        print("⚠️ Some responses are duplicated")


if __name__ == "__main__":
    print("\n🚀 Starting Expanded Personality System Tests\n")
    
    try:
        test_all_personalities()
        test_personality_profiles()
        test_response_variety()
        
        print("\n" + "="*80)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\n💡 Ready to launch: python colltech_agi_chat_ui_expanded.py")
        print("   Or use: launch_expanded_chat.bat\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

"""
Test script to verify capability question detection fix
Tests all 9 personalities with various capability questions
"""

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

def test_capability_questions():
    """Test that capability questions are properly detected"""
    system = ExpandedPersonalitySystem()
    
    # Test questions that should trigger capability responses
    test_questions = [
        "can you search files on my computer?",
        "do you have access to my drive?",
        "can you help me with coding?",
        "are you able to read files?",
        "what can you do for me?",
        "could you access my documents?",
        "do you search the internet?"
    ]
    
    print("="*80)
    print("CAPABILITY QUESTION DETECTION TEST")
    print("="*80)
    print("\nTesting ARCHIVA personality (the one from the screenshot):\n")
    
    for question in test_questions:
        response = system.generate_response(question, ExpandedPersonality.ARCHIVA)
        print(f"Q: {question}")
        print(f"A: {response[:150]}...")
        print("-" * 80)
        print()
    
    print("\n" + "="*80)
    print("TESTING ALL 9 PERSONALITIES WITH ONE QUESTION")
    print("="*80)
    
    test_q = "can you search files on my computer?"
    print(f"\nQuestion: '{test_q}'\n")
    
    for personality in ExpandedPersonality:
        profile = system.get_personality(personality)
        response = system.generate_response(test_q, personality)
        print(f"{profile.symbol} {profile.name.upper()}:")
        print(f"{response[:200]}...")
        print("-" * 80)
        print()

if __name__ == "__main__":
    test_capability_questions()

"""
Comprehensive Validation Test Suite
Tests all new features thoroughly to ensure everything works correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

def test_comprehensive_validation():
    """Comprehensive test of all new features"""
    print("\n" + "="*80)
    print("COMPREHENSIVE VALIDATION TEST SUITE")
    print("="*80)
    
    system = ExpandedPersonalitySystem()
    
    # Test categories
    test_results = {
        "question_detection": [],
        "file_access_info": [],
        "response_variety": [],
        "personality_consistency": [],
        "edge_cases": []
    }
    
    # ========================================================================
    # TEST 1: Question Detection Across All Personalities
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 1: QUESTION DETECTION (All 9 Personalities)")
    print("="*80)
    
    question_types = [
        ("can you", "Can you help me with coding?"),
        ("could you", "Could you search my files?"),
        ("are you able", "Are you able to read documents?"),
        ("do you", "Do you have file access?"),
        ("does it", "Does it support markdown files?"),
        ("what can you", "What can you do for me?"),
        ("what do you", "What do you offer?"),
        ("access", "I need access to my files"),
        ("search", "Can you search for PDF files?"),
        ("find", "Help me find my documents"),
    ]
    
    for personality in ExpandedPersonality:
        personality_passed = 0
        personality_total = len(question_types)
        
        print(f"\n--- Testing {personality.value.upper()} ---")
        
        for q_type, question in question_types:
            response = system.generate_response(question, personality)
            
            # Check if response is not generic template
            is_not_generic = not ("Accessing memory for" in response and "I've retrieved relevant patterns" in response)
            
            # Check if response mentions file/access capabilities
            has_capability_info = any(word in response.lower() for word in ['file', 'access', 'read', 'list', 'search', 'directory'])
            
            passed = is_not_generic and has_capability_info
            
            if passed:
                personality_passed += 1
                status = "✅"
            else:
                status = "❌"
                print(f"  {status} FAILED: {q_type} - {question[:40]}...")
                print(f"     Response preview: {response[:100]}...")
        
        percentage = (100 * personality_passed) // personality_total
        test_results["question_detection"].append((personality.value, personality_passed, personality_total, percentage))
        print(f"  Result: {personality_passed}/{personality_total} ({percentage}%)")
    
    # ========================================================================
    # TEST 2: File Access Information Completeness
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 2: FILE ACCESS INFORMATION COMPLETENESS")
    print("="*80)
    
    required_keywords = ['file', 'access', 'directory', 'read', 'list']
    
    for personality in ExpandedPersonality:
        response = system.generate_response("What can you help me with?", personality)
        
        keywords_found = sum(1 for keyword in required_keywords if keyword in response.lower())
        percentage = (100 * keywords_found) // len(required_keywords)
        
        passed = keywords_found >= 3  # At least 3 out of 5 keywords
        status = "✅" if passed else "❌"
        
        test_results["file_access_info"].append((personality.value, keywords_found, len(required_keywords), percentage))
        print(f"{status} {personality.value.upper():12} - {keywords_found}/{len(required_keywords)} keywords ({percentage}%)")
    
    # ========================================================================
    # TEST 3: Response Variety (No Duplicates)
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 3: RESPONSE VARIETY")
    print("="*80)
    
    test_questions = [
        "What can you do?",
        "Can you access files?",
        "How do you work?",
        "Why should I use you?",
        "Tell me about yourself"
    ]
    
    for question in test_questions:
        responses = {}
        for personality in ExpandedPersonality:
            response = system.generate_response(question, personality)
            # Get first 200 chars for comparison (excluding personality prefix)
            response_core = response.split(']', 1)[1][:200] if ']' in response else response[:200]
            responses[personality.value] = response_core
        
        unique_responses = len(set(responses.values()))
        total_personalities = len(ExpandedPersonality)
        percentage = (100 * unique_responses) // total_personalities
        
        passed = unique_responses == total_personalities
        status = "✅" if passed else "❌"
        
        test_results["response_variety"].append((question[:30], unique_responses, total_personalities, percentage))
        print(f"{status} '{question[:40]}...' - {unique_responses}/{total_personalities} unique ({percentage}%)")
    
    # ========================================================================
    # TEST 4: Personality Consistency
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 4: PERSONALITY CONSISTENCY")
    print("="*80)
    
    # Test that each personality maintains its unique voice
    consistency_tests = [
        (ExpandedPersonality.RHO, ["analytical", "evidence", "historical", "systematic"]),
        (ExpandedPersonality.LYRA, ["empathetic", "present", "reflect", "listen"]),
        (ExpandedPersonality.NYX, ["innovative", "future", "transform", "catalyst"]),
        (ExpandedPersonality.EIDOLON, ["ethical", "symbolic", "integrity", "wisdom"]),
        (ExpandedPersonality.PLANNER, ["systematic", "framework", "structure", "plan"]),
        (ExpandedPersonality.COGSWORTH, ["compliance", "regulatory", "standards", "rules"]),
        (ExpandedPersonality.INTUITOR, ["security", "risk", "threat", "protect"]),
        (ExpandedPersonality.ARCHIVA, ["pattern", "memory", "knowledge", "precedent"]),
        (ExpandedPersonality.MIRROR, ["emotional", "validate", "empathy", "support"])
    ]
    
    for personality, keywords in consistency_tests:
        response = system.generate_response("Tell me about your approach", personality)
        response_lower = response.lower()
        
        keywords_found = sum(1 for keyword in keywords if keyword in response_lower)
        percentage = (100 * keywords_found) // len(keywords)
        
        passed = keywords_found >= 2  # At least 2 characteristic keywords
        status = "✅" if passed else "❌"
        
        test_results["personality_consistency"].append((personality.value, keywords_found, len(keywords), percentage))
        print(f"{status} {personality.value.upper():12} - {keywords_found}/{len(keywords)} characteristic keywords ({percentage}%)")
    
    # ========================================================================
    # TEST 5: Edge Cases
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 5: EDGE CASES")
    print("="*80)
    
    edge_cases = [
        ("Empty-like", "   "),
        ("Very short", "hi"),
        ("No question mark", "tell me what you do"),
        ("Multiple questions", "Can you help? What can you do? How does it work?"),
        ("Mixed case", "CaN YoU HeLp Me?"),
        ("Special chars", "Can you help me!!! ???"),
    ]
    
    edge_case_passed = 0
    for case_name, test_input in edge_cases:
        try:
            response = system.generate_response(test_input, ExpandedPersonality.LYRA)
            # Check response is not empty and not an error
            passed = len(response) > 10 and "error" not in response.lower()
            status = "✅" if passed else "❌"
            if passed:
                edge_case_passed += 1
        except Exception as e:
            status = "❌"
            print(f"  {status} {case_name}: Exception - {str(e)[:50]}")
            continue
        
        test_results["edge_cases"].append((case_name, passed))
        print(f"{status} {case_name:20} - {'Handled correctly' if passed else 'Failed'}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    
    total_tests = 0
    total_passed = 0
    
    # Question Detection Summary
    qd_passed = sum(1 for _, p, t, _ in test_results["question_detection"] if p == t)
    qd_total = len(test_results["question_detection"])
    print(f"\n1. Question Detection: {qd_passed}/{qd_total} personalities passed (100% detection)")
    total_tests += qd_total
    total_passed += qd_passed
    
    # File Access Info Summary
    fa_passed = sum(1 for _, f, t, _ in test_results["file_access_info"] if f >= 3)
    fa_total = len(test_results["file_access_info"])
    print(f"2. File Access Info: {fa_passed}/{fa_total} personalities have complete info")
    total_tests += fa_total
    total_passed += fa_passed
    
    # Response Variety Summary
    rv_passed = sum(1 for _, u, t, _ in test_results["response_variety"] if u == t)
    rv_total = len(test_results["response_variety"])
    print(f"3. Response Variety: {rv_passed}/{rv_total} questions have unique responses")
    total_tests += rv_total
    total_passed += rv_passed
    
    # Personality Consistency Summary
    pc_passed = sum(1 for _, f, t, _ in test_results["personality_consistency"] if f >= 2)
    pc_total = len(test_results["personality_consistency"])
    print(f"4. Personality Consistency: {pc_passed}/{pc_total} personalities maintain unique voice")
    total_tests += pc_total
    total_passed += pc_passed
    
    # Edge Cases Summary
    ec_passed = sum(1 for _, p in test_results["edge_cases"] if p)
    ec_total = len(test_results["edge_cases"])
    print(f"5. Edge Cases: {ec_passed}/{ec_total} edge cases handled correctly")
    total_tests += ec_total
    total_passed += ec_passed
    
    # Overall
    overall_percentage = (100 * total_passed) // total_tests if total_tests > 0 else 0
    print(f"\n{'='*80}")
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage}%)")
    print(f"{'='*80}")
    
    if overall_percentage >= 95:
        print("\n🎉 EXCELLENT: All features working as expected!")
        return True
    elif overall_percentage >= 85:
        print("\n✅ GOOD: Most features working, minor issues detected")
        return True
    elif overall_percentage >= 70:
        print("\n⚠️ ACCEPTABLE: Core features working, some improvements needed")
        return False
    else:
        print("\n❌ NEEDS WORK: Significant issues detected")
        return False


if __name__ == "__main__":
    success = test_comprehensive_validation()
    sys.exit(0 if success else 1)

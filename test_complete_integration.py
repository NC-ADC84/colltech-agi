"""
Complete Integration Test Suite
Tests all aspects of the bug fix including UI, backend, and personality integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality
from colltech_agi_enhanced_backend import EnhancedBackend

def test_personality_question_detection():
    """Test that all personalities properly detect capability questions"""
    print("\n" + "="*70)
    print("TEST 1: PERSONALITY QUESTION DETECTION")
    print("="*70)
    
    system = ExpandedPersonalitySystem()
    
    test_questions = [
        "Can you search files on my computer?",
        "Do you have access to my drive?",
        "What can you help me with?",
        "Are you able to read files?",
        "Could you find files for me?"
    ]
    
    personalities_to_test = [
        ExpandedPersonality.ARCHIVA,
        ExpandedPersonality.RHO,
        ExpandedPersonality.LYRA
    ]
    
    results = []
    for personality in personalities_to_test:
        print(f"\n--- Testing {personality.value.upper()} ---")
        for question in test_questions:
            response = system.generate_response(question, personality)
            
            # Check if response is NOT the generic template
            is_generic = "Accessing memory for" in response and "I've retrieved relevant patterns" in response
            is_capability_response = any(keyword in response.lower() for keyword in [
                'can help', 'i can', 'capabilities', 'file system access', 'pattern recognition'
            ])
            
            if is_capability_response and not is_generic:
                print(f"✅ {question[:40]}... → Proper response")
                results.append(True)
            else:
                print(f"❌ {question[:40]}... → Generic/improper response")
                results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} passed ({100*passed//total}%)")
    return passed == total


def test_backend_file_operations():
    """Test backend file operations"""
    print("\n" + "="*70)
    print("TEST 2: BACKEND FILE OPERATIONS")
    print("="*70)
    
    backend = EnhancedBackend({
        "llm_provider": "local",
        "search_provider": "duckduckgo"
    })
    
    test_dir = os.path.dirname(__file__)
    
    tests = [
        {
            "name": "List directory",
            "command": f"/list {test_dir}",
            "expected_type": "directory_list",
            "check": lambda r: r.get('result', {}).get('success', False)
        },
        {
            "name": "Read README",
            "command": f"/read {os.path.join(test_dir, 'README.md')}",
            "expected_type": "file_read",
            "check": lambda r: r.get('result', {}).get('success', False)
        },
        {
            "name": "Invalid path error",
            "command": "/list /nonexistent/path/12345",
            "expected_type": "directory_list",
            "check": lambda r: not r.get('result', {}).get('success', True)
        }
    ]
    
    results = []
    for test in tests:
        print(f"\n--- {test['name']} ---")
        print(f"Command: {test['command']}")
        
        try:
            result = backend.process_message(test['command'], personality='archiva')
            
            if result.get('type') == test['expected_type'] and test['check'](result):
                print(f"✅ PASS")
                results.append(True)
            else:
                print(f"❌ FAIL - Unexpected result: {result.get('type')}")
                results.append(False)
        except Exception as e:
            print(f"❌ FAIL - Exception: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} passed ({100*passed//total}%)")
    return passed == total


def test_ui_command_detection():
    """Test UI command detection logic"""
    print("\n" + "="*70)
    print("TEST 3: UI COMMAND DETECTION")
    print("="*70)
    
    test_inputs = [
        ("Search C:\\path for md files", True, "Natural language search"),
        ("list files in C:\\path", True, "Natural language list"),
        ("/list C:\\path", True, "Direct command"),
        ("/read C:\\path\\file.txt", True, "Direct read command"),
        ("What is the weather?", False, "Regular chat question"),
        ("Tell me about Python", False, "Regular chat question"),
        ("find files in documents", True, "Natural language find"),
        ("show me files", True, "Natural language show")
    ]
    
    results = []
    for user_input, should_detect, description in test_inputs:
        user_input_lower = user_input.lower()
        is_file_command = any(keyword in user_input_lower for keyword in [
            '/read', '/list', '/search', 'search', 'search for', 'find', 'find files', 'list files',
            'read file', 'show me files', 'look for'
        ])
        
        if is_file_command == should_detect:
            print(f"✅ {description}: Correctly {'detected' if should_detect else 'ignored'}")
            results.append(True)
        else:
            print(f"❌ {description}: {'Missed' if should_detect else 'False positive'}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} passed ({100*passed//total}%)")
    return passed == total


def test_archiva_file_access_response():
    """Test ARCHIVA specifically states it HAS file access"""
    print("\n" + "="*70)
    print("TEST 4: ARCHIVA FILE ACCESS RESPONSE")
    print("="*70)
    
    system = ExpandedPersonalitySystem()
    
    questions = [
        "Can you access files on my computer?",
        "Do you have file system access?",
        "Can you search my files?"
    ]
    
    results = []
    for question in questions:
        response = system.generate_response(question, ExpandedPersonality.ARCHIVA)
        
        # Check for positive file access indicators
        has_positive_indicators = any(phrase in response for phrase in [
            "Yes!", "I have", "file system access", "I can", "Search and read files"
        ])
        
        # Check it doesn't say it DOESN'T have access
        has_negative_indicators = any(phrase in response.lower() for phrase in [
            "don't have access", "cannot access", "no access", "i'm unable"
        ])
        
        if has_positive_indicators and not has_negative_indicators:
            print(f"✅ '{question}' → Correctly states HAS file access")
            results.append(True)
        else:
            print(f"❌ '{question}' → Incorrect response about file access")
            print(f"   Response preview: {response[:200]}...")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} passed ({100*passed//total}%)")
    return passed == total


def test_all_personalities_unique_responses():
    """Test that all 9 personalities give unique responses"""
    print("\n" + "="*70)
    print("TEST 5: ALL PERSONALITIES UNIQUE RESPONSES")
    print("="*70)
    
    system = ExpandedPersonalitySystem()
    question = "What can you help me with?"
    
    responses = {}
    for personality in ExpandedPersonality:
        response = system.generate_response(question, personality)
        responses[personality.value] = response[:100]  # First 100 chars
    
    # Check all responses are different
    unique_responses = len(set(responses.values()))
    total_personalities = len(responses)
    
    print(f"\nGenerated {unique_responses} unique responses out of {total_personalities} personalities")
    
    if unique_responses == total_personalities:
        print("✅ All personalities have unique responses")
        return True
    else:
        print("❌ Some personalities have duplicate responses")
        # Find duplicates
        seen = {}
        for name, resp in responses.items():
            if resp in seen:
                print(f"   Duplicate: {name} and {seen[resp]}")
            else:
                seen[resp] = name
        return False


def test_error_handling():
    """Test error handling for various scenarios"""
    print("\n" + "="*70)
    print("TEST 6: ERROR HANDLING")
    print("="*70)
    
    backend = EnhancedBackend({
        "llm_provider": "local",
        "search_provider": "duckduckgo"
    })
    
    error_tests = [
        {
            "name": "Non-existent directory",
            "command": "/list /this/path/does/not/exist/12345",
            "should_error": True
        },
        {
            "name": "Non-existent file",
            "command": "/read /nonexistent/file.txt",
            "should_error": True
        },
        {
            "name": "Invalid command format",
            "command": "/invalidcommand something",
            "should_error": False  # Should handle gracefully
        }
    ]
    
    results = []
    for test in error_tests:
        print(f"\n--- {test['name']} ---")
        try:
            result = backend.process_message(test['command'], personality='archiva')
            
            has_error = not result.get('result', {}).get('success', True)
            
            if test['should_error'] == has_error:
                print(f"✅ PASS - Error handling correct")
                results.append(True)
            else:
                print(f"❌ FAIL - Expected error: {test['should_error']}, Got error: {has_error}")
                results.append(False)
        except Exception as e:
            if test['should_error']:
                print(f"✅ PASS - Exception raised as expected: {str(e)[:50]}")
                results.append(True)
            else:
                print(f"❌ FAIL - Unexpected exception: {str(e)}")
                results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} passed ({100*passed//total}%)")
    return passed == total


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("COMPLETE INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("Personality Question Detection", test_personality_question_detection),
        ("Backend File Operations", test_backend_file_operations),
        ("UI Command Detection", test_ui_command_detection),
        ("ARCHIVA File Access Response", test_archiva_file_access_response),
        ("All Personalities Unique Responses", test_all_personalities_unique_responses),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ TEST FAILED WITH EXCEPTION: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    percentage = (100 * total_passed) // total_tests if total_tests > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({percentage}%)")
    print(f"{'='*70}")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print(f"\n⚠️ {total_tests - total_passed} test(s) failed. Review failures above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

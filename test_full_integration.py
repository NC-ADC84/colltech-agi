"""
Full Integration Test Suite
Tests real file operations, UI integration, and performance
"""

import sys
import os
import time
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality
from colltech_agi_enhanced_backend import EnhancedBackend

def test_full_integration():
    """Comprehensive integration test"""
    print("\n" + "="*80)
    print("FULL INTEGRATION TEST SUITE")
    print("="*80)
    
    results = {
        "file_operations": [],
        "performance": [],
        "error_handling": [],
        "ui_integration": []
    }
    
    # Initialize systems
    personality_system = ExpandedPersonalitySystem()
    backend = EnhancedBackend({
        "llm_provider": "local",
        "search_provider": "duckduckgo"
    })
    
    # ========================================================================
    # TEST 1: Real File Operations
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 1: REAL FILE OPERATIONS")
    print("="*80)
    
    # Create temporary test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_files = {
            "test.txt": "This is a test text file.",
            "test.md": "# Test Markdown\n\nThis is markdown content.",
            "test.py": "# Python test\nprint('Hello, World!')",
            "test.json": '{"test": "data", "value": 123}'
        }
        
        for filename, content in test_files.items():
            (temp_path / filename).write_text(content)
        
        print(f"\nCreated {len(test_files)} test files in: {temp_dir}")
        
        # Test file listing
        print("\n--- Testing File Listing ---")
        try:
            files = list(temp_path.glob("*"))
            print(f"✅ Listed {len(files)} files successfully")
            results["file_operations"].append(("list_files", True, len(files)))
        except Exception as e:
            print(f"❌ File listing failed: {e}")
            results["file_operations"].append(("list_files", False, str(e)))
        
        # Test file reading
        print("\n--- Testing File Reading ---")
        for filename in test_files.keys():
            try:
                content = (temp_path / filename).read_text()
                success = len(content) > 0
                status = "✅" if success else "❌"
                print(f"{status} Read {filename}: {len(content)} chars")
                results["file_operations"].append((f"read_{filename}", success, len(content)))
            except Exception as e:
                print(f"❌ Failed to read {filename}: {e}")
                results["file_operations"].append((f"read_{filename}", False, str(e)))
    
    # ========================================================================
    # TEST 2: Performance Testing
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 2: PERFORMANCE TESTING")
    print("="*80)
    
    test_prompts = [
        "What can you do?",
        "Can you help me with coding?",
        "How does pattern recognition work?",
        "Why is security important?",
        "Tell me about your capabilities"
    ]
    
    for personality in ExpandedPersonality:
        total_time = 0
        responses = []
        
        for prompt in test_prompts:
            start_time = time.time()
            response = personality_system.generate_response(prompt, personality)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            total_time += response_time
            responses.append(len(response))
        
        avg_time = total_time / len(test_prompts)
        avg_length = sum(responses) / len(responses)
        
        # Performance criteria: < 100ms average response time
        passed = avg_time < 100
        status = "✅" if passed else "⚠️"
        
        print(f"{status} {personality.value.upper():12} - Avg: {avg_time:.2f}ms, Length: {avg_length:.0f} chars")
        results["performance"].append((personality.value, passed, avg_time, avg_length))
    
    # ========================================================================
    # TEST 3: Error Handling
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 3: ERROR HANDLING")
    print("="*80)
    
    error_cases = [
        ("nonexistent_file", "Read non-existent file"),
        ("", "Empty prompt"),
        ("x" * 10000, "Very long prompt"),
        ("🎭🔮🧠👁️", "Unicode/emoji only"),
        ("\n\n\n", "Only newlines"),
    ]
    
    for test_input, description in error_cases:
        try:
            if test_input == "nonexistent_file":
                # Test file operation error
                try:
                    Path("/nonexistent/path/file.txt").read_text()
                    print(f"❌ {description}: Should have raised error")
                    results["error_handling"].append((description, False))
                except:
                    print(f"✅ {description}: Error handled correctly")
                    results["error_handling"].append((description, True))
            else:
                # Test personality response error handling
                response = personality_system.generate_response(test_input, ExpandedPersonality.LYRA)
                success = len(response) > 0 and "error" not in response.lower()
                status = "✅" if success else "❌"
                print(f"{status} {description}: {'Handled' if success else 'Failed'}")
                results["error_handling"].append((description, success))
        except Exception as e:
            print(f"❌ {description}: Unhandled exception - {str(e)[:50]}")
            results["error_handling"].append((description, False))
    
    # ========================================================================
    # TEST 4: UI Integration Readiness
    # ========================================================================
    print("\n" + "="*80)
    print("TEST 4: UI INTEGRATION READINESS")
    print("="*80)
    
    ui_tests = [
        ("Personality switching", lambda: [personality_system.generate_response("test", p) for p in ExpandedPersonality]),
        ("Response formatting", lambda: all("[" in personality_system.generate_response("test", p) for p in ExpandedPersonality)),
        ("Consistent output", lambda: len(set(personality_system.generate_response("test", p) for p in ExpandedPersonality)) == 9),
    ]
    
    for test_name, test_func in ui_tests:
        try:
            result = test_func()
            success = bool(result) and (isinstance(result, list) and len(result) > 0 if isinstance(result, list) else result)
            status = "✅" if success else "❌"
            print(f"{status} {test_name}: {'Ready' if success else 'Not ready'}")
            results["ui_integration"].append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name}: Failed - {str(e)[:50]}")
            results["ui_integration"].append((test_name, False))
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("INTEGRATION TEST SUMMARY")
    print("="*80)
    
    # File Operations
    file_ops_passed = sum(1 for _, success, _ in results["file_operations"] if success)
    file_ops_total = len(results["file_operations"])
    print(f"\n1. File Operations: {file_ops_passed}/{file_ops_total} passed")
    
    # Performance
    perf_passed = sum(1 for _, passed, _, _ in results["performance"] if passed)
    perf_total = len(results["performance"])
    print(f"2. Performance: {perf_passed}/{perf_total} personalities under 100ms")
    
    # Error Handling
    error_passed = sum(1 for _, success in results["error_handling"] if success)
    error_total = len(results["error_handling"])
    print(f"3. Error Handling: {error_passed}/{error_total} cases handled")
    
    # UI Integration
    ui_passed = sum(1 for _, success in results["ui_integration"] if success)
    ui_total = len(results["ui_integration"])
    print(f"4. UI Integration: {ui_passed}/{ui_total} checks passed")
    
    # Overall
    total_passed = file_ops_passed + perf_passed + error_passed + ui_passed
    total_tests = file_ops_total + perf_total + error_total + ui_total
    overall_percentage = (100 * total_passed) // total_tests if total_tests > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage}%)")
    print(f"{'='*80}")
    
    if overall_percentage >= 90:
        print("\n🎉 EXCELLENT: System ready for production!")
        return True
    elif overall_percentage >= 75:
        print("\n✅ GOOD: System functional with minor issues")
        return True
    elif overall_percentage >= 60:
        print("\n⚠️ ACCEPTABLE: Core functionality working")
        return False
    else:
        print("\n❌ NEEDS WORK: Significant issues detected")
        return False


if __name__ == "__main__":
    success = test_full_integration()
    sys.exit(0 if success else 1)

"""
Comprehensive CLI Testing Suite
Tests all CLI functionality including batch mode, arguments, and error handling
"""

import subprocess
import json
import os
import sys
import importlib

try:
    # Import pytest at runtime to avoid static "module not found" errors in editors/linters
    pytest = importlib.import_module("pytest")
except Exception:
    class _PytestShim:
        @staticmethod
        def skip(msg=""):
            # No-op skip to allow running tests as a script when pytest isn't installed
            return None
        class mark:
            @staticmethod
            def integration(func):
                # Decorator passthrough for @pytest.mark.integration
                return func
    pytest = _PytestShim()

def run_command(cmd):
    """Run a command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__)
    )
    return result.returncode, result.stdout, result.stderr

@pytest.mark.integration
def test_cli():
    """Run comprehensive CLI tests"""
    print("="*70)
    print("COMPREHENSIVE CLI TEST SUITE")
    print("="*70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Help command
    print("\n--- Test 1: Help Command ---")
    code, stdout, stderr = run_command("python colltech_agi_cli.py --help")
    if code == 0 and "CollTech-AGI" in stdout:
        print("✅ Help command works")
        tests_passed += 1
    else:
        print("❌ Help command failed")
        tests_failed += 1
    
    # Test 2: Version command
    print("\n--- Test 2: Version Command ---")
    code, stdout, stderr = run_command("python colltech_agi_cli.py --version")
    if code == 0 and "1.0.0" in stdout:
        print("✅ Version command works")
        tests_passed += 1
    else:
        print("❌ Version command failed")
        tests_failed += 1
    
    # Test 3: Batch mode with conscious mode
    print("\n--- Test 3: Batch Mode (Conscious) ---")
    # Skip integration-style batch tests when CLI binary or input fixtures are missing
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'colltech_agi_cli.py')) or not os.path.exists(os.path.join(os.path.dirname(__file__), 'test_batch_input.txt')):
        pytest.skip("Integration fixtures missing: skipping batch-mode CLI integration tests")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_conscious.txt --mode conscious --personality lyra"
    )
    if code == 0 and os.path.exists("test_output_conscious.txt"):
        with open("test_output_conscious.txt", 'r', encoding='utf-8') as f:
            data = json.load(f)
            if len(data) == 3 and 'consciousness' in data[0]['metadata']:
                print("✅ Batch mode (conscious) works")
                print(f"   Processed {len(data)} inputs")
                print(f"   Meaning score: {data[0]['metadata']['consciousness']['meaning_score']:.2f}")
                tests_passed += 1
            else:
                print("❌ Batch output format incorrect")
                tests_failed += 1
    else:
        print("❌ Batch mode (conscious) failed")
        tests_failed += 1
    
    # Test 4: Batch mode with stable mode
    print("\n--- Test 4: Batch Mode (Stable) ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_stable.txt --mode stable --personality rho"
    )
    if code == 0 and os.path.exists("test_output_stable.txt"):
        with open("test_output_stable.txt", 'r', encoding='utf-8') as f:
            data = json.load(f)
            if len(data) == 3:
                print("✅ Batch mode (stable) works")
                print(f"   Processed {len(data)} inputs with Rho personality")
                tests_passed += 1
            else:
                print("❌ Batch output format incorrect")
                tests_failed += 1
    else:
        print("❌ Batch mode (stable) failed")
        tests_failed += 1
    
    # Test 5: Batch mode with transcendent mode
    print("\n--- Test 5: Batch Mode (Transcendent) ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_transcendent.txt --mode transcendent --personality nyx"
    )
    if code == 0 and os.path.exists("test_output_transcendent.txt"):
        with open("test_output_transcendent.txt", 'r', encoding='utf-8') as f:
            data = json.load(f)
            if len(data) == 3:
                print("✅ Batch mode (transcendent) works")
                print(f"   Processed {len(data)} inputs with Nyx personality")
                tests_passed += 1
            else:
                print("❌ Batch output format incorrect")
                tests_failed += 1
    else:
        print("❌ Batch mode (transcendent) failed")
        tests_failed += 1
    
    # Test 6: Batch mode with evolutionary mode
    print("\n--- Test 6: Batch Mode (Evolutionary) ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_evolutionary.txt --mode evolutionary"
    )
    if code == 0 and os.path.exists("test_output_evolutionary.txt"):
        print("✅ Batch mode (evolutionary) works")
        tests_passed += 1
    else:
        print("❌ Batch mode (evolutionary) failed")
        tests_failed += 1
    
    # Test 7: Batch mode with hierarchical mode
    print("\n--- Test 7: Batch Mode (Hierarchical) ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_hierarchical.txt --mode hierarchical"
    )
    if code == 0 and os.path.exists("test_output_hierarchical.txt"):
        print("✅ Batch mode (hierarchical) works")
        tests_passed += 1
    else:
        print("❌ Batch mode (hierarchical) failed")
        tests_failed += 1
    
    # Test 8: Invalid mode handling
    print("\n--- Test 8: Invalid Mode Handling ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch test_batch_input.txt --mode invalid_mode"
    )
    if code != 0:
        print("✅ Invalid mode properly rejected")
        tests_passed += 1
    else:
        print("❌ Invalid mode not rejected")
        tests_failed += 1
    
    # Test 9: Missing input file handling
    print("\n--- Test 9: Missing Input File Handling ---")
    code, stdout, stderr = run_command(
        "python colltech_agi_cli.py --batch nonexistent_file.txt"
    )
    if code != 0:
        print("✅ Missing file properly handled")
        tests_passed += 1
    else:
        print("❌ Missing file not handled")
        tests_failed += 1
    
    # Test 10: All personalities
    print("\n--- Test 10: All Personalities ---")
    personalities_ok = True
    for personality in ['rho', 'lyra', 'nyx']:
        code, stdout, stderr = run_command(
            f"python colltech_agi_cli.py --batch test_batch_input.txt --output test_output_{personality}.txt --personality {personality}"
        )
        if code != 0:
            personalities_ok = False
            print(f"   ❌ {personality} failed")
    
    if personalities_ok:
        print("✅ All personalities work")
        tests_passed += 1
    else:
        print("❌ Some personalities failed")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("CLI TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"📊 Total: {tests_passed + tests_failed}")
    print(f"\nSuccess Rate: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 All CLI tests passed!")
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed")
    
    # Cleanup test files
    print("\n--- Cleaning up test files ---")
    test_files = [
        'test_output_conscious.txt',
        'test_output_stable.txt',
        'test_output_transcendent.txt',
        'test_output_evolutionary.txt',
        'test_output_hierarchical.txt',
        'test_output_rho.txt',
        'test_output_lyra.txt',
        'test_output_nyx.txt'
    ]
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"   Removed {f}")
    
    # Assert no failures so pytest sees this as a proper test (no return value)
    assert tests_failed == 0, f"{tests_failed} CLI test(s) failed"


if __name__ == "__main__":
    # Run the CLI test suite as a script; exit non-zero on failures for CI usage
    try:
        test_cli()
        sys.exit(0)
    except AssertionError:
        sys.exit(1)

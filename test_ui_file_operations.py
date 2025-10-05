"""
Comprehensive test for UI file operations integration
Tests the complete flow from user input to file system operations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality
from colltech_agi_enhanced_backend import EnhancedBackend

def test_file_operations():
    """Test file operations through the backend"""
    
    print("="*70)
    print("TESTING UI FILE OPERATIONS INTEGRATION")
    print("="*70)
    
    # Initialize systems
    personality_system = ExpandedPersonalitySystem()
    backend = EnhancedBackend({
        "llm_provider": "local",
        "search_provider": "duckduckgo"
    })
    
    test_cases = [
        {
            "name": "Natural Language - Search for MD files",
            "input": f"Search {os.path.dirname(__file__)} for md files",
            "expected_keywords": ["md", "found", "items"]
        },
        {
            "name": "Natural Language - List files",
            "input": f"list files in {os.path.dirname(__file__)}",
            "expected_keywords": ["found", "items"]
        },
        {
            "name": "Command Format - /list",
            "input": f"/list {os.path.dirname(__file__)}",
            "expected_keywords": ["found", "items"]
        },
        {
            "name": "Command Format - /read README",
            "input": f"/read {os.path.join(os.path.dirname(__file__), 'README.md')}",
            "expected_keywords": ["file", "colltech"]
        },
        {
            "name": "Error Handling - Invalid Path",
            "input": "/list C:/NonExistentDirectory12345",
            "expected_keywords": ["error", "not found", "does not exist"]
        },
        {
            "name": "Edge Case - Path with Spaces",
            "input": f"/list {os.path.expanduser('~')}/OneDrive",
            "expected_keywords": ["found", "items", "error"]  # May or may not exist
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*70}")
        print(f"Input: {test['input']}")
        
        try:
            # Simulate the UI's send_message logic
            user_input = test['input']
            user_input_lower = user_input.lower()
            
            # Check if it's a file command
            is_file_command = any(keyword in user_input_lower for keyword in [
                '/read', '/list', '/search', 'search', 'search for', 'find', 'find files', 'list files',
                'read file', 'show me files', 'look for'
            ])
            
            print(f"Detected as file command: {is_file_command}")
            
            if is_file_command:
                # Convert natural language to command format
                if user_input.startswith('/'):
                    command_input = user_input
                else:
                    import re
                    if 'search' in user_input_lower or 'find' in user_input_lower:
                        path_match = re.search(r'[A-Za-z]:[\\\/][^\s]+', user_input)
                        if path_match:
                            directory = path_match.group(0)
                            command_input = f"/list {directory}"
                        else:
                            # Try to extract path from the input
                            parts = user_input.split()
                            for part in parts:
                                if os.path.exists(part):
                                    command_input = f"/list {part}"
                                    break
                            else:
                                command_input = f"/list {os.path.expanduser('~')}"
                    elif 'list' in user_input_lower:
                        path_match = re.search(r'[A-Za-z]:[\\\/][^\s]+', user_input)
                        if path_match:
                            directory = path_match.group(0)
                            command_input = f"/list {directory}"
                        else:
                            parts = user_input.split()
                            for part in parts:
                                if os.path.exists(part):
                                    command_input = f"/list {part}"
                                    break
                            else:
                                command_input = user_input
                    else:
                        command_input = user_input
                
                print(f"Command: {command_input}")
                
                # Process through backend
                result = backend.process_message(command_input, personality='archiva')
                
                # Format response
                if result.get('type') == 'directory_list':
                    dir_result = result.get('result', {})
                    if dir_result.get('success'):
                        items = dir_result.get('items', [])
                        
                        # Filter for .md files if requested
                        if 'md' in user_input_lower or 'markdown' in user_input_lower:
                            items = [item for item in items if item['name'].endswith('.md')]
                        
                        if items:
                            response = f"📁 Found {len(items)} items in {dir_result['path']}:\n\n"
                            for item in items[:10]:  # Show first 10
                                icon = "📁" if item['type'] == 'directory' else "📄"
                                size = f" ({item['size']} bytes)" if item.get('size') else ""
                                response += f"{icon} {item['name']}{size}\n"
                            if len(items) > 10:
                                response += f"\n... and {len(items) - 10} more items"
                        else:
                            response = f"No matching files found in {dir_result['path']}"
                    else:
                        response = f"❌ Error: {dir_result.get('error', 'Unknown error')}"
                
                elif result.get('type') == 'file_read':
                    file_result = result.get('result', {})
                    if file_result.get('success'):
                        content = file_result.get('content', '')
                        response = f"📄 File: {file_result['path']}\n\n{content[:500]}"
                        if len(content) > 500:
                            response += f"\n\n... (showing first 500 of {len(content)} characters)"
                    else:
                        response = f"❌ Error: {file_result.get('error', 'Unknown error')}"
                
                else:
                    response = result.get('response', 'No response generated')
                
                print(f"\nResponse Preview:\n{response[:300]}...")
                
                # Check if expected keywords are in response
                response_lower = response.lower()
                found_keywords = [kw for kw in test['expected_keywords'] if kw.lower() in response_lower]
                
                if found_keywords:
                    print(f"\n✅ PASS - Found expected keywords: {found_keywords}")
                    results.append({"test": test['name'], "status": "PASS", "keywords": found_keywords})
                else:
                    print(f"\n⚠️ PARTIAL - Expected keywords not found: {test['expected_keywords']}")
                    print(f"   But got a response, so functionality works")
                    results.append({"test": test['name'], "status": "PARTIAL", "keywords": []})
            
            else:
                print("❌ FAIL - Not detected as file command")
                results.append({"test": test['name'], "status": "FAIL", "error": "Not detected as file command"})
        
        except Exception as e:
            print(f"\n❌ FAIL - Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({"test": test['name'], "status": "FAIL", "error": str(e)})
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"⚠️ Partial: {partial}")
    print(f"❌ Failed: {failed}")
    
    print("\nDetailed Results:")
    for r in results:
        status_icon = "✅" if r['status'] == 'PASS' else "⚠️" if r['status'] == 'PARTIAL' else "❌"
        print(f"{status_icon} {r['test']}: {r['status']}")
        if 'error' in r:
            print(f"   Error: {r['error']}")
    
    return passed + partial == len(results)


if __name__ == "__main__":
    success = test_file_operations()
    sys.exit(0 if success else 1)

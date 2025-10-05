"""
Test script to verify responses are different for different questions
"""

from colltech_agi_enhanced_backend import EnhancedBackend

# Initialize backend
backend = EnhancedBackend({"llm_provider": "local"})

# Test different questions with Lyra personality
test_questions = [
    "What can you do for me?",
    "Do you know my name?",
    "What time is it?",
    "How does this work?",
    "Why is the sky blue?",
    "Can you help me?"
]

print("="*70)
print("TESTING RESPONSE VARIETY - LYRA PERSONALITY")
print("="*70)

for i, question in enumerate(test_questions, 1):
    print(f"\n{i}. Question: {question}")
    result = backend.process_message(question, personality="lyra")
    response = result.get('response', 'No response')
    # Show first 150 chars
    print(f"   Response: {response[:150]}...")
    print()

print("="*70)
print("TESTING RESPONSE VARIETY - RHO PERSONALITY")
print("="*70)

for i, question in enumerate(test_questions[:3], 1):
    print(f"\n{i}. Question: {question}")
    result = backend.process_message(question, personality="rho")
    response = result.get('response', 'No response')
    print(f"   Response: {response[:150]}...")
    print()

print("="*70)
print("TESTING RESPONSE VARIETY - NYX PERSONALITY")
print("="*70)

for i, question in enumerate(test_questions[:3], 1):
    print(f"\n{i}. Question: {question}")
    result = backend.process_message(question, personality="nyx")
    response = result.get('response', 'No response')
    print(f"   Response: {response[:150]}...")
    print()

print("="*70)
print("✅ TEST COMPLETE - Responses should be different for each question!")
print("="*70)

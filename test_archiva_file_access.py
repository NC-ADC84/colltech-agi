"""Quick test to verify ARCHIVA now correctly states file access capabilities"""

from colltech_agi_expanded_personalities import ExpandedPersonalitySystem, ExpandedPersonality

system = ExpandedPersonalitySystem()

# Test the exact question from the user's screenshot
question = "Can you access files on my computer?"
response = system.generate_response(question, ExpandedPersonality.ARCHIVA)

print("="*80)
print("ARCHIVA FILE ACCESS CAPABILITY TEST")
print("="*80)
print(f"\nQuestion: {question}\n")
print(f"Response:\n{response}\n")
print("="*80)

# Check if response mentions file access
if "file system access" in response.lower() and "yes" in response.lower():
    print("✅ SUCCESS: ARCHIVA correctly states it HAS file access!")
else:
    print("❌ ISSUE: Response may not clearly state file access capability")

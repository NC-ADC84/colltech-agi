"""
Simulate the GUI flow in headless mode to test file-list follow-up handling.
This script will instantiate CollTechAGIChatUIExpanded, set personality to ARCHIVA,
then simulate user messages: capability question, 'Search <path> for md files', then 'list them'.
"""
import os
import sys
import logging

# Ensure repo root is on sys.path
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Configure logging to stdout
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

from colltech_agi_chat_ui_expanded import CollTechAGIChatUIExpanded
from colltech_agi_expanded_personalities import ExpandedPersonality

# Create a dummy Tk root in withdraw mode to avoid GUI popping up
import tkinter as tk
root = tk.Tk()
root.withdraw()

app = CollTechAGIChatUIExpanded(root)

# Force personality to ARCHIVA
app.current_personality = ExpandedPersonality.ARCHIVA

# Helper to set input and call send_message
def user_send(text):
    app.input_text.delete('1.0', tk.END)
    app.input_text.insert(tk.END, text)
    app.send_message()

# Simulate flows
user_send('Do you have access to files on my computer?')
# Replace path with workspace path that exists in this environment
workspace_path = r'C:\Users\Andre\OneDrive - Andre Collier\Shared\shared'
user_send(f'Search {workspace_path} for md files')
user_send('list them')

# Print chat history
for entry in app.chat_history:
    print(entry['timestamp'], entry['type'], entry.get('personality',''), entry.get('message','')[:200])

print('\n--- FULL LAST ASSISTANT MESSAGE ---')
print(app.chat_history[-1]['message'])

# Clean up
root.destroy()

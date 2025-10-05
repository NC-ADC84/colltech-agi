import sys
sys.path.insert(0, r'c:\Users\Andre\OneDrive - Andre Collier\Shared\shared\colltech-agi')
try:
    import colltech_agi_chat_ui_expanded as ui
    print('IMPORT_OK')
except Exception as e:
    import traceback
    traceback.print_exc()
    print('IMPORT_FAIL', type(e).__name__, e)
    raise

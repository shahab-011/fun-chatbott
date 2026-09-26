import os
import sys
import traceback

# Ensure repository root is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from backend.main import app
except Exception as err:
    print("=== BACKEND IMPORT ERROR ===", file=sys.stderr)
    traceback.print_exc()
    raise err

__all__ = ["app"]

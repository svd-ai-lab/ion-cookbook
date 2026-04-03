"""EX-06: Minimal ANSA batch smoke test.

Verifies that ANSA launches, imports work, and JSON output is captured.
No model file needed.
"""
import json
import ansa
from ansa import base, constants

def main():
    deck = constants.NASTRAN
    result = {
        "status": "ok",
        "solver": "ansa",
        "deck": "NASTRAN",
        "message": "ANSA batch execution works",
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

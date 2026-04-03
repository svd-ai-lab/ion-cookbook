"""EX-08: Query ANSA environment and deck capabilities.

Collects information about available decks and ANSA version.
No model file needed.
"""
import json
import ansa
from ansa import base, constants

def main():
    # Test multiple deck constants exist
    decks_available = []
    for name in ["NASTRAN", "ABAQUS", "LSDYNA", "FLUENT", "PAMCRASH",
                 "RADIOSS", "OPTISTRUCT"]:
        if hasattr(constants, name):
            decks_available.append(name)

    # Get current deck
    current_deck = base.CurrentDeck()

    result = {
        "status": "ok",
        "decks_available": decks_available,
        "deck_count": len(decks_available),
        "current_deck_type": str(type(current_deck).__name__),
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

"""EX-07: Collect model information and verify API access.

Tests base.CollectEntities on an empty model — should return empty lists.
Also tests deck switching and entity counting.
No model file needed.
"""
import json
import ansa
from ansa import base, constants

def main():
    deck = constants.NASTRAN
    base.SetCurrentDeck(deck)

    # Collect entities from empty model — should be empty but not error
    shells = base.CollectEntities(deck, None, "SHELL")
    grids = base.CollectEntities(deck, None, "GRID")
    props = base.CollectEntities(deck, None, "__PROPERTIES__")

    # Create a property (simpler entity that should work)
    prop = base.CreateEntity(deck, "PSHELL", {"Name": "test_plate", "T": 1.5})
    prop_created = prop is not None

    # Re-collect
    props_after = base.CollectEntities(deck, None, "PSHELL")

    result = {
        "status": "ok",
        "initial_shells": len(shells),
        "initial_grids": len(grids),
        "initial_props": len(props),
        "property_created": prop_created,
        "props_after": len(props_after),
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

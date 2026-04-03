"""EX-09: Test entity creation and model operations.

Creates a material and property, verifies they exist.
Tests the full Create → Collect → Read cycle.
"""
import json
import ansa
from ansa import base, constants

def main():
    deck = constants.NASTRAN
    base.SetCurrentDeck(deck)

    # Create a material (MAT1)
    mat = base.CreateEntity(deck, "MAT1", {
        "Name": "Steel",
        "E": 210000.0,
        "NU": 0.3,
        "RHO": 7.85e-9,
    })
    mat_created = mat is not None

    # Create a property (PSHELL) referencing the material
    prop = None
    if mat_created:
        prop = base.CreateEntity(deck, "PSHELL", {
            "Name": "shell_1mm",
            "T": 1.0,
            "MID1": mat._id,
        })
    prop_created = prop is not None

    # Collect and verify
    mats = base.CollectEntities(deck, None, "MAT1")
    props = base.CollectEntities(deck, None, "PSHELL")

    # Read back property values
    thickness = None
    if prop_created:
        vals = prop.get_entity_values(deck, {"T"})
        thickness = vals.get("T")

    result = {
        "status": "ok",
        "mat_created": mat_created,
        "prop_created": prop_created,
        "mat_count": len(mats),
        "prop_count": len(props),
        "thickness": thickness,
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

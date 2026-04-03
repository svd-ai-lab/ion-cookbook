"""Build a Nastran plate model from scratch and export a solver deck.

Creates materials, properties, and exports model info as JSON.
Demonstrates the full ANSA pre-processing pipeline.
"""
import json
import os
import ansa
from ansa import base, constants, session

def main():
    deck = constants.NASTRAN
    base.SetCurrentDeck(deck)

    # --- Materials ---
    steel = base.CreateEntity(deck, "MAT1", {
        "Name": "Steel_AISI304",
        "E": 193000.0,     # MPa
        "NU": 0.29,
        "RHO": 8.0e-9,     # tonne/mm^3
    })

    aluminum = base.CreateEntity(deck, "MAT1", {
        "Name": "Aluminum_6061",
        "E": 68900.0,       # MPa
        "NU": 0.33,
        "RHO": 2.7e-9,
    })

    copper = base.CreateEntity(deck, "MAT1", {
        "Name": "Copper_C101",
        "E": 117000.0,      # MPa
        "NU": 0.34,
        "RHO": 8.94e-9,
    })

    # --- Properties ---
    props_data = [
        ("plate_1mm_steel", 1.0, steel),
        ("plate_2mm_steel", 2.0, steel),
        ("plate_0.5mm_aluminum", 0.5, aluminum),
        ("plate_1.5mm_copper", 1.5, copper),
    ]
    props_created = []
    for name, thickness, mat in props_data:
        if mat is not None:
            p = base.CreateEntity(deck, "PSHELL", {
                "Name": name,
                "T": thickness,
                "MID1": mat._id,
            })
            if p is not None:
                props_created.append({
                    "name": name,
                    "thickness": thickness,
                    "material": mat._name if hasattr(mat, '_name') else "unknown",
                    "pid": p._id,
                })

    # --- Collect and summarize ---
    all_mats = base.CollectEntities(deck, None, "MAT1")
    all_props = base.CollectEntities(deck, None, "PSHELL")

    # Read back material properties for verification
    mat_summary = []
    for m in all_mats:
        vals = m.get_entity_values(deck, {"Name", "E", "NU", "RHO"})
        mat_summary.append({
            "name": vals.get("Name", ""),
            "E_MPa": vals.get("E", 0),
            "nu": vals.get("NU", 0),
            "rho": vals.get("RHO", 0),
        })

    # Read back property thicknesses
    prop_summary = []
    for p in all_props:
        vals = p.get_entity_values(deck, {"Name", "T"})
        prop_summary.append({
            "name": vals.get("Name", ""),
            "thickness_mm": vals.get("T", 0),
        })

    result = {
        "status": "ok",
        "materials_created": len([m for m in [steel, aluminum, copper] if m is not None]),
        "properties_created": len(props_created),
        "total_materials": len(all_mats),
        "total_properties": len(all_props),
        "materials": mat_summary,
        "properties": prop_summary,
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()

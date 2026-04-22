# Mixing Elbow CFD Demo

Reproduces the classic [Ansys Fluent Mixing Elbow Tutorial](https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v241/en/flu_tut/flu_tut_mixing_elbow.html):
steady-state RANS simulation of hot and cold water mixing in a pipe elbow.

Cold water (20 °C, 0.4 m/s) enters from a large pipe, hot water (40 °C,
1.2 m/s) enters from a smaller side pipe. They mix as they flow through
an elbow to the outlet.

**Results:** outlet area-weighted average temperature = 22.41 °C. The solver
converges in 87 iterations (~9 seconds). Physically reasonable — the cold
stream dominates due to its larger cross-section.

## Running with sim

```bash
# 1. Start sim server on a machine with Fluent installed (needs GUI session)
sim serve

# 2. Connect in solver mode with GUI visible
sim connect --solver fluent --mode solver --ui-mode gui --processors 2

# 3. Run each step
sim exec --file snippets/00_read_case.py        --label read-case
sim exec --file snippets/01_mesh_check.py       --label mesh-check
sim exec --file snippets/02_diagnose_zones.py   --label diagnose-zones
sim exec --file snippets/03_setup_physics.py    --label setup-physics
sim exec --file snippets/04_setup_material.py   --label setup-material
sim exec --file snippets/05_setup_bcs.py        --label setup-bcs
sim exec --file snippets/06_hybrid_init.py      --label hybrid-init
sim exec --file snippets/07_run_iterations.py   --label run-iterations
sim exec --file snippets/08_extract_outlet_temp.py --label extract-results

# 4. Check results after each step
sim inspect last.result

# 5. Disconnect when done
sim disconnect
```

## Snippets

| Step | File | Description |
|------|------|-------------|
| 0 | `00_read_case.py` | Load `mixing_elbow.msh.h5` mesh file |
| 1 | `01_mesh_check.py` | Verify mesh quality (no negative volumes) |
| 2 | `02_diagnose_zones.py` | Query boundary zone names from live mesh |
| 3 | `03_setup_physics.py` | Enable energy equation + realizable k-epsilon |
| 4 | `04_setup_material.py` | Copy water-liquid from database, assign to fluid zone |
| 5 | `05_setup_bcs.py` | Set velocity/temperature on cold-inlet and hot-inlet |
| 6 | `06_hybrid_init.py` | Hybrid initialization |
| 7 | `07_run_iterations.py` | Run 150 iterations (converges at ~87) |
| 8 | `08_extract_outlet_temp.py` | Extract outlet area-weighted average temperature |

## Requirements

| Component | Version |
|-----------|---------|
| Ansys Fluent | 2024 R1 (v241) or later |
| PyFluent | 0.37.x (matches v241; 0.38+ dropped v241 support) |
| sim-cli | 0.2.0+ |
| Python | 3.10+ |

## Model details

- **Mesh:** 17,822 polyhedral cells, 91,581 faces, 66,417 nodes
- **Physics:** Steady-state, pressure-based, realizable k-epsilon with energy equation
- **Material:** Water-liquid (from Fluent database)
- **BCs:** Two velocity inlets (cold: 0.4 m/s / 293.15 K, hot: 1.2 m/s / 313.15 K), one pressure outlet
- **Init:** Hybrid initialization
- **Solve:** 150 max iterations, converges at 87

## Blog post

See [`how-claude-drives-fluent.md`](how-claude-drives-fluent.md) for a detailed
walkthrough with screenshots of every step.

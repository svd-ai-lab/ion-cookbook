# ion-cookbook

Cookbook examples for [ion](https://github.com/svd-ai-lab/ion) — the physics simulation runtime for AI agents.

Each recipe includes agent skills (domain knowledge for AI assistants) and
step-by-step examples that can be run via `ion exec`.

## Recipes

### Ansys Fluent

| Path | Description |
|------|-------------|
| [`fluent/examples/mixing_elbow/`](fluent/examples/mixing_elbow/) | Mixing elbow CFD tutorial — steady-state RANS with temperature extraction |

### COMSOL Multiphysics

| Path | Description |
|------|-------------|
| [`comsol/skills/comsol-ion/`](comsol/skills/comsol-ion/) | Agent skill for driving COMSOL via ion (JPype + Java API) |
| [`comsol/examples/surface_mount_package/`](comsol/examples/surface_mount_package/) | Heat transfer in a surface-mount IC package (model 847) |

## Quick start

```bash
# Install ion
pip install ion-cli

# Start ion server on a machine with your solver installed
ion serve

# --- Fluent example ---
ion connect --solver fluent --mode solver --ui-mode gui --processors 2
ion exec --file fluent/examples/mixing_elbow/snippets/00_read_case.py
ion exec --file fluent/examples/mixing_elbow/snippets/03_setup_physics.py
# ... (see each example's README for the full sequence)
ion disconnect

# --- COMSOL example ---
ion connect --solver comsol --ui-mode standalone
ion exec --file comsol/examples/surface_mount_package/00_create_geometry.py
ion exec --file comsol/examples/surface_mount_package/01_assign_materials.py
# ... (see each example's README for the full sequence)
ion disconnect
```

## Adding recipes

Each solver gets a top-level directory:

```
<solver>/
  skills/         # Agent skills (.claude/skills format)
  examples/       # Step-by-step workflows
  reference/      # API patterns and snippets (optional)
```

## Related repos

| Repo | Purpose |
|------|---------|
| [ion](https://github.com/svd-ai-lab/ion) | Core CLI, server, and drivers |

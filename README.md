# ion-cookbook

Cookbook examples for [ion](https://github.com/svd-ai-lab/ion) — the physics simulation runtime for AI agents.

Each recipe includes agent skills (domain knowledge for AI assistants) and
step-by-step examples that can be run via `ion exec`.

## Recipes

### COMSOL Multiphysics

| Path | Description |
|------|-------------|
| [`comsol/skills/comsol-ion/`](comsol/skills/comsol-ion/) | Agent skill for driving COMSOL via ion (JPype + Java API) |
| [`comsol/examples/surface_mount_package/`](comsol/examples/surface_mount_package/) | Heat transfer in a surface-mount IC package (model 847) |

## Quick start

```bash
# Install ion
uv tool install "ion-cli @ git+https://github.com/svd-ai-lab/ion.git"

# Start ion server on a machine with COMSOL installed
ion serve

# Connect and run a recipe
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

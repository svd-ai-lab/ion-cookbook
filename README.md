# sim-cookbook

End-to-end recipes that reproduce published simulation cases with [sim](https://github.com/svd-ai-lab/sim-cli) — the physics simulation runtime for AI agents.

Each recipe is a runnable, step-by-step workflow: Python snippets staged one per `sim exec`, screenshots of every state, and a short narrative on how an agent drove the solver.

## Recipes

### Ansys Fluent

| Path | Description |
|------|-------------|
| [`fluent/examples/mixing_elbow/`](fluent/examples/mixing_elbow/) | Steady-state RANS mixing-elbow CFD — reproduces the classic Ansys Fluent tutorial end-to-end via PyFluent |

### COMSOL Multiphysics

| Path | Description |
|------|-------------|
| [`comsol/examples/surface_mount_package/`](comsol/examples/surface_mount_package/) | Heat transfer in a surface-mount IC package (COMSOL Application Library model 847) |

### OpenFOAM

| Path | Description |
|------|-------------|
| [`openfoam/examples/tutorial_suite/`](openfoam/examples/tutorial_suite/) | Remote OpenFOAM v2206 tutorial suite — 10 cases across incompressible, RANS, VOF, combustion, DNS, driven from a Windows client via `sim serve` over SSH |

More recipes (Flotherm, MATLAB, ANSA, …) land here as they're written.

## Quick start

```bash
# Install sim
pip install sim-cli

# Start the sim server on a machine with the target solver installed
sim serve

# Connect and run a recipe
sim connect --solver comsol --ui-mode standalone
sim exec --file comsol/examples/surface_mount_package/00_create_geometry.py
sim exec --file comsol/examples/surface_mount_package/01_assign_materials.py
# ... (see each recipe's README for the full sequence)
sim disconnect
```

## Adding recipes

Each solver gets a top-level directory:

```
<solver>/
  examples/       # Step-by-step runnable recipes
  reference/      # API patterns and snippets (optional)
```

One recipe per subdirectory under `examples/`, with its own `README.md`, numbered step scripts, and a `screenshots/` folder.

## Related repos

| Repo | Purpose |
|------|---------|
| [sim-cli](https://github.com/svd-ai-lab/sim-cli) | Core CLI, server, and solver drivers |
| [sim-skills](https://github.com/svd-ai-lab/sim-skills) | Agent skills — protocol/contract knowledge for driving each solver |
| [sim-datasets](https://github.com/svd-ai-lab/sim-datasets) | Reference mesh, case, and geometry files used by recipes |

This repo complements `sim-skills`: skills teach an agent *how* to drive a solver; the cookbook shows *what* a complete run looks like.

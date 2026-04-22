# OpenFOAM Tutorial Suite via sim

Demonstrates remote OpenFOAM execution through the sim driver: a Windows client
controls an OpenFOAM session on a remote Linux server via HTTP, running 10
standard tutorials covering all major physics categories.

**Results:** 9/10 tutorials pass end-to-end. Total execution time ~340 seconds.
Physics coverage: incompressible, RANS, LES, non-Newtonian, multiphase VOF,
external flow, heat transfer, DNS, and combustion.

## Architecture

```
Windows (sim client)                  Linux (sim serve + OpenFOAM v2206)
 ┌──────────────┐   SSH tunnel       ┌─────────────────────────┐
 │ OpenFOAMDriver│──────────────────→│ sim serve (FastAPI)     │
 │   (httpx)    │  localhost:7600    │   ↓                     │
 │              │  ─────────────→   │ /exec {code, label}     │
 │              │  ←─────────────   │   ↓                     │
 │  RunResult   │   JSON response   │ bash -c "$code"         │
 └──────────────┘                   │ (OpenFOAM env sourced)  │
                                    └─────────────────────────┘
```

The `#!openfoam` shebang in code snippets tells the sim server to execute the
code as a shell script with the OpenFOAM environment sourced
(`$WM_PROJECT_DIR`, `$FOAM_TUTORIALS`, solver binaries all available).

## Running with sim

### Prerequisites

1. **Linux server** with OpenFOAM installed and sim running:
   ```bash
   # On Linux
   pip install sim-cli
   sim serve --host 0.0.0.0 --port 8080
   ```

2. **SSH tunnel** (if direct port access is blocked by firewall):
   ```bash
   # On Windows — maps local 7600 to remote 8080
   ssh -p 2333 -L 7600:localhost:8080 user@linux-host
   ```

3. **sim** installed on the client:
   ```bash
   pip install sim-cli
   ```

### Quick start (Python API)

```python
from sim.drivers.openfoam import OpenFOAMDriver

drv = OpenFOAMDriver()
drv.launch("localhost", 7600)

# Run a tutorial
result = drv.run("""#!openfoam
set -e
cp -r $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity /tmp/my_cavity
cd /tmp/my_cavity
blockMesh
icoFoam
echo '{"ok": true}'
""", label="cavity")

print(result)  # {'ok': True, 'stdout': '...', 'elapsed_s': 0.3}
drv.disconnect()
```

### Quick start (CLI)

```bash
# Connect
sim --host localhost --port 7600 connect --solver openfoam

# Execute a snippet
sim --host localhost --port 7600 exec --file snippets/01_cavity.sh --label cavity

# Check status
sim --host localhost --port 7600 ps

# Disconnect
sim --host localhost --port 7600 disconnect
```

### Run the full suite

```bash
# Connect once, run all 10 tutorials sequentially
sim --host localhost --port 7600 connect --solver openfoam

for f in snippets/*.sh; do
    label=$(basename "$f" .sh)
    echo ">>> Running $label"
    sim --host localhost --port 7600 exec --file "$f" --label "$label"
done

sim --host localhost --port 7600 disconnect
```

## Test Results

| # | Test | Solver | Physics | Status | Time | Notes |
|---|------|--------|---------|--------|------|-------|
| 1 | Cavity | icoFoam | Incompressible laminar | **PASS** | 0.3s | Classic lid-driven cavity |
| 2 | Backward Facing Step | simpleFoam | RANS k-omega SST | **PASS** | 70.4s | 2000 iterations with post-processing |
| 3 | NonNewton OffsetCylinder | nonNewtonianIcoFoam | Non-Newtonian | **PASS** | 6.1s | Shear-thinning flow around cylinder |
| 4 | DamBreak | interFoam | VOF multiphase | **PASS** | 7.5s | Free surface tracking |
| 5 | Cylinder2D | pimpleFoam | Laminar external | **PASS** | 18.7s | snappyHexMesh + solver |
| 6 | BuoyantCavity | buoyantSimpleFoam | Natural convection | **PASS** | 170.3s | 1000 iterations, k-omega |
| 7 | HIT DNS 16^3 | dnsFoam | DNS turbulence | **PASS** | 6.3s | boxTurb initial field + solver |
| 8 | SquareBend | simpleFoam | Incompressible RANS | **PASS** | 21.8s | 3D pipe bend, 100 iterations |
| 9 | DLR-A Combustion | reactingFoam | Turbulent diffusion flame | **PASS** | 9.8s | RANS with chemistry, 100 iterations |
| 10 | Cavity RANS | pisoFoam | RANS k-epsilon | **PASS** | 25.6s | Turbulent cavity with norm output |

## Snippets

| Step | File | Solver | Description |
|------|------|--------|-------------|
| 1 | `01_cavity.sh` | icoFoam | Lid-driven cavity — simplest incompressible case |
| 2 | `02_backward_step.sh` | simpleFoam | Backward facing step — steady RANS |
| 3 | `03_non_newtonian.sh` | nonNewtonianIcoFoam | Offset cylinder — viscoelastic fluid |
| 4 | `04_dambreak.sh` | interFoam | Dam break — VOF free surface |
| 5 | `05_cylinder2d.sh` | pimpleFoam | Cylinder 2D — snappyHexMesh + transient |
| 6 | `06_buoyant_cavity.sh` | buoyantSimpleFoam | Buoyant cavity — natural convection |
| 7 | `07_hit_dns.sh` | dnsFoam | HIT — DNS forced turbulence |
| 8 | `08_square_bend.sh` | simpleFoam | Square bend — 3D pipe RANS |
| 9 | `09_combustion.sh` | reactingFoam | DLR-A flame — combustion |
| 10 | `10_cavity_rans.sh` | pisoFoam | Cavity RANS — turbulent lid-driven |

## How it works

### The `#!openfoam` shebang convention

Every snippet starts with `#!openfoam`. When the sim server receives code with
this prefix, it:

1. Sources the OpenFOAM environment (`/etc/bashrc` from `$WM_PROJECT_DIR`)
2. Executes the remaining lines as a bash script
3. Captures stdout, stderr, exit code, and elapsed time
4. Returns a JSON response with all fields

Without the shebang, sim would try to execute the code as Python.

### Common patterns in snippets

```bash
#!openfoam
set -e                        # Stop on first error
cd /tmp && rm -rf mycase      # Clean workspace
cp -r $FOAM_TUTORIALS/... mycase  # Copy tutorial
cd mycase
cp -r 0.orig 0               # Many tutorials need this!

blockMesh 2>&1 | tail -5     # Generate mesh (pipe to tail for clean output)
<solver> 2>&1 | tail -10     # Run solver

echo '{"ok": true, ...}'     # JSON on last line for parse_output()
```

### Key gotchas

1. **`0.orig` → `0` copy**: Most OpenFOAM tutorials ship with `0.orig/` instead
   of `0/`. You must `cp -r 0.orig 0` before running the solver, otherwise you
   get `cannot find file "0/p"`.

2. **Function objects**: Some tutorials include post-processing `functions {}` in
   `controlDict` that reference sample surfaces. These may fail in batch mode.
   Fix: `sed -i "/^functions/,$ d" system/controlDict`

3. **LES is expensive**: PitzDaily LES with deltaT=1e-5 and 10,000 steps takes
   hours on a single core. For testing, reduce `endTime` or skip LES cases.

4. **Output convention**: Print a JSON object as the last stdout line.
   `sim.runner.parse_output()` scans stdout in reverse for the first valid JSON.

### Network setup

OpenFOAM typically runs on Linux, but your agent (Claude, GPT, etc.) may be on
Windows or macOS. The sim architecture handles this via HTTP:

```
Agent (any OS) → sim OpenFOAMDriver → HTTP → sim serve (Linux) → OpenFOAM
```

If the Linux server is behind a firewall that blocks non-standard ports:
```bash
# SSH tunnel: local:7600 → remote:8080
ssh -p <ssh-port> -L 7600:localhost:8080 user@linux-host
```

Then all sim commands target `localhost:7600`.

## Environment

| Component | Version |
|-----------|---------|
| OpenFOAM | v2206 (ESI/OpenCFD) |
| sim-cli | 0.2.0+ |
| Python | 3.10+ |
| OS (server) | Ubuntu 22.04 |

## Source YAML prompts

The test cases are derived from [MetaOpenFOAM](https://github.com/) prompt
definitions in `/data/Chenyx/MetaOpenFOAM3/inputs/*.yaml`. Each YAML contains
a `usr_requirement` field describing the simulation in natural language:

| YAML | Prompt | Mapped Tutorial |
|------|--------|-----------------|
| `Cavity.yaml` | "incompressible lid driven cavity flow...top wall at 1 m/s" | icoFoam/cavity |
| `Backward_facing_step.yaml` | "RANS simulation of backward facing step" | simpleFoam/backwardFacingStep2D |
| `DamBreak.yaml` | "laminar multiphase simulation using interFoam" | interFoam/damBreak |
| `Cylinder.yaml` | "flow around a cylinder with inlet velocity 1 m/s" | pimpleFoam/cylinder2D |
| `BuoyantCavity.yaml` | "natural convection...temperature difference of 20K" | buoyantSimpleFoam/buoyantCavity |
| `HIT.yaml` | "DNS of incompressible forcing HIT with Grid 32^3" | dnsFoam/boxTurb16 |
| `SquareBendLiq.yaml` | "compressible squareBendLiq using rhoSimpleFoam" | simpleFoam/squareBend |
| `Combustion.yaml` | "2D laminar counterflow flame using reactingFoam" | reactingFoam/DLR_A_LTS |
| `Cavity_RANS.yaml` | "2D RANS cavity using pisoFoam with RNGkEpsilon" | pisoFoam/RAS/cavity |

## Key Differences from Fluent/COMSOL/ANSA Cookbooks

| Aspect | Fluent/COMSOL | ANSA | OpenFOAM |
|--------|---------------|------|----------|
| Execution model | Persistent session (Python snippets) | One-shot batch | Remote shell scripts via HTTP |
| Solver location | Same machine as sim | Same machine | Remote Linux server |
| Script language | Python | Python | Bash (`#!openfoam`) |
| Network | Local or LAN | Local | HTTP over SSH tunnel |
| Mesh tool | Built-in | Built-in | blockMesh / snappyHexMesh |
| Session state | In-memory (solver object) | None (batch) | Filesystem (`/tmp/sim_*`) |

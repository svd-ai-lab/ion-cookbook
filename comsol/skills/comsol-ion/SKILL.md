# COMSOL Simulation via ion

## Scope

Control protocol for running COMSOL Multiphysics simulations through the ion runtime. Covers connecting to COMSOL, building models via the Java API (through JPype), solving, and post-processing.

This is NOT a general COMSOL Java API reference. It defines how an agent should use `ion connect/exec/inspect/disconnect` to drive COMSOL simulations with human oversight.

## When to Use

- Task involves COMSOL simulation + ion CLI
- Agent needs to build geometry, assign materials, set physics/BCs, mesh, solve, extract results
- Human wants to watch the simulation in the COMSOL GUI (human-in-the-loop)

## Hard Constraints

- **Never** launch COMSOL server directly in snippets — `ion connect` handles this
- **Always** use incremental execution (one step per `ion exec`) so human can verify each step
- **Always** set `_result` dict at the end of every snippet for structured output
- The `model` and `ModelUtil` objects are injected into the exec namespace — don't import them
- Java arrays must use `jpype.JArray(jpype.JDouble)([...])` or `jpype.JArray(jpype.JInt)([...])`
- After modifying the model, remind the human to **Import Application from Server** in the GUI

## Agent Workflow

### Step 0: Parse task and identify inputs

Classify inputs:
- **Category A (MUST ASK)**: geometry dimensions, material properties, physics type, boundary conditions, acceptance criteria
- **Category B (MAY DEFAULT)**: mesh size (default: fine/4), solver type (default: stationary), ui_mode (default: gui)
- **Category C (INFER)**: boundary numbers (from geometry), coordinate system

### Step 1: Connect

```bash
# Client-server mode (separate GUI client, manual import needed)
ion --host <host> connect --solver comsol --ui-mode gui

# Standalone mode (simpler, no server subprocess, save .mph for visual check)
ion --host <host> connect --solver comsol --ui-mode standalone
```

Verify: `ion --host <host> inspect session.summary` shows `connected: true`.

### Step 2: Build model incrementally

Each step is a separate `ion exec` call. **After each step, run the corresponding verification utility** (see Verification Utilities section) before proceeding. Never skip verification — image export is broken on Windows, so programmatic checks are the only way to catch issues early.

Typical sequence:
1. Create component and geometry → verify domain count, volume, bounding box, no voids
2. Assign materials → verify all domains assigned, no orphans
3. Add physics and boundary conditions → verify each BC has selected entities
4. Generate mesh → verify element count and min quality > 0
5. Create study and solve → verify convergence, check min/max temperature
6. Create result plots and extract data

### Step 3: Save and verify

After major steps, save the model for human inspection:
```python
model.save("C:/Users/jiwei/Desktop/<model_name>.mph")
```

For client-server mode, tell the human to:
1. **File > COMSOL Multiphysics Server > Import Application from Server**
2. Click the relevant node (Geometry, Mesh, Results) to render

### Step 4: Extract results

```python
# Example: extract min/max temperature
import jpype
derived = model.result().numerical().create("gev1", "EvalGlobal")
derived.setIndex("expr", "minop1(T)", 0)
derived.setIndex("expr", "maxop1(T)", 1)
# ... evaluate and set _result
```

### Step 5: Disconnect

```bash
ion --host <host> disconnect
```

## Snippet Conventions

Every snippet must:
- Use injected `model` and `ModelUtil` objects (never import them)
- Import `jpype` if Java arrays are needed
- Set `_result = {...}` with structured output
- Be focused on a single step (not the whole workflow)

```python
import jpype

# [one simulation step]
# ...

_result = {
    "step": "description",
    "key_metric": value,
    "status": "ok"
}
```

## COMSOL Java API Quick Reference

### Geometry
```python
comp = model.component().create("comp1", True)
geom = model.component("comp1").geom().create("geom1", 3)  # 3D
blk = geom.create("blk1", "Block")
blk.set("size", jpype.JArray(jpype.JDouble)([1.0, 0.5, 0.2]))
geom.run()
```

### Materials
```python
mat = model.component("comp1").material().create("mat1", "Common")
mat.propertyGroup("def").set("thermalconductivity", jpype.JArray(jpype.JString)(["237[W/(m*K)]"]))
mat.selection().all()
```

### Physics (Heat Transfer)
```python
ht = model.component("comp1").physics().create("ht", "HeatTransfer", "geom1")
temp1 = ht.create("temp1", "TemperatureBoundary", 2)
temp1.selection().set(jpype.JArray(jpype.JInt)([1]))
temp1.set("T0", "373[K]")
```

### Mesh
```python
mesh = model.component("comp1").mesh().create("mesh1")
mesh.autoMeshSize(4)  # 1=extremely fine, 9=extremely coarse
mesh.run()
```

### Study and Solve
```python
std = model.study().create("std1")
std.create("stat", "Stationary")
model.sol().create("sol1")
model.sol("sol1").createAutoSequence("std1")
model.sol("sol1").runAll()
```

### Results
```python
pg = model.result().create("pg1", "PlotGroup3D")
surf = pg.create("surf1", "Surface")
surf.set("expr", "T")
surf.set("colortable", "ThermalLight")
pg.run()
```

## Verification Utilities

Since image export is blank on Windows, the agent must verify each step programmatically. Run these checks after every `ion exec` step.

### After Geometry

```python
geom = model.component("comp1").geom("geom1")
ndom = geom.getNDomains()
nbnd = geom.getNBoundaries()
vol  = geom.measureFinal().getVolume()       # total volume
bbox = geom.measureFinal().getBoundingBox()   # [xmin,ymin,zmin,xmax,ymax,zmax]
voids = geom.measureFinal().getNFiniteVoids() # should be 0
geom.check()                                 # returns None if valid

# Sanity: compare volume and domain count against expectations
```

### After Materials

```python
# Verify every domain has a material (no orphans)
assigned = set()
for tag in list(comp.material().tags()):
    mat = comp.material(tag)
    doms = list(mat.selection().entities(jpype.JInt(3)))
    print(f"{mat.label()} ({tag}): {len(doms)} domains")
    assigned.update(doms)
total = geom.getNDomains()
missing = set(range(1, total + 1)) - assigned
assert not missing, f"Unassigned domains: {missing}"
```

### After Physics

```python
# Verify each BC has at least one selected entity
ht = comp.physics("ht")
for tag in list(ht.feature().tags()):
    feat = ht.feature(tag)
    try:
        n = len(list(feat.selection().entities(jpype.JInt(2))))
        print(f"{feat.label()} ({tag}): {n} boundaries")
    except Exception:
        pass  # some features (e.g. init) have no selection
```

### After Mesh

```python
mesh = comp.mesh("mesh1")
stat = mesh.stat()
nelem  = stat.getNumElem()           # total element count
qual   = stat.getMinQuality()         # min element quality (>0 required)
print(f"Elements: {nelem}, min quality: {qual:.4f}")
assert qual > 0, "Mesh has inverted elements"
```

### After Solve

```python
# Check convergence + temperature range
info = model.sol("sol1").getSolverSequence("1")
# Extract min/max of solution field
import jpype
JD = jpype.JArray(jpype.JDouble)
T_min = model.result().numerical().create("ev_min", "MinVolume")
T_min.selection().all()
T_min.set("expr", "T")
val_min = T_min.getReal()[0][0]
T_max = model.result().numerical().create("ev_max", "MaxVolume")
T_max.selection().all()
T_max.set("expr", "T")
val_max = T_max.getReal()[0][0]
print(f"T range: {val_min - 273.15:.1f} to {val_max - 273.15:.1f} degC")
# Clean up
model.result().numerical().remove("ev_min")
model.result().numerical().remove("ev_max")
```

### Saving for Manual Inspection

When programmatic checks pass but visual confirmation is needed, save the `.mph` file:

```python
model.save("C:/Users/jiwei/Desktop/model_name.mph")
```

The human can open it in COMSOL Desktop to visually verify geometry, mesh, and results.

## Known Limitations

- **No auto-refresh in GUI**: in client-server mode, human must Import from Server after each agent modification
- **Image export is blank on Windows**: both standalone and client-server modes produce blank PNGs from the Java API. Use `model.save()` + open in COMSOL Desktop, or `ion screenshot` (desktop capture) for visual verification
- **Standalone mode has no GUI window**: `initStandalone(True)` enables the rendering engine but does not open a COMSOL Desktop window. Save `.mph` files for manual inspection
- **JVM singleton**: restart `ion serve` between sessions if connection state goes stale
- **First-time setup**: `comsolmphserver -login force` must be run once to set credentials

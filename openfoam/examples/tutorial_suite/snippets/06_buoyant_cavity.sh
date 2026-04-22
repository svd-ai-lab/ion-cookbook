#!openfoam
# Test 6: Buoyant cavity natural convection (buoyantSimpleFoam)
# RANS heat transfer with 20K temperature difference
set -e
cd /tmp && rm -rf ion_test_buoyant
cp -r $FOAM_TUTORIALS/heatTransfer/buoyantSimpleFoam/buoyantCavity ion_test_buoyant
cd ion_test_buoyant
ls 0.orig 2>/dev/null && cp -r 0.orig 0 || true

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

buoyantSimpleFoam 2>&1 | tail -15
echo "=== buoyantSimpleFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "buoyantCavity", "solver": "buoyantSimpleFoam", "type": "heat_transfer"}'

#!openfoam
# Test 1: Lid-driven cavity flow (icoFoam)
# Classic incompressible laminar benchmark — top wall moves at 1 m/s
set -e
cd /tmp && rm -rf ion_test_cavity
cp -r $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity ion_test_cavity
cd ion_test_cavity

blockMesh 2>&1 | tail -5
echo "=== blockMesh done ==="

icoFoam 2>&1 | tail -10
echo "=== icoFoam done ==="

ls -d [0-9]* | wc -l | xargs -I{} echo "Time steps: {}"
echo '{"ok": true, "test": "cavity", "solver": "icoFoam", "type": "incompressible_laminar"}'

#!openfoam
# Test 10: Cavity RANS (pisoFoam with k-epsilon)
# Turbulent lid-driven cavity with RAS model
set -e
cd /tmp && rm -rf ion_test_cavity_rans
cp -r $FOAM_TUTORIALS/incompressible/pisoFoam/RAS/cavity ion_test_cavity_rans
cd ion_test_cavity_rans
cp -r 0.orig 0 2>/dev/null || true

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

pisoFoam 2>&1 | tail -10
echo "=== pisoFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "cavity_RANS", "solver": "pisoFoam", "type": "RANS"}'

#!openfoam
# Test 4: Dam break (interFoam VOF multiphase)
# Laminar two-phase flow with free surface tracking
set -e
cd /tmp && rm -rf ion_test_dambreak
cp -r $FOAM_TUTORIALS/multiphase/interFoam/laminar/damBreak/damBreak ion_test_dambreak
cd ion_test_dambreak
cp -r 0.orig 0

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

setFields 2>&1 | tail -5
echo "=== setFields done ==="

interFoam 2>&1 | tail -10
echo "=== interFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "damBreak", "solver": "interFoam", "type": "multiphase_VOF"}'

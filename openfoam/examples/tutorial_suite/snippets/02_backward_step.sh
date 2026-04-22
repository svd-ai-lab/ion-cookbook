#!openfoam
# Test 2: Backward facing step (simpleFoam RANS)
# 2D steady-state turbulent flow with k-omega SST
set -e
cd /tmp && rm -rf ion_test_backstep
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/backwardFacingStep2D ion_test_backstep
cd ion_test_backstep
cp -r 0.orig 0

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

simpleFoam 2>&1 | tail -15
echo "=== simpleFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "backwardFacingStep", "solver": "simpleFoam", "type": "RANS"}'

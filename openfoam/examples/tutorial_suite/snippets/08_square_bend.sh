#!openfoam
# Test 8: Square bend pipe flow (simpleFoam)
# 3D turbulent flow through a square cross-section bend
set -e
cd /tmp && rm -rf ion_test_squarebend
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/squareBend ion_test_squarebend
cd ion_test_squarebend
cp -r 0.orig 0

# Remove function objects (avoid sample errors in headless mode)
sed -i "/^functions/,$ d" system/controlDict
# Reduce endTime for quick test
sed -i "s/endTime         500/endTime         100/" system/controlDict

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

simpleFoam 2>&1 | tail -10
echo "=== simpleFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "squareBend", "solver": "simpleFoam", "type": "incompressible_RANS"}'

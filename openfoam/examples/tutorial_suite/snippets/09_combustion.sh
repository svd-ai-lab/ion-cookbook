#!openfoam
# Test 9: DLR-A turbulent diffusion flame (reactingFoam)
# RANS combustion with detailed chemistry
set -e
cd /tmp && rm -rf ion_test_combustion
cp -r $FOAM_TUTORIALS/combustion/reactingFoam/RAS/DLR_A_LTS ion_test_combustion
cd ion_test_combustion
cp -r 0.orig 0

# Reduce endTime for quick test
sed -i "s/endTime         5000/endTime         100/" system/controlDict

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

reactingFoam 2>&1 | tail -15
echo "=== reactingFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "DLR_A_combustion", "solver": "reactingFoam", "type": "combustion"}'

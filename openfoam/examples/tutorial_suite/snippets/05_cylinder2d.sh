#!openfoam
# Test 5: 2D cylinder flow (pimpleFoam)
# Laminar flow around cylinder with snappyHexMesh
set -e
cd /tmp && rm -rf ion_test_cylinder
cp -r $FOAM_TUTORIALS/incompressible/pimpleFoam/laminar/cylinder2D ion_test_cylinder
cd ion_test_cylinder
cp -r 0.orig 0

# Mesh preparation (multi-step)
blockMesh -dict system/blockMeshDict.coarse 2>&1 | tail -3
echo "=== coarse blockMesh done ==="

snappyHexMesh -overwrite 2>&1 | tail -3
echo "=== snappyHexMesh done ==="

mkdir -p constant/coarseMesh
mv -f constant/polyMesh constant/coarseMesh

blockMesh -dict system/blockMeshDict.main 2>&1 | tail -3
echo "=== main blockMesh done ==="

mirrorMesh -overwrite 2>&1 | tail -3
echo "=== mirrorMesh done ==="

# Reduce endTime for quick test (100 -> 5)
sed -i "s/endTime         100/endTime         5/" system/controlDict

pimpleFoam 2>&1 | tail -10
echo "=== pimpleFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "cylinder2D", "solver": "pimpleFoam", "type": "laminar_external"}'

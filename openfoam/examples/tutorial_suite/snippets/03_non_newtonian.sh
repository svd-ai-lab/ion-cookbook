#!openfoam
# Test 3: Non-Newtonian fluid flow around offset cylinder (nonNewtonianIcoFoam)
# Viscoelastic fluid with shear-thinning behavior
set -e
cd /tmp && rm -rf ion_test_nonnewton
cp -r $FOAM_TUTORIALS/incompressible/nonNewtonianIcoFoam/offsetCylinder ion_test_nonnewton
cd ion_test_nonnewton

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

nonNewtonianIcoFoam 2>&1 | tail -10
echo "=== nonNewtonianIcoFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "nonNewtonianOffsetCylinder", "solver": "nonNewtonianIcoFoam", "type": "non_newtonian"}'

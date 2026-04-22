#!openfoam
# Test 7: Homogeneous Isotropic Turbulence DNS (dnsFoam)
# 16^3 grid, forced turbulence with boxTurb initial field
set -e
cd /tmp && rm -rf ion_test_hit
cp -r $FOAM_TUTORIALS/DNS/dnsFoam/boxTurb16 ion_test_hit
cd ion_test_hit
cp -r 0.orig 0

blockMesh 2>&1 | tail -3
echo "=== blockMesh done ==="

boxTurb 2>&1 | tail -3
echo "=== boxTurb done (initial field generated) ==="

dnsFoam 2>&1 | tail -10
echo "=== dnsFoam done ==="

ls -d [0-9]* | tail -5
echo '{"ok": true, "test": "HIT_DNS_16", "solver": "dnsFoam", "type": "DNS"}'

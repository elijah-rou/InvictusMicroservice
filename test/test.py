# Unit tests for functions of the InvictusMicroservice service
# Test for square if odd
import sys
sys.path.append("src/")

import src.InvictusService as iserv 
service = iserv.InvictusService()

def test_odd_square():
    assert service.odd_square(0) == 0
    assert service.odd_square(1) == 1
    assert service.odd_square(2) == 2
    assert service.odd_square(3) == 9

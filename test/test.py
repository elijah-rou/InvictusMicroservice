# Unit tests for functions of the InvictusMicroservice service
# Test for square if odd
import sys
sys.path.append("src/")

from InvictusService import InvictusService
service = InvictusService()

def test_odd_square():
    assert service.odd_square(0) == 0
    assert service.odd_square(1) == 1
    assert service.odd_square(2) == 2
    assert service.odd_square(3) == 9

def test_odd_square_list():
    x = [1,2,3,4,5]
    assert list(map(service.odd_square, x)) == [1,2,9,4,25]

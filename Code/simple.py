def addtwo(x):
    """
        Add 2 to x
    """
    return x+1

def test_addtwo_inside():
    """
        Test addtwo
        """
    assert( addtwo(3)==5)


x = addtwo(5)

print(x)

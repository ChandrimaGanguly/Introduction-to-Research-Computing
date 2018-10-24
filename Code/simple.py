def addtwo(x):
    """
        Add 2 to x
    """
    return x+1

def add02(x):
    """
        Add 0.3 to x
        """
    return x+0.2

def test_addtwo_inside():
    """
        Test addtwo
        """
    assert( addtwo(3)==5)


x = 7

y = addtwo(x)

print(y)

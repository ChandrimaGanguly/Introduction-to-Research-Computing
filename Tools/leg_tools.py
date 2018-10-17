def create_vectors(lmax):
    lmax += 1
    lvec = [l for l in range(lmax)]
    xmax = lmax*10
    xvec = [(2e0*x/(xmax-1))-1 for x in range(xmax)]
    return xvec, lvec

def create_legendre(xvec,lvec):
    legendre = []
    for x in xvec:
        pt = [1,x]
        for i in lvec[2:]:
            y = ((2*i-1)/(i))*pt[i-1]*x - ((i-1)/i)*pt[i-2]
            pt.append(y)
        legendre.append(pt)
    return legendre

def integrate(l1,l2,l3,xvec,legendre):
    y1 = legendre[0][l1]*legendre[0][l2]*legendre[0][l3]
    x1 = xvec[0]
    int = 0e0
    for i, x in enumerate(xvec[1:]):
        y2 = legendre[i][l1]*legendre[i][l2]*legendre[i][l3]
        x2 = x
        int += 0.5*(y2+y1)*(x2-x1)
        y1 = y2
        x1 = x2
    return int
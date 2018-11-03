"""
    This Module contains functions to create arrays of common polynomials
    
    Contains:
    ----------------------------------------
    legendre_array
    Creates an array of the legendre polynomials
    chebyshev_array
    Creates an array of the chebyshev polynomials
    ----------------------------------------
    
    
    All functions take two arguments:
    ----------------------------------------
    lmax
    the maximum dregree to include
    X
    The array of X points to calculate the polynomials on
    ----------------------------------------
    
    Calculation is done by recursion
    
    Written by James Fergusson: J.Fergusson@DAMTP.cam.ac.uk
    """

import numpy as np

def legendre_array(X,lmax):
    """
        Calculates an array of Legendre polynomials
        with size: len(X) by lmax
        
        Parameters
        ----------
        lmax: int
        the maximum degree, must be positive
        X: array(float)
        points to calculate the polynomials on
        
        Returns
        ----------
        array(float)
        A table of the Legendre polynomials
        """
    
    # Initilise the array
    P = np.zeros((lmax,len(X)), dtype='float')
    
    # Set P_0 and P_l
    P[0,:]=1.0
    P[1,:]=X
    
    # Calculate the rest via iteration
    for n in range(2,lmax):
        P[n,:] = ((2*n-1)*X*P[n-1,:] - (n-1)*P[n-2,:])/n
    
    # return the array of Legendre polynomials
    return P

def chebyshev_array(X,lmax):
    """
        Calculates an array of Chebyshev polynomials
        with size: len(X) by lmax
        
        Parameters
        ----------
        lmax: int
        the maximum degree, must be positive
        X: array(float)
        points to calculate the polynomials on
        
        Returns
        ----------
        array(float)
        A table of the Chebyshev polynomials
        """
    
    # Initilise the array
    C = np.zeros((lmax,len(X)), dtype='float')
    
    # Set C_0 and C_l
    C[0,:]=1.0
    C[1,:]=X
    
    # Calculate the rest via iteration
    for n in range(2,lmax):
        C[n,:] = 2*X*C[n-1,:] - C[n-2,:]
    
    # return the array of Chebyshev polynomials
    return C


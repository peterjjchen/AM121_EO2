"""
polygon.py - Generate regular polygon coordinates

Adj = polygon(N, d, rad)
Generates the regular polygon {N/d} with vertices on a circle of radius 'rad'.
The output 'Adj' is an Nx2 matrix with point coordinates.

Modified for use in graphvisualizer.py
Adj now returns N by 2 matrix with point coordinates.

Original MATLAB version by Nima Moshtagh (nima@seas.upenn.edu)
Python translation for AM 121 Optimization
"""

import numpy as np


def polygon(N, d, rad):
    """
    Generate coordinates for a regular polygon.
    
    Parameters:
    -----------
    N : int
        Number of vertices
    d : int
        Step size (must be <= N)
    rad : float
        Radius of the circle
        
    Returns:
    --------
    Adj : numpy.ndarray
        Nx2 matrix with [X, Y] coordinates
    """
    # Check the values of 'd' and 'N'. They must be integers.
    if not isinstance(d, (int, np.integer)) or not isinstance(N, (int, np.integer)):
        raise ValueError('Input parameters N and d must be integers!')
    if d > N:
        raise ValueError('d must be less than or equal to N.')
    
    # Generate the vertices
    theta = np.linspace(0, 2 * np.pi, N + 1)
    X = rad * np.cos(theta)
    Y = rad * np.sin(theta)
    
    # Return Nx2 matrix (exclude the last point which is duplicate of first)
    Adj = np.column_stack([X[:N], Y[:N]])
    return Adj


if __name__ == '__main__':
    # Test example
    Adj = polygon(9, 4, 1)
    print("Polygon coordinates (9 vertices, step 4, radius 1):")
    print(Adj)


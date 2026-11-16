"""
gplotd.py - Plot a Directed Graph

GPLOTD(A,XY) Plots the Directed Graph represented by adjacency
matrix A and points xy using the default style.

Modified for use in graphvisualizer.py
Now also returns all XY vectors for further use in plotting directed arrows.

Original MATLAB version by Joseph Kirk (jdkirk630@gmail.com)
Python translation for AM 121 Optimization
"""

import numpy as np
import matplotlib.pyplot as plt


def gplotd(A, xy, **kwargs):
    """
    Plot a directed graph and return edge coordinates.
    
    Parameters:
    -----------
    A : numpy.ndarray
        NxN adjacency matrix, where A[i,j] is nonzero if and only if
        there is an edge between points i and j
    xy : numpy.ndarray
        Nx2 matrix of x/y coordinates
    **kwargs : dict
        Additional matplotlib plot parameters
        
    Returns:
    --------
    dxu, dyu : numpy.ndarray
        XY vectors for directed edges (smaller to larger vertex ID)
    dxl, dyl : numpy.ndarray
        XY vectors for directed edges (larger to smaller vertex ID)
    ux, uy : numpy.ndarray
        XY vectors for undirected (2-way) edges
    """
    # Process inputs
    A = np.array(A)
    xy = np.array(xy)
    
    nr, nc = A.shape
    n, dim = xy.shape
    
    if n == 0 or nr != n or nc != n or dim < 2:
        raise ValueError('Invalid input dimensions. A must be NxN and xy must be Nx2.')
    
    # Parse the adjacency matrix
    A = A.astype(bool).astype(float)
    iA = np.diag(np.diag(A))  # self-connecting edges
    dA = A * (1 - A.T)  # directed edges (1-way)
    dAu = np.triu(dA, 1)  # directed edges (1-way, sm2lg)
    dAl = np.tril(dA, -1)  # directed edges (1-way, lg2sm)
    uA = A - dA - iA  # undirected edges (2-way)
    
    # Make NaN-separated XY vectors
    ix, iy = makeXY(iA, xy)
    ux, uy = makeXY(np.tril(uA, 0), xy)
    dxu, dyu = makeXY(dAu, xy)
    dxl, dyl = makeXY(dAl, xy)
    
    # Plot the graph (only if we're not being called from graphvisualizer)
    # The original MATLAB gplotd plots, but graphvisualizer doesn't use that plot
    # We'll skip plotting here and let the caller handle it
    # Uncomment below if you want gplotd to plot directly:
    # plt.figure()
    # if not np.all(np.isnan(ux)):
    #     plt.plot(ux, uy, 'k-', **kwargs)
    # if not np.all(np.isnan(dxu)):
    #     plt.plot(dxu, dyu, 'k-', **kwargs)
    # if not np.all(np.isnan(dxl)):
    #     plt.plot(dxl, dyl, 'k-', **kwargs)
    # if not np.all(np.isnan(ix)):
    #     plt.plot(ix, iy, 'o', color=[0.6, 0, 1], **kwargs)
    # plt.plot(xy[:, 0], xy[:, 1], 'k.')
    
    return dxu, dyu, dxl, dyl, ux, uy


def makeXY(A, xy):
    """
    Create NaN-separated XY vectors for edges.
    
    Parameters:
    -----------
    A : numpy.ndarray
        Adjacency matrix subset
    xy : numpy.ndarray
        Nx2 coordinate matrix
        
    Returns:
    --------
    x, y : numpy.ndarray
        NaN-separated coordinate vectors
    """
    if np.any(A):
        J, I = np.where(A.T)
        m = len(I)
        xmat = np.column_stack([xy[I, 0], xy[J, 0], np.full(m, np.nan)]).T
        ymat = np.column_stack([xy[I, 1], xy[J, 1], np.full(m, np.nan)]).T
        x = xmat.flatten(order='F')  # column-major, like MATLAB's xmat(:)
        y = ymat.flatten(order='F')
    else:
        x = np.full(3, np.nan)  # one NaN "edge" keeps start/stop slices aligned
        y = np.full(3, np.nan)
    return x, y


if __name__ == '__main__':
    # Test example
    n = 9
    t = 2 * np.pi / n * np.arange(n)
    A = np.round(np.random.rand(n, n))
    xy = 10 * np.column_stack([np.cos(t), np.sin(t)])
    
    dxu, dyu, dxl, dyl, ux, uy = gplotd(A, xy)
    plt.title('Directed Graph Test')
    plt.axis('equal')
    plt.show()


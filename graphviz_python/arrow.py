"""
arrow.py - Draw arrows on a plot

Simplified Python version of the MATLAB arrow.m function.
Uses matplotlib's FancyArrowPatch for drawing arrows.

Original MATLAB version by Dr. Erik A. Johnson
Python translation for AM 121 Optimization
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def arrow(start, stop, BaseAngle=60, **kwargs):
    """
    Draw arrows from start points to stop points.
    
    Parameters:
    -----------
    start : numpy.ndarray or list
        Nx2 array of starting points [x, y]
    stop : numpy.ndarray or list
        Nx2 array of ending points [x, y]
    BaseAngle : float, optional
        Base angle in degrees (default: 60)
    **kwargs : dict
        Additional matplotlib arrow properties
        (e.g., color, linewidth, alpha, etc.)
    """
    start = np.array(start)
    stop = np.array(stop)
    
    # Ensure 2D arrays
    if start.ndim == 1:
        start = start.reshape(1, -1)
    if stop.ndim == 1:
        stop = stop.reshape(1, -1)
    
    if start.shape[0] != stop.shape[0]:
        raise ValueError('Start and stop must have the same number of rows')
    
    # Default arrow properties
    arrow_props = {
        'arrowstyle': '->',
        'mutation_scale': 20,
        'linewidth': 1.5,
        'color': 'black',
        **kwargs
    }
    
    # Draw each arrow
    for i in range(start.shape[0]):
        # Skip if start or stop contains NaN
        if np.any(np.isnan(start[i])) or np.any(np.isnan(stop[i])):
            continue
        
        # Create arrow
        arrow = FancyArrowPatch(
            (start[i, 0], start[i, 1]),
            (stop[i, 0], stop[i, 1]),
            **arrow_props
        )
        plt.gca().add_patch(arrow)
    
    return


if __name__ == '__main__':
    # Test example
    fig, ax = plt.subplots()
    
    start = np.array([[0, 0], [1, 1], [2, 0]])
    stop = np.array([[1, 1], [2, 2], [3, 1]])
    
    arrow(start, stop, BaseAngle=60, color='blue', linewidth=2)
    
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    plt.title('Arrow Test')
    plt.show()


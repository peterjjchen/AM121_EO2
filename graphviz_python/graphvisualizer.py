"""
graphvisualizer.py - Kidney Exchange Visualization Script

Applied Math/Engineering Sciences 121
Extreme Optimization 2: Kidney Exchange
Visualization script

Python translation of the MATLAB graphvisualizer.m script.
"""

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Import local modules
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from polygon import polygon
from gplotd import gplotd
from arrow import arrow


def load_matrix_file(filepath):
    """
    Load a matrix from a text file.
    
    Parameters:
    -----------
    filepath : str
        Path to the file
        
    Returns:
    --------
    matrix : numpy.ndarray
        Loaded matrix
    """
    try:
        data = np.loadtxt(filepath)
        return data
    except Exception as e:
        raise ValueError(f'Error loading file {filepath}: {e}')


def select_file(title, filetypes, initialdir=None):
    """
    Open a file dialog to select a file.
    
    Parameters:
    -----------
    title : str
        Dialog title
    filetypes : list of tuples
        File type filters, e.g., [('Text files', '*.txt'), ('All files', '*.*')]
    initialdir : str, optional
        Initial directory
        
    Returns:
    --------
    filepath : str or None
        Selected file path, or None if cancelled
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    filepath = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes,
        initialdir=initialdir
    )
    
    root.destroy()
    return filepath if filepath else None


def main():
    """Main visualization function."""
    # Number of patient-donor pairs
    N = 50
    
    # Try to get N from command line argument
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
        except ValueError:
            print(f"Warning: Invalid N value '{sys.argv[1]}', using default N={N}")
    
    print(f"Kidney Exchange Visualizer - N={N} pairs")
    print("=" * 50)
    
    # Load exchange output from AMPL
    print("\n1. Select exchange output file (usually *.out or *.txt)")
    exchange_file = select_file(
        'Please select the exchange output file from AMPL, usually *.out',
        [('Output files', '*.out'), ('Text files', '*.txt'), ('All files', '*.*')]
    )
    
    if not exchange_file:
        print("Error: Exchange output file selection cancelled.")
        return
    
    try:
        exchange = load_matrix_file(exchange_file)
        print(f"   Loaded: {exchange_file}")
    except Exception as e:
        print(f"Error loading exchange file: {e}")
        return
    
    # Load compatibility graph
    initialdir = os.path.dirname(exchange_file)
    print("\n2. Select compatibility data file (usually *_raw.txt)")
    compat_file = select_file(
        'Please select the compatibility data, usually *_raw.txt',
        [('Text files', '*.txt'), ('Output files', '*.out'), ('All files', '*.*')],
        initialdir=initialdir
    )
    
    if not compat_file:
        print("Error: Compatibility file selection cancelled.")
        return
    
    try:
        compat = load_matrix_file(compat_file)
        print(f"   Loaded: {compat_file}")
    except Exception as e:
        print(f"Error loading compatibility file: {e}")
        return
    
    # Check dimensions
    if compat.shape[0] != N or compat.shape[1] != N:
        print(f"Warning: Compatibility matrix shape {compat.shape} doesn't match N={N}")
        N = compat.shape[0]
        print(f"   Using N={N} from compatibility matrix")
    
    if exchange.shape[0] != N or exchange.shape[1] != N:
        print(f"Error: Exchange matrix shape {exchange.shape} doesn't match N={N}")
        return
    
    print(f"\n3. Generating visualization for N={N} pairs...")
    
    # Generate ring of points
    Adj = polygon(N, 2, 200)
    
    # Process both exchange and compatibility matrices
    # Exchange output shows the optimal cycles found (Cycles)
    # Compatibility graph shows all possible matches (Matches)
    matrices = [exchange, compat]
    titles = ['Cycles', 'Matches']
    
    # Extract problem number from exchange filename
    exchange_filename = os.path.basename(exchange_file)
    problem_num = "1"  # default
    if '_' in exchange_filename:
        parts = exchange_filename.split('_')
        if len(parts) >= 1:
            problem_num = parts[0]
    
    for idx, (matrix, title) in enumerate(zip(matrices, titles)):
        print(f"   Plotting {title}...")
        
        # Get edge coordinates
        dxu, dyu, dxl, dyl, ux, uy = gplotd(matrix, Adj)
        
        # Extract start and end points for arrows (matching MATLAB exactly)
        # MATLAB: startx = [ux(1:3:end).', ux(2:3:end).', dxu(1:3:end).',dxl(1:3:end)].';
        # MATLAB: stopx = [ux(2:3:end).', ux(1:3:end).', dxu(2:3:end).',dxl(2:3:end)].';
        # Then removes NaNs
        
        # Get all start/end points from each edge type
        ux_starts = ux[0::3]  # ux(1:3:end) in MATLAB (1-indexed)
        ux_ends = ux[1::3]    # ux(2:3:end) in MATLAB
        uy_starts = uy[0::3]
        uy_ends = uy[1::3]
        
        dxu_starts = dxu[0::3]  # dxu(1:3:end)
        dxu_ends = dxu[1::3]    # dxu(2:3:end)
        dyu_starts = dyu[0::3]
        dyu_ends = dyu[1::3]
        
        dxl_starts = dxl[0::3]  # dxl(1:3:end)
        dxl_ends = dxl[1::3]    # dxl(2:3:end)
        dyl_starts = dyl[0::3]
        dyl_ends = dyl[1::3]
        
        # Concatenate all start points (matching MATLAB: [ux(1:3:end), ux(2:3:end), dxu(1:3:end), dxl(1:3:end)])
        # Concatenate all arrays (even if some are empty - they'll be filtered by NaN removal)
        all_startx = [ux_starts, ux_ends, dxu_starts, dxl_starts]
        all_starty = [uy_starts, uy_ends, dyu_starts, dyl_starts]
        all_stopx = [ux_ends, ux_starts, dxu_ends, dxl_ends]
        all_stopy = [uy_ends, uy_starts, dyu_ends, dyl_ends]
        
        # Filter out completely empty arrays, then concatenate
        startx_parts = [arr for arr in all_startx if len(arr) > 0]
        starty_parts = [arr for arr in all_starty if len(arr) > 0]
        stopx_parts = [arr for arr in all_stopx if len(arr) > 0]
        stopy_parts = [arr for arr in all_stopy if len(arr) > 0]
        
        if startx_parts:
            startx = np.concatenate(startx_parts)
            starty = np.concatenate(starty_parts)
        else:
            startx = np.array([])
            starty = np.array([])
        
        if stopx_parts:
            stopx = np.concatenate(stopx_parts)
            stopy = np.concatenate(stopy_parts)
        else:
            stopx = np.array([])
            stopy = np.array([])
        
        # Remove NaNs (matching MATLAB: starty(isnan(starty)) = [])
        # Only remove NaNs if arrays are not empty and have the same length
        if len(startx) > 0 and len(stopx) > 0 and len(startx) == len(stopx):
            valid = ~(np.isnan(startx) | np.isnan(starty) | np.isnan(stopx) | np.isnan(stopy))
            startx = startx[valid]
            starty = starty[valid]
            stopx = stopx[valid]
            stopy = stopy[valid]
        elif len(startx) != len(stopx):
            # If lengths don't match, something went wrong - use the minimum length
            min_len = min(len(startx), len(stopx))
            if min_len > 0:
                startx = startx[:min_len]
                starty = starty[:min_len]
                stopx = stopx[:min_len]
                stopy = stopy[:min_len]
                valid = ~(np.isnan(startx) | np.isnan(starty) | np.isnan(stopx) | np.isnan(stopy))
                startx = startx[valid]
                starty = starty[valid]
                stopx = stopx[valid]
                stopy = stopy[valid]
            else:
                startx = np.array([])
                starty = np.array([])
                stopx = np.array([])
                stopy = np.array([])
        
        # Create start and stop arrays
        start = np.column_stack([startx, starty])
        stop = np.column_stack([stopx, stopy])
        
        # Draw arrows if we have valid edges
        if len(start) > 0:
            
            # Draw arrows only (matching MATLAB style - minimal, no extra elements)
            plt.figure(figsize=(10, 10))
            arrow(start, stop, BaseAngle=60, color='black', linewidth=1.5)
            
            # MATLAB version doesn't plot nodes separately or add labels
            # Just the arrows on a blank background
            
            plt.axis('equal')
            # Remove axis labels and ticks to match MATLAB style
            plt.axis('off')
            
            # Save figure (matching original naming convention: EO2_{problem}_{N}_{Type}_.png)
            output_file = f'EO2_{problem_num}_{N}_{title}_.png'
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"   Saved: {output_file}")
            
            plt.show(block=False)
    
    print("\nVisualization complete!")
    input("Press Enter to close all figures...")


if __name__ == '__main__':
    main()


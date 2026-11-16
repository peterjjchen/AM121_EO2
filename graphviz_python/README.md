# EO2 Graph Visualizer (Python)

This script draws the kidney exchange graphs for EO2. It is a Python version of the MATLAB
visualizer in `graphviz.zip` and draws the same two graphs.

## Setup

You need Python 3 with `numpy` and `matplotlib`. If they are not already installed:

```bash
pip install numpy matplotlib
```

The script also uses `tkinter` for its file dialogs. It is included with most Python
installations.

## Running the visualizer

From the `graphviz_python` directory, run

```bash
python graphvisualizer.py N
```

where `N` is the number of patient-donor pairs in the instance (for example, 50). If you leave
out `N`, the script uses 50, and it corrects `N` to match the size of the data file you choose.

The script then asks for two files:

1. The AMPL output file: a binary N×N matrix whose element (i, j) is 1 when the donor of pair i
   gives a kidney to the patient of pair j.
2. The input data file for the same instance, for example `50_raw.txt`.

Both files should hold whitespace-separated 0s and 1s, one matrix row per line.

## Output

The script displays two graphs:

- **Cycles**: the exchanges in your solution.
- **Matches**: every compatible donor-patient match in the input data.

Arrows point from a donor to a recipient. For instances with more than 250 pairs the graphs are
usually too dense to read.

The script also saves both graphs as PNG files in the directory where you run it, named
`EO2_<prefix>_<N>_Cycles_.png` and `EO2_<prefix>_<N>_Matches_.png`. The prefix is the part of
your AMPL output file name before its first underscore (or `1` if the name has no underscore).
When you are done looking at the graphs, press Enter in the terminal to close them.

## Files

- `graphvisualizer.py`: the script to run
- `gplotd.py`, `arrow.py`, `polygon.py`: helper functions used by `graphvisualizer.py`

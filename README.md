# Tokenized BIM-Twin Monte Carlo Figures

This repository contains the cleaned figure-generation notebook for the Tokenized BIM-Twin Monte Carlo analysis.

## Contents

- `Tokenized_BIM_Twin_Monte_Carlo_GitHub.ipynb` — cleaned Jupyter notebook.
- `generate_figures.py` — script version for regenerating the figures.
- `figures/` — exported `.png` and `.pdf` figure files.
- `requirements.txt` — minimal Python dependencies.

## How to run

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run either the notebook or the script:

```bash
python generate_figures.py
```

The figures will be saved in the `figures/` directory.

## Reproducibility note

The numerical values, random seeds, labels, colors, hatch patterns, figure sizes, and export settings follow the final working notebook.  
Earlier draft cells and duplicated trial blocks were removed so the repository stays compact and easy to review.



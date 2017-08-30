# Jupyter notebook auto import

## Description

A common pattern is to start notebooks by importing the packages in your current environment. When you install new packages in your environment, you will then also need to synchronize these import statements. This can be tedious, especially if you have multiple notebooks that need to be updated.

## Usage

This repo attempts to automate the synchronization between your conda environment and import statements. Simply use `%run imports.py` to:

1. Import the most common standard libraries into the notebook. E.g., `os`, `re`, and `time`.
2. Import conda packages defined in your `environment.yml`.
  - You should explicitly list all packages you want to import in your environment spec.
  - Works even when the conda package name is different from the Python module name.
  - Uses common package abbreviations for you, such as `import numpy as np`.
  - If you have `line_profiler` or `memory_profiler` in your environment spec, the corresponding extensions will be loaded.
  - If you have `matplotlib` or `plotly` in your environment spec, these will be loaded with improved defaults for high-DPI screens.
3. Import local packages.
4. Cell output will display all single-line variables, not just the last one.
5. Changes made to local packages will be autoreloaded by default.

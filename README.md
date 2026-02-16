# FEP Simulation Data Automation & Convergence Analysis Tool

## Author
**David [Your Last Name]**
M.Sc. Student, Quantum Chemistry (Digital Chemistry)
University of Gdansk

---

## Overview
This software automates the post-processing of multi-stage Free Energy Perturbation (FEP) simulations. It addresses the critical need to assess whether a simulation has run long enough to yield reliable results (convergence).

The tool accepts **$N$ input files** (representing sequential simulation stages) and generates:
1.  **99 Data Subsets:** Representing 1% through 99% of the production run duration.
2.  **Convergence Plot:** A graphical analysis showing the stability of the Free Energy ($\Delta G$) calculation over time.

## Repository Contents
* `generate_data.py`: Core automation script for slicing and merging simulation data.
* `plot_results.py`: Analytical script that parses the generated subsets to plot $\Delta G$ convergence.
* `convergence_plot.png`: The visual output of the analysis.

---

## Design Rationale & Optimizations (`generate_data.py`)
This code was engineered specifically to handle high-throughput simulation data (e.g., $N=1000$ files or $10^7$ steps) without exceeding system resources.

### 1. Sequential Stream Processing (Memory Efficiency)
* **The Challenge:** Loading 1,000 simulation files into RAM simultaneously would cause an immediate `MemoryError` or system crash.
* **The Solution:** The script processes input files **sequentially**. Only one raw simulation file is held in memory at any given time. Once processed and distributed to the output streams, the memory is released.

### 2. Zero-Copy Slicing with `itertools.islice`
* **The Challenge:** Standard Python list slicing (e.g., `data[:50000]`) creates a *new copy* of the list in RAM. Doing this 99 times per file results in massive memory thrashing.
* **The Solution:** I utilized `itertools.islice`. This creates an **iterator** that "streams" the required data points directly from memory to the file without creating intermediate copies. This significantly reduces CPU overhead.

### 3. Disk I/O Optimization (Output Buffering)
* **The Challenge:** Writing data line-by-line to 99 different files simultaneously creates a bottleneck at the hard disk level (high I/O latency).
* **The Solution:** Output files are opened with a **1MB Buffer** (`buffering=1024*1024`). The script accumulates data in memory and flushes to the physical disk only when the buffer is full.

### 4. Dynamic Percentage Calculation
* **The Feature:** The script dynamically calculates slice points based on the number of production steps in the current file.
* **Robustness:** This ensures the code functions correctly regardless of the total step count (e.g., 1,000 vs 10,000,000 steps).

---

## Visualization Module (`plot_results.py`)
This script performs the analytical pass:
1.  Iterates through the 99 generated subsets.
2.  Extracts the final cumulative Free Energy value ($\Delta G$) from each.
3.  Generates a convergence plot (`convergence_plot.png`) to visually verify if the simulation has reached thermodynamic equilibrium.

---

## Usage

### Step 1: Data Generation
Ensure all raw simulation files are named `forward_*.fepout` and place them in the script directory.

```bash
python generate_data.py
```

### Output: 99 files generated in the processed_runs/ directory.

### Step 2: Convergence Analysis
Run the plotting script to analyze the generated data.

```bash
python plot_results.py
```

### Output: convergence_plot.png generated in the main directory.

---

## Requirements
* `Python 3.x`
* `Standard Libraries`: os, glob, itertools
* `External Libraries`: matplotlib (for graphing)

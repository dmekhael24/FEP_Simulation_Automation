import glob
import os
import matplotlib.pyplot as plt

def get_last_dG(filename):
    """Retrieves the final dG value by parsing the last valid data line."""
    with open(filename, 'r') as f:
        # Load file content
        lines = f.readlines()
        
        # Reverse scan to find last non-comment, non-empty line
        for line in reversed(lines):
            if line.strip() and not line.startswith('#'):
                parts = line.split()
                try:

                    return float(parts[-1])
                except ValueError:
                    continue
    return None

def main():
    # Locate dataset; sorted() ensures X-axis monotonicity (01% -> 99%)
    files = sorted(glob.glob("processed_runs/simulation_*percent.fepout"))
    
    if not files:
        files = sorted(glob.glob("simulation_*percent.fepout"))

    if not files:
        print("Error: No simulation_XXpercent.fepout files found.")
        return

    percentages = []
    dG_values = []

    print(f"Extracting dG metrics from {len(files)} files...")

    for filename in files:
        try:
            base_name = os.path.basename(filename)
            percent_str = base_name.split('_')[1].replace('percent.fepout', '')
            percent = int(percent_str)
            
            val = get_last_dG(filename)
            
            if val is not None:
                percentages.append(percent)
                dG_values.append(val)
        except Exception as e:
            print(f"Skipping {filename}: {e}")

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(percentages, dG_values, marker='o', linestyle='-', color='b', markersize=4)
    
    plt.title("Convergence of Free Energy (\u0394G) vs. Simulation Length")
    plt.xlabel("Percentage of Production Run Used (%)")
    plt.ylabel("Free Energy \u0394G (kcal/mol)")
    plt.grid(True)
    
    output_img = "convergence_plot.png"
    plt.savefig(output_img)
    print(f"Plot saved to {output_img}")

if __name__ == "__main__":
    main()

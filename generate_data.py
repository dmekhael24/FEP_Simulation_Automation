import os
import glob
from itertools import islice

def process_simulations():
    # Grab input files
    input_files = sorted(glob.glob("forward_*.fepout"))
    
    if not input_files:
        print("Error: No 'forward_*.fepout' files found.")
        return

    print(f"Processing {len(input_files)} input files...")

    output_dir = "processed_runs"
    os.makedirs(output_dir, exist_ok=True)

    output_handles = {}
    for i in range(1, 100):
        fname = os.path.join(output_dir, f"simulation_{i:02d}percent.fepout")
        output_handles[i] = open(fname, 'w', buffering=1024*1024)

    for f_name in input_files:
        print(f"Parsing {f_name}...")
        
        with open(f_name, 'r') as f:
            lines = f.readlines()
        
        headers = []
        equil = []
        prod = []
        
        # Parse data
        for line in lines:
            if line.startswith('#'):
                headers.append(line)
            elif line.startswith('FepEnergy:'):
                step = int(line.split()[1])
                # Threshold: 1M steps for equilibration
                if step <= 1000000:
                    equil.append(line)
                else:
                    prod.append(line)

        total_prod_lines = len(prod)
        
        # write to outputs
        for i in range(1, 100):
            slice_idx = int(total_prod_lines * (i / 100.0))
            
            # Append Headers -> Full Equil -> Sliced Prod
            output_handles[i].writelines(headers)
            output_handles[i].writelines(equil)
            output_handles[i].writelines(islice(prod, slice_idx))

    # Cleanup
    for h in output_handles.values():
        h.close()

    print("Done. Generated 99 files in 'processed_runs'.")

if __name__ == "__main__":
    process_simulations()

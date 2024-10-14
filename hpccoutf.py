#!/usr/bin/env python3

import argparse
import sys
import re
import csv
import os

def read_hpcc_output(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Parse the content into a dictionary
    hpcc_output = dict(re.findall(r'(\w+)=(\d.*)', content))
    return hpcc_output

def write_web_to_csv(hpccoutf, csv_file):
    # Initialize a dictionary to store existing keys and their corresponding values
    existing_data = {}

    # Check if the CSV file exists
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            # Load existing keys and their corresponding values
            for row in reader:
                if len(row) > 0:  # Ensure the row is not empty
                    key = row[0]
                    values = row[1:]  # Remaining entries are the values
                    existing_data[key] = values  # Store in a dictionary

    # Collect new entries for the CSV
    new_entries = {}

    # Process keys from walkorder to add new entries
    for key in walkorder:
        if key == 'StarSTREAM_Triad*CommWorldProcs':
            value = float(hpccoutf['StarSTREAM_Triad']) * float(hpccoutf['CommWorldProcs']) / 1000
        elif key in ['PTRANS_GBs', 'MPIFFT_Gflops']:
            value = float(hpccoutf[key]) / 1000
        else:
            value = float(hpccoutf.get(key, 0))

        # If the key exists in existing_data, append the new value
        if key in existing_data:
            existing_data[key].append(value)
        else:
            # If the key does not exist, create a new entry
            new_entries[key] = [value]

    # Write updated data back to the CSV file
    with open(csv_file, mode='w', newline='') as file:  # Write mode to update the file
        writer = csv.writer(file)

        # Write existing data
        for key, values in existing_data.items():
            writer.writerow([key] + values)  # Write key and all its values

        # Write new entries to the CSV file
        for key, values in new_entries.items():
            writer.writerow([key] + values)  # Write new key and its value

    if new_entries:
        print(f"New web parameters added to {csv_file}:")
        for key, value in new_entries.items():
            print(f"  {key}: {value}")
    else:
        print("No new web parameters to add.")

def show_all(hpccoutf):
    for key in sorted(hpccoutf.keys()):
        print(f"{key}: {hpccoutf[key]}")

def show_web(hpccoutf):
    print("\n")
    count = 0
    for key in walkorder:
        if key == 'StarSTREAM_Triad*CommWorldProcs':
            value = float(hpccoutf['StarSTREAM_Triad']) * float(hpccoutf['CommWorldProcs']) / 1000
        elif key in ['PTRANS_GBs', 'MPIFFT_Gflops']:
            value = float(hpccoutf[key]) / 1000
        else:
            value = float(hpccoutf.get(key, 0))

        print(f"{key:<40} {crosswalk[key]:<30} {value:>10.3f} {walkunits[count]}")
        count += 1


# Define constants
walkorder = [
    'HPL_Tflops', 'PTRANS_GBs', 'MPIRandomAccess_GUPs', 'MPIFFT_Gflops',
    'StarSTREAM_Triad*CommWorldProcs', 'StarSTREAM_Triad', 'StarDGEMM_Gflops',
    'RandomlyOrderedRingBandwidth_GBytes', 'RandomlyOrderedRingLatency_usec'
]

walkunits = [
    'Tera Flops per Second', 'Tera Bytes per Second', 'Giga Updates per Second',
    'Tera Flops per Second', 'Tera Bytes per Second', 'Giga Bytes per Second',
    'Giga Flops per Second', 'Giga Bytes per second', 'micro-seconds'
]

crosswalk = {
    'HPL_Tflops': 'G-HPL',
    'PTRANS_GBs': 'G-PTRANS',
    'MPIRandomAccess_GUPs': 'G-RandomAccess',
    'MPIFFT_Gflops': 'G-FFT',
    'StarSTREAM_Triad*CommWorldProcs': 'EP-STREAM Sys',
    'CommWorldProcs': 'MPI Processes',
    'StarSTREAM_Triad': 'EP-STREAM Triad',
    'StarDGEMM_Gflops': 'EP-DGEMM',
    'RandomlyOrderedRingBandwidth_GBytes': 'RandomRing Bandwidth',
    'RandomlyOrderedRingLatency_usec': 'RandomRing Latency'
}

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process HPCC output file.')
    parser.add_argument('-a', action='store_true', help='Show all parameters')
    parser.add_argument('-w', action='store_true', help='Show web parameters')
    parser.add_argument('-f', type=str, required=True, help='Input file name')
    parser.add_argument('--csv', type=str, help='Output CSV file name for web parameters')  # Option for CSV output

    args = parser.parse_args()

    if not (args.a or (args.w and args.f)):
        parser.print_help()
        sys.exit(1)

    # Read the HPCC output
    hpccoutf = read_hpcc_output(args.f)

    if args.a:
        show_all(hpccoutf)
    if args.w:
        show_web(hpccoutf)
    
    if args.csv:
        write_web_to_csv(hpccoutf, args.csv)  # Write web parameters to CSV if specified

if __name__ == "__main__":
    main()


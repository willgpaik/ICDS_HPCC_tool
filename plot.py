#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_csv_data(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, header=None)

    # Set the first column as the index (the keys)
    df.set_index(0, inplace=True)

    # Transpose the DataFrame to have keys as rows and values as columns
    df = df.transpose()

    # List of y-labels corresponding to the keys
    y_labels = [
        'TFlops',       # HPL_Tflops
        'TB/s',         # PTRANS_GBs
        'GUpdates/s',   # MPIRandomAccess_GUPs
        'TFlops',       # MPIFFT_Gflops
        'TB/s',         # StarSTREAM_Triad*CommWorldProcs
        'GB/s',         # StarSTREAM_Triad
        'Gflops',       # StarDGEMM_Gflops
        'GB/s',         # RandomlyOrderedRingBandwidth_GBytes
        'usec'          # RandomlyOrderedRingLatency_usec
    ]

    # Create a new figure for the plot
    plt.figure(figsize=(12, 6))

    # Plot each key's data
    for i, key in enumerate(df.columns):
        plt.plot(df.index, df[key], marker='o', label=key)

    # Formatting the plot
    plt.title('Data Trends from CSV')
    plt.xlabel('Entry Number')  # Optional: You can include x-label if needed
    
    # Set y-ticks based on the data
    plt.ylabel('Values')  # General y-label for all data
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()

    # Show individual y-labels in the legend for clarity
    for i, label in enumerate(y_labels):
        plt.plot([], [], marker='o', label=label)  # Empty plots to create legend entries for y-labels

    plt.tight_layout()

    # Show the plot
    plt.show()

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Plot data from CSV file.')
    parser.add_argument('--csv', type=str, required=True, help='Input CSV file name')

    args = parser.parse_args()

    # Plot the data from the specified CSV file
    plot_csv_data(args.csv)

if __name__ == "__main__":
    main()


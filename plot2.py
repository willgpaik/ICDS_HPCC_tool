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

    # Create subplots
    num_keys = df.shape[1]  # Number of keys (columns)
    num_rows = (num_keys + 1) // 2  # Determine number of rows needed for subplots
    fig, axes = plt.subplots(num_rows, 2, figsize=(12, num_rows * 4))  # Adjust the figure size as needed

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # List of y-axis labels corresponding to the keys
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

    # Plot each key's data in a different subplot
    for i, key in enumerate(df.columns):
        axes[i].plot(df.index, df[key], marker='o', label=key)
        axes[i].set_title(key)
        axes[i].set_ylabel(y_labels[i])  # Set the y-label for each subplot
        axes[i].grid()
#        axes[i].legend()
        
        # Optionally set x-ticks for better readability
        axes[i].set_xticks(df.index)
        axes[i].set_xticklabels(df.index, rotation=45)
        
        # Remove x-labels as per request
        axes[i].set_xlabel('')  # Clear x-label

    # Hide any empty subplots if the number of keys is odd
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)  # Adjust padding

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


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

    # Plot each key's data
    for key in df.columns:
        plt.plot(df.index, df[key], marker='o', label=key)

    # Formatting the plot
    plt.title('Data Trends from CSV')
    plt.xlabel('Entry Number')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
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


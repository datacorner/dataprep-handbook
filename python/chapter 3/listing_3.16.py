import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import common constants and functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import common as C


def initialize():
    """ Read the source file (Titanic disaster) and provide a dataframe

    Returns:
        dataframe: titanic dataset
    """
    # read the CSV file
    df = pd.read_csv(C.DATASET_FOLDER + "titanic/train.csv")
    # survived=0 means the passenger died, survived=1 means he survived, let's make it more clear in the dataset:
    df['SurvivedProba'] = df['Survived']
    df['SurvivedLabel'] = df['Survived'].map({1: 'alive' , 0: 'dead'})
    return df

def compare_dist(distrib1, distrib2, nbbins = 40):
    """ This funtion is an utility to display the difference between two ages distribution

    Args:
        distrib1 (dataframe): First distribution 
        distrib2 (dataframe): Second distribution to compare with
        nbbins (int, optional): Nb bins for histogram. Defaults to 40.
    """
    # Set up the plot
    plt.figure(figsize=(15, 6))
    # Define the bins
    bins = np.linspace(0, max(distrib.max(), distrib2.max()), nbbins+1)  # x bins, ranging from 0 to the max
    bin_width = bins[1] - bins[0]
    # Calculate the histograms
    hist1, _ = np.histogram(distrib1, bins=bins)
    hist2, _ = np.histogram(distrib2, bins=bins)
    # Set up the bar positions
    bar_positions = np.arange(len(bins) - 1)
    bar_width = 0.35
    # Create the side-by-side bar chart
    plt.bar(bar_positions - bar_width/2, hist1, bar_width, alpha=0.8, color='black', label='Original dataset')
    plt.bar(bar_positions + bar_width/2, hist2, bar_width, alpha=0.8, color='grey', label='Dataset updated')
    # Customize & show the plot
    plt.title('Age Distribution Comparison in dataset')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.legend()
    plt.xticks(bar_positions, [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins)-1)])
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def impute_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1 #A
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    replacement_value = data.median()
    data[data < lower_bound] = replacement_value
    data[data > upper_bound] = replacement_value
    return data


if __name__ == "__main__":
    df = initialize()
    distrib = df['Age'].dropna()

    # Imputing age outliers with the IQR technique and the median
    dfo = impute_outliers(distrib.copy())
    compare_dist(distrib, dfo)

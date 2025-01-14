import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

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

def parse_name(name):
    """ parsing the names column

    Args:
        name (string): name

    Returns:
        parsed name: _description_
    """
    name_without_parentheses = re.sub(r'\([^)]*\)', '', name).strip() #A
    words = re.findall(r'\b\w+\b|\.|,', name_without_parentheses) #B
    names = []
    prefix = None
    title = None
    for word in words:
        if word.lower() in ['mr', 'mrs', 'miss', 
                            'master', 'dr', 'rev', 
                            'col', 'major', 'capt']:
            title = word
        elif word.lower() in ['van', 'de', 'der', 'du', 'di', 'la', 'le']:
            prefix = word
        elif word not in [',', '.']:
            names.append(word)

    return {
        'names': names,
        'prefix': prefix,
        'title': title
    }

def categorize_title(title):
    if title in ['Mr', 'Mrs', 'Ms', 'Miss', 'Mme', 'Mlle']:
        return 'Common'
    elif title in ['Master', 'Don', 'Lady', 'Sir', 'Jonkheer', 'Dona']:
        return 'Rich'
    elif title in ['Rev', 'Dr', 'Major', 'Col', 'Capt']:
        return 'Professional'
    else:
        return np.nan

def plotByGroupAndRate(df, col):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    sns.countplot(x=col, hue="Survived", 
                data=df[df["Survived"].notnull()], ax=axs[0])
    axs[0].set_title("Survival by Group")
    axs[0].set_xlabel("Group")
    axs[0].set_ylabel("Count")

    survival_rates = df.groupby(col)['SurvivedProba'].mean()
    sns.barplot(x=survival_rates.index, y=survival_rates.values, ax=axs[1])
    axs[1].set_title('Survival Rate by Group')
    axs[1].set_xlabel('Title Group')
    axs[1].set_ylabel('Survival Rate')
    axs[1].set_ylim(0, 1)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = initialize()
    df['NameComponents'] = df['Name'].apply(parse_name) #C
    df['NameList'] = df['NameComponents'].apply(lambda x: x['names'])
    df['Prefix'] = df['NameComponents'].apply(lambda x: x['prefix'])
    df['Title'] = df['NameComponents'].apply(lambda x: x['title'])
    df = df.drop('NameComponents', axis=1)
    df['TitleGroup'] = df['Title'].apply(categorize_title)
    plotByGroupAndRate(df, "TitleGroup")
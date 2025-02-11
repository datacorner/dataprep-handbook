import pandas as pd
import re 

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
    """ This function parses a name string into its components, extracting the 
        individual names, any title (e.g., Mr., Dr.), and any prefix 
        (e.g., van, de). The function is designed to handle names with punctuation 
        and parentheses gracefully, removing irrelevant elements before processing.
    Parameters:
        name (str): The input name string to parse. It may include titles, prefixes, 
                    parentheses, and punctuation.
    Returns:
        dict: A dictionary containing the parsed components:
            - 'names' (list): A list of individual name components (excluding titles and prefixes).
            - 'prefix' (str or None): The identified prefix (if any).
            - 'title' (str or None): The identified title (if any).
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
        elif word.lower() in ['van', 'de', 'der', 
                                'du', 'di', 'la', 'le']:
            prefix = word
        elif word not in [',', '.']:
            names.append(word)

    return {
        'names': names,
        'prefix': prefix,
        'title': title
    }

if __name__ == "__main__":
    df = initialize()
    df['NameComponents'] = df['Name'].apply(parse_name) #C
    df['NameList'] = df['NameComponents'].apply(lambda x: x['names'])
    df['Prefix'] = df['NameComponents'].apply(lambda x: x['prefix'])
    df['Title'] = df['NameComponents'].apply(lambda x: x['title'])
    df = df.drop('NameComponents', axis=1)
    print (df)
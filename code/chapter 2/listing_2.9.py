import pandas as pd
import numpy as np
import re

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
    """ This function categorizes a given title into predefined groups based on its 
        social or professional context. Titles are grouped as 'Common', 'Rich', or 
        'Professional', while unrecognized titles are assigned a NaN value.
    Parameters:
        title (str): The input title to categorize (e.g., 'Mr', 'Dr', 'Lady').
    Returns:
        str or np.nan: The category of the title:
            - 'Common' for widely used social titles (e.g., 'Mr', 'Miss').
            - 'Rich' for titles typically associated with wealth or nobility 
            (e.g., 'Don', 'Lady').
            - 'Professional' for titles related to professions or ranks 
            (e.g., 'Dr', 'Major').
            - np.nan if the title does not match any predefined categories.
    """
    if title in ['Mr', 'Mrs', 'Ms', 'Miss', 'Mme', 'Mlle']:
        return 'Common'
    elif title in ['Master', 'Don', 'Lady', 'Sir', 'Jonkheer', 'Dona']:
        return 'Rich'
    elif title in ['Rev', 'Dr', 'Major', 'Col', 'Capt']:
        return 'Professional'
    else:
        return np.nan

if __name__ == "__main__":
    df = pd.read_csv("../data/titanic/train.csv")
    df['NameComponents'] = df['Name'].apply(parse_name) 
    df['NameList'] = df['NameComponents'].apply(lambda x: x['names'])
    df['Prefix'] = df['NameComponents'].apply(lambda x: x['prefix'])
    df['Title'] = df['NameComponents'].apply(lambda x: x['title'])
    df = df.drop('NameComponents', axis=1)

    df['TitleGroup'] = df['Title'].apply(categorize_title)
    
    print (df)
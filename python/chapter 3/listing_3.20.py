import pandas as pd
from fuzzywuzzy import fuzz

def fuzzy_deduplication(df, threshold=90):
    """ Define a function for fuzzy matching rows

    Args:
        df (dataframe): dataset to undup
        threshold (int, optional): threshold. Defaults to 90.

    Returns:
        _type_: _description_
    """
    duplicates = []
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            if fuzz.ratio(df.iloc[i]['Name'].lower(), \
                    df.iloc[j]['Name'].lower()) > threshold:
                duplicates.append((i, j))
    return duplicates

if __name__ == "__main__":
    data = {
        'Name': ['John doe', 'John doe', 'Alice Johnson', 'Alice jonson', 'Bob Smith', 'Bob Smith'],
        'Email': ['john@example.com', 'john@example.com', 'alice@domain.com', 'alice@domain2.com', 'bob@website.com', 'bob@website.com'],
        'Date_of_Birth': ['1990-01-01', '1990-01-01', '1985-05-12', '1985-05-12', '1970-08-22', '1970-08-22'],
    }
    
    df = pd.DataFrame(data)

    # Detect duplicates based on fuzzy matching of the 'Name' column
    fuzzy_duplicates = fuzzy_deduplication(df)
    print("\nFuzzy Matched Duplicates (Name):")
    print(fuzzy_duplicates)

    # Drop duplicates (this can be adjusted as per need)
    df_fuzzy = df.drop([dup[1] for dup in fuzzy_duplicates])
    print("\nAfter Fuzzy Matching Deduplication:")
    print(df_fuzzy)


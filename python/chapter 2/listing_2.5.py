import pandas as pd

def initialize():
    """ Read the source file (Titanic disaster) and provide a dataframe

    Returns:
        dataframe: titanic dataset
    """
    # read the CSV file
    df = pd.read_csv("../Titanic disaster/train.csv")
    # survived=0 means the passenger died, survived=1 means he survived, let's make it more clear in the dataset:
    df['SurvivedProba'] = df['Survived']
    df['SurvivedLabel'] = df['Survived'].map({1: 'alive' , 0: 'dead'})
    return df

if __name__ == "__main__":
    df = initialize()
    
    ticket_counts = df.groupby('Ticket')['PassengerId'].count().reset_index()
    same_tickets = ticket_counts[ticket_counts['PassengerId'] > 1] 
    dfTickAna = df.merge(same_tickets [['Ticket']], 
                        on='Ticket', 
                        how='inner') 
    dfTickAna[["PassengerId", "Ticket", "Fare"]].sort_values(by=["Ticket"])

    print (dfTickAna)
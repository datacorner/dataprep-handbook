import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

def manage_datetime(df):
    """
    Converts the 'datetime' column in the DataFrame to a datetime object and extracts the hour.
    Parameters:
        df (pandas.DataFrame): The input DataFrame containing a 'datetime' column.
    Returns:
        pandas.DataFrame: The DataFrame with 'datetime' converted and an additional 'hour' column.
    """
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Extract the hour from the datetime column
    df['hour'] = df['datetime'].dt.hour
    df = df.drop(columns=['datetime'])
    return df

def onehot(df):
    """ Apply the one hot encoding technique to a dataset
    Args:
        df (dataframe): initial dataset
    Returns:
        dataframe: encoded dataset
    """
    thres = 10  # Par exemple, les colonnes avec moins de 10 valeurs uniques sont considérées comme catégorielles
    cols_categ = [col for col in df.columns if df[col].nunique() < thres and df[col].dtype == 'object']
    cols_non_categ = [col for col in df.columns if df[col].nunique() >= thres and df[col].dtype == 'object' or df[col].dtype != 'object']
    df_train_non_categ = df[ cols_non_categ ]
    df_train_non_categ = manage_datetime(df_train_non_categ) 
    df_train_categ = df[ cols_categ ]

    encoder = OneHotEncoder(sparse_output=False) #A
    onehot_encoded = encoder.fit_transform(df_train_categ[cols_categ])
    feature_names = encoder.get_feature_names_out(cols_categ) #B
    df_onehot_encoded = pd.DataFrame(onehot_encoded, columns=feature_names) #C
    return pd.concat([df_train_non_categ, df_onehot_encoded], axis=1) #D

def prepare_features(df):
    """ Prepares the feature
    Args:
        df (dataframe): Initial dataframe
    """
    # One hot encoding
    df_final = onehot(df)
    # Scaling data
    scaler = MinMaxScaler()
    scaled_array = scaler.fit_transform(df_final)
    # Convert the scaled array back to a DataFrame with the same column names
    return pd.DataFrame(scaled_array, columns=df_final.columns, index=df_final.index)

if __name__ == "__main__":
    df = pd.read_csv("../data/bikerental/rental_train.csv", encoding='UTF8')

    df_scaled = prepare_features(df)
    
    # Applying PCA on our bike rental dataset
    X = df_scaled.drop(['Nb of rental'], axis=1)    
    y = df_scaled['Nb of rental']   
    pca = PCA(n_components=5)    
    X_pca = pca.fit_transform(X)

    print(pca.explained_variance_ratio_)
    print(sum(pca.explained_variance_ratio_))
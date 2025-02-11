# Import common constants and functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common import DATASET_FOLDER

import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv(DATASET_FOLDER + "titanic/train.csv")
    chunk_size = 100
    chunks = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    print (chunks)
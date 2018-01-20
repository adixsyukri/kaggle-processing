import requests
import numpy as np
import pandas as pd
import yaml
from kaggle import Kaggle

# Download dataset process
DATA_URL = "https://www.kaggle.com/crawford/weekly-sales-transactions/downloads/Sales_Transactions_Dataset_Weekly.csv"
SETTINGS = load_settings()

def load_settings():
    with open('config.yaml', 'r') as sf:
        settings = yaml.load(sf.read())
    return settings

def chunk(df, n):
    for i in range(0, df.shape[0], n):
        yield df[i:i + n]

def cleanup(arr):
    '''Cleanup Kaggle dataset since there are additional columns'''
    index = 0
    for i, x in enumerate(arr[0]):
        if (x.find('Normalized') == 0):
            continue
        if (x.find('MAX') == 0):
            continue
        if (x.find('MIN') == 0):
            continue
        index = i
    
    return [x[:index] for x in arr if x]

kaggle = Kaggle(DATA_URL, SETTINGS)
kaggle_data = kaggle.get_data()
processed_data = cleanup(kaggle_data)
np_transpose_data = np.transpose(np.array(processed_data)) #transpose data so that product become the columns
fullData = pd.DataFrame(data=np_transpose_data[1:, 1:].astype(np.float), index=np_transpose_data[1:,0], columns=np_transpose_data[0,1:])

# Median for all product
median_data = fullData.median()

# Mean for all product
mean_data = fullData.mean()

# Min for all product
min_data = fullData.min()   

# Max for all product
max_data = fullData.max()

# Best product based on volume
sum_of_product = fullData.sum()
index_array, = np.where(sum_of_product == sum_of_product.max())
best_product = (fullData.columns[index_array[0]], sum_of_product.max())

# Group biweekly sales
grouped = chunk(fullData, 2)
sum_grouped = [i.sum() for i in grouped]
worst_5_product_biweekly = [('Biweekly {}'.format(i+1), x.nsmallest(5)), for i, x in enumerate(sum_grouped)]

# Get outliers for every product
outliers = fullData[~(np.abs(fullData - fullData.mean())<=(3*fullData.std()))]


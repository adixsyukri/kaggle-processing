import requests
import numpy as np
import yaml
from kaggle import Kaggle

# Download dataset process
DATA_URL = "https://www.kaggle.com/crawford/weekly-sales-transactions/downloads/Sales_Transactions_Dataset_Weekly.csv"

def load_settings():
    with open('config.yaml', 'r') as sf:
        settings = yaml.load(sf.read())
    return settings


def median_mean_stdev(data):
    sorted_array = sorted(np.array(data).astype(np.float))
    median_data = np.median(sorted_array)
    print('median_data', median_data)
    mean_data = np.mean(sorted_array)
    print('mean_data', mean_data)
    stdev_data = np.std(sorted_array)
    print('stdev_data', stdev_data)
    threshold = 3

    z_scores = [(x - mean_data) / stdev_data for x in sorted_array]
    outlier_indexes, = np.where(np.abs(z_scores) > threshold)
    print('outlier_indexes', outlier_indexes)
    return (median_data, mean_data, stdev_data, outlier_indexes)

def chunk(arr, n):
    for i in range(0, len(arr), n):
        yield sum(arr[i:i + n])


kaggle = Kaggle(DATA_URL)
kaggle.login(load_settings())
kaggle_data = kaggle.get_data()
header = kaggle_data[0]
dataset = kaggle_data[1:]


# Search for median
final = []
for index, row in enumerate(dataset):
    if len(row) == 1:
        continue
    product = row[0]
    data = [float(x) for x in row[1:] if x]
    median_data, mean_data, stdev_data, outlier_indexes = median_mean_stdev(data)
    outliers = [(header[x+1], data[x]) for x in outlier_indexes if x]
    final.append({
        'product': row[0],
        'median': median_data,
        'mean': mean_data,
        'min': min(data),
        'max': max(data),
        'total': sum(data),
        'biweekly': [x for x in chunk(data, 2) if x],
        'outliers': outliers
    })

print final
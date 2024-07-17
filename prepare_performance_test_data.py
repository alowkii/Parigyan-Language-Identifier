import numpy as np
import random
import pandas as pd

def random_data_selection(size=1000):
    file_path = 'backup/test_dataset_30k_[Backup].csv'

    training_data = pd.read_csv(file_path, encoding='utf-8', dtype={'column1': 'string', 'column2': 'string'})

    if training_data.shape[0] < size:
        raise ValueError("The input file does not have at least size rows.")

    random_rows = training_data.sample(n=size, axis=0, random_state=np.random.seed(random.randint(0, size*100)))

    random_rows.to_csv('dataset/performance_test.csv', index=False)

random_data_selection()
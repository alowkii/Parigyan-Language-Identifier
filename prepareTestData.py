## Do not run this file, it may harm the program. Only run it if you want to prepare test data for the model from a new dataset.
import pandas as pd

def prepare_test_data(input_file, output_file, N):
    df = pd.read_csv(input_file, encoding= 'utf-8')

    if N > len(df):
        raise ValueError("N is greater than the number of rows in the training data")
    
    df.drop(columns=['id'], inplace=True)
    
    test_data = df.sample(n=N)
    
    remaining_data = df.drop(test_data.index)

    test_data.to_csv(output_file, index=False)
    
    remaining_data.to_csv(input_file, index=False)

input_file = 'dataset/training-data.csv'
output_file = 'dataset/test-data.csv'
N = 10000

prepare_test_data(input_file, output_file, N)

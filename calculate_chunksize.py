import psutil
import pandas as pd

def calc_chunksize(df, share=0.3):
    """Estimate optimal chunksize (in records) for writing large dfs with df.to_csv"""

    # get approximate record size in bytes
    row_size = df.memory_usage(index=True, deep=True).sum() / df.index.size
    # get share of available memory size in bytes
    avail_mem = psutil.virtual_memory().available * share

    return int(avail_mem / row_size)

df = pd.read_csv('dataset/training-data.csv', encoding='utf-8', dtype={'column1': 'string', 'column2': 'string'})
print(calc_chunksize(df))
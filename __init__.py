# Usage:
# Initialize NaiveBayesLanguageIdentifier
import random_data_selection
import pickle
from test import *
from model import *
import threading
import itertools
import sys
import time

model = NaiveBayesLanguageIdentifier(n=3)
epochs = 10

def loading_screen(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f"\rLoading... {next(spinner)}                    ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rModel Loaded!                                   \n')
    sys.stdout.flush()

for i in range(epochs):
    print(f"Epoch: {i + 1}")
    
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_screen, args=(stop_event,))
    loading_thread.start()
    
    random_data_selection.random_data_selection(size=2000000)
    text_data, labels = model.load_data('dataset/train-subDataSet.csv')
    model.train(text_data, labels)

    stop_event.set()
    loading_thread.join()
    test(model)

print("\nTraining completed.\n")

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

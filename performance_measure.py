import pandas as pd
import time
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def progress_bar(progress, total, elapsed_time):
    percent = 100 * (progress / total)
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    eta_minutes, eta_seconds = divmod(elapsed_time, 60)
    print(f"\rTesting:\t|{bar}| {percent:.2f}%\tETA: {eta_minutes:.0f} mins {eta_seconds:.0f} seconds    ", end='\r')

def test(model):
    df = pd.read_csv('dataset/test-data-test-case.csv', encoding='utf-8', dtype={'column1': 'string', 'column2': 'string'})
    text_data = df['sentence'].tolist()
    true_labels = df['lan_code'].tolist()
    length_data = len(text_data)

    with open('dataset/lan_to_language.json', 'r', encoding='utf-8') as file:
        lan_to_language = json.load(file)
    
    start_time = time.time()
    # Initial prediction for time estimation
    predicted_language = model.predict(text_data[0])
    elapsed_time = time.time() - start_time

    total_time = elapsed_time * length_data * 2  # Estimated total time (200% buffer)
    
    predicted_labels = [lan_to_language[predicted_language]]

    for i in range(1, length_data):
        start_time = time.time()
        predicted_language = model.predict(text_data[i])
        elapsed_time = time.time() - start_time

        predicted_labels.append(lan_to_language[predicted_language])

        total_time -= elapsed_time
        progress_bar(i + 1, length_data, total_time)
    
    eta_minutes, eta_seconds = divmod((elapsed_time * length_data * 3 - total_time), 60)
    print(f"\nTesting Complete. Total time: {eta_minutes:.0f} mins {eta_seconds:.0f} seconds\n")
    
    # Preprocess labels
    true_labels = [label.lower() for label in true_labels]
    predicted_labels = [label.lower() for label in predicted_labels]

    # Compute metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    # Print the metrics
    print("Performance Metrics:")
    print(f"Accuracy: {accuracy*100:.2f}")
    print(f"Precision: {precision*100:.2f}")
    print(f"Recall: {recall*100:.2f}")
    print(f"F1-Score: {f1*100:.2f}")

model = pickle.load(open("model.pkl", 'rb'))
test(model)

import pandas as pd
import time

# Load test data
def progress_bar(progress, total, elapsed_time):
    percent = 100 * (progress / total)
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    if progress > 0:
        eta_minutes, eta_seconds = divmod(elapsed_time, 60)
        eta_seconds = int(eta_seconds)
    if progress == total:
        eta_seconds = 0
    print(f"\rTesting:\t|{bar}| {percent:.2f}%\tETA: {eta_minutes} mins {eta_seconds} seconds    ", end='\r')
    

def test(model):
    score = 0
    df = pd.read_csv('dataset/test-data.csv', encoding='utf-8', dtype={'column1': 'string', 'column2': 'string'})
    text_data = df['sentence'].tolist()
    labels = df['lan_code'].tolist()
    length_data = len(text_data)
    
    start_time = time.time()
    predicted_language = model.predict(text_data[0])
    elapsed_time = time.time() - start_time
    total_time = elapsed_time * length_data * 1.5       # 50% extra time for the total time
    predicted_time = total_time
    
    for i in range(1,length_data):
        start_time = time.time()
        predicted_language = model.predict(text_data[i])
        elapsed_time = time.time() - start_time
        
        if predicted_language.lower() == labels[i].lower():
            score += 1
        
        if(total_time < 0):
            total_time = elapsed_time * (length_data - i + 1)
        total_time -= elapsed_time
        progress_bar(i + 1, length_data, total_time)
        
    eta_minutes, eta_seconds = divmod((predicted_time - total_time), 60)
    eta_seconds = int(eta_seconds)
    
    print("\n")
    print("\nTime Taken:\t", eta_minutes,"minutes",eta_seconds, "seconds")
    print("\nTesting Completed.\n")
    print(f"Score: {score} out of {len(text_data)}")
    print("Accuracy: ", (score/len(text_data))*100, "%")
    print("\n\n")
    return score
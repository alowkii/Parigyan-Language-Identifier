import pickle
import json

def identify_language():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    def load_text_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    # Load a test document from file
    test_document = load_text_file('input/input.txt')

    # Predict the language of the test document
    predicted_language = model.predict(test_document)

    # Metadata of languages
    file_path = 'dataset/lan_to_language.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        lan_to_language = json.load(file)
        
    return lan_to_language[predicted_language]
    
# print("Predicted language:", identify_language())
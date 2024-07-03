import io
from pydub import AudioSegment
from google.oauth2 import service_account
from google.cloud import speech

def recognize_voice():
    # Convert stereo audio to mono
    input_audio_path = "input/input.wav"
    output_audio_path = "input/input.wav"

    sound = AudioSegment.from_wav(input_audio_path)
    sound = sound.set_channels(1)
    sound.export(output_audio_path, format="wav")

    # Path to the service account key file
    client_file = "service_account_Google.json"

    # Create credentials using the service account key file
    credentials = service_account.Credentials.from_service_account_file(client_file)

    # Initialize the Speech-to-Text client with the credentials
    client = speech.SpeechClient(credentials=credentials)

    # Read the mono audio file
    with io.open(output_audio_path, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    # Configuration for the speech recognition
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",  # Default language, can be removed if using alternative language codes
        alternative_language_codes=["en-US", "es-ES", "fr-FR", "de-DE", "hi-IN", "it-IT", "ja-JP", "ko-KR", "pt-BR", "ru-RU", "zh-CN", "ne-NP", "ar-AE", "bn-BD", "cs-CZ", "da-DK", "nl-NL", "fi-FI", "el-GR", "he-IL", "hu-HU", "id-ID", "ga-IE", "ms-MY", "no-NO", "pl-PL", "ro-RO", "sk-SK", "sl-SI", "sv-SE", "th-TH", "tr-TR", "uk-UA", "vi-VN"] 
    )

    # Perform the speech recognition
    response = client.recognize(config=config, audio=audio)

    # Print the transcript of the recognized audio
    if response.results:
        text = response.results[0].alternatives[0].transcript
        with open('input/input.txt', 'w', encoding='utf-8') as file:
            file.write(text)
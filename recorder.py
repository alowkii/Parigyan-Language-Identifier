import tkinter as tk
from tkinter import font
from voice_to_text import recognize_voice
import sounddevice as sd
import soundfile as sf
import time
import os

recording = False
audio_data = None
start_time = None
def record_voice():
    # Global variables to keep track of recording state, audio data, and start time
    global recording
    global audio_data
    global start_time

    # Set the default samplerate
    sd.default.samplerate = 44100

    # Function to toggle recording
    def toggle_recording():
        global recording
        global audio_data
        global start_time
        if not recording:
            # Start recording
            start_time = time.time()
            recording = True
            start_button.config(text="Stop Recording", bg="#ff0000", fg="black")
            audio_data = sd.rec(5 * sd.default.samplerate, samplerate=sd.default.samplerate, channels=2, dtype="int16")
            start_timer()
        else:
            # Stop recording
            recording = False
            start_button.config(text="Start Recording", bg="#1E1E1E",fg="white")
            sd.stop()
            sd.wait()
            save_button.config(state=tk.NORMAL)


    # Function to update the recording timer
    def start_timer():
        global start_time
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Recording : {int(elapsed_time)} seconds")
        if recording:
            timer_label.after(1000, start_timer)


    # Function to save the recorded audio
    def save_audio():
        global audio_data

        if audio_data is not None:
            filename = 'input/input.wav'
            if os.path.exists(filename):
                os.remove(filename)
            sf.write(filename, audio_data, samplerate=sd.default.samplerate)
            recognize_voice()
            root.destroy()

    # Create the main Tkinter window
    root = tk.Tk()
    root.geometry("600x500")
    root.resizable(False, False)
    root.title("Parigyan Voice Recorder")
    root.config(bg="#1E1E1E")

    # Load the custom font
    custom_font = font.Font(family="Unicorns are Awesome", size=40)

    # Create a label with the custom font for the title
    label = tk.Label(root, text="Record voice", font=("Poppins Thin", 32), bg="#1E1E1E",fg="#ffffff" )
    label.place(relx=0.5, rely=0.02, anchor="n")

    # Create the Save Audio button
    save_button = tk.Button(root, text="Save Audio", font=("Poppins", 20), bg="white", fg="#1E1E1E",\
                            command=save_audio, state=tk.DISABLED, width=15)
    save_button.place(relx=0.5, rely=0.22, anchor="n")

    # Create the Start Recording button
    start_button = tk.Button(root, text="Start Recording",font=("Poppins", 20), command=toggle_recording,\
                            bg="#1E1E1E",fg="white", width=15)
    start_button.place(relx=0.5, rely=0.62, anchor="n")

    # Create the recording timer label
    timer_label = tk.Label(root, text="", font=("Poppins Thin", 30), bg="#1E1E1E", fg="grey")
    timer_label.place(relx=0.5, rely=0.42, anchor="n")

    # Start the Tkinter event loop
    root.mainloop()
    
## record_voice()

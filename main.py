from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
from identify_language import identify_language
from image_to_text import extract_text_from_image
from recorder import record_voice
import shutil
import os

def predict_language():
    prediction = identify_language()
    messagebox.showinfo("Prediction", f"The predicted language is: {prediction}")

def load_image():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            destination_path = 'images/' + file_path.split('/')[-1]
            shutil.copy(file_path, destination_path)
            if os.path.exists('images/image.png'):
                os.remove('images/image.png')
            os.rename(destination_path, 'images/image.png')
            extract_text_from_image()
            predict_language()
    except shutil.SameFileError:
        print("Choose another file in another directory.")

def predict_language_from_entry():
    def on_submit():
        text = entry.get()
        if text:
            with open('input/input.txt', 'w', encoding='utf-8') as file:
                file.write(text)
            window_text_loader.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    window_text_loader = tk.Tk()
    window_text_loader.title("Text Loader")
    window_text_loader.configure(bg="#1E1E1E")
    window_text_loader.geometry("450x200")
    window_text_loader.resizable(False, False)

    tk.Label(window_text_loader, text="Enter text:", font=("Poppins", 12), bg="#1E1E1E", fg="#FFFFFF").pack(pady=10)
    
    entry_frame = tk.Frame(window_text_loader)
    entry_frame.pack(pady=5)

    entry = tk.Entry(entry_frame, width=30, font=("Poppins", 12))
    entry.pack(side="left", padx=5)
    
    clear_button = tk.Button(entry_frame, text="Clear", width=5 ,command=lambda: entry.delete(0, tk.END), background="#1E1E1E", fg="white")
    clear_button.pack(side="left", padx=5)

    submit_button = tk.Button(window_text_loader, text="Load Text", command=on_submit, font=("Poppins", 12), bg="#1E1E1E", fg="white")
    submit_button.pack(pady=20)

    window_text_loader.mainloop()

BASE_DIR = Path.cwd()
ASSETS_PATH = BASE_DIR / "assets"
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("900x500")
window.configure(bg = "#1E1E1E")


canvas = Canvas(
    window,
    bg = "#1E1E1E",
    height = 500,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: load_image(),
    relief="flat"
)
button_1.place(
    x=123.0,
    y=164.0,
    width=171.0,
    height=173.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: record_voice(),
    relief="flat"
)
button_2.place(
    x=365.0,
    y=164.0,
    width=171.0,
    height=173.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: predict_language_from_entry(),
    relief="flat"
)
button_3.place(
    x=613.0,
    y=163.0,
    width=174.0,
    height=176.0
)

canvas.create_text(
    900/2,
    100/2,
    anchor="center",
    text="Language Identifier",
    fill="#FFFFFF",
    font=("Poppins Thin", 40 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: predict_language(),
    relief="flat"
)
button_4.place(
    x=770.0,
    y=370.0,
    width=100.0,
    height=99.77922058105469
)
window.resizable(False, False)
window.mainloop()

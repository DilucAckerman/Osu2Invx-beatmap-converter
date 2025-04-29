import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
from pathlib import Path
from pydub import AudioSegment
import os

def convert_osz_file(input_path, output_path):
    try:
        temp_dir = Path("temp_osz")
        temp_dir.mkdir(exist_ok=True)

        # Step 1: Unzip the .osz file
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Step 2: Convert .mp3 to .ogg
        for file in temp_dir.glob("*.mp3"):
            audio = AudioSegment.from_mp3(file)
            new_file = file.with_suffix('.ogg')
            audio.export(new_file, format="ogg")
            file.unlink()  # Delete original .mp3

        # Step 3: Edit .osu files
        for osu_file in temp_dir.glob("*.osu"):
            with open(osu_file, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
                content = f.read()
            content = content.replace(".mp3", ".ogg") 
            with open(osu_file, 'w', encoding='utf-8') as f:  # Write back with UTF-8 encoding
                f.write(content)

        # Step 4: Rezip the files
        with zipfile.ZipFile(output_path, 'w') as zip_ref:
            for file in temp_dir.rglob("*"):
                zip_ref.write(file, file.relative_to(temp_dir))

        # Cleanup
        for file in temp_dir.rglob("*"):
            file.unlink()
        temp_dir.rmdir()

        messagebox.showinfo("Success", "File converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("osu! Beatmap files", "*.osz")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".osz", filetypes=[("osu! Beatmap files", "*.osz")])
        if output_path:
            convert_osz_file(file_path, output_path)

# Create the main application window
root = tk.Tk()
root.title("Invxn Converter")
root.geometry("400x200")

# UI Elements
label = tk.Label(root, text="Convert osu!mania beatmaps for Invaxion", font=("Arial", 12))
label.pack(pady=20)

select_button = tk.Button(root, text="Select .osz File", command=select_file, font=("Arial", 10))
select_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=10)

# Run the application
root.mainloop()

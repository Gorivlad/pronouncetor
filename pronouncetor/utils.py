import subprocess
from pydub import AudioSegment
import tkinter as tk
from tkinter import scrolledtext
import os


def convert_to_wav(input_file, output_file):
    command = [
        'ffmpeg', '-y', '-loglevel', 'error', '-i', input_file,
        '-c:a', 'pcm_s16le', output_file
        ]
    subprocess.run(command)
    print("Audio file converted into .wav")


def extract_and_save_clips(file_path, time_segments, output_path):
    '''
    Extract clips and save it as .wav file using pydub
    Time segments == list of touples
    '''
    audio = AudioSegment.from_file(file_path)
    extracted_audio = AudioSegment.empty()

    for start, end in time_segments:
        start_ms = start * 1000
        end_ms = end * 1000
        extracted_audio += audio[start_ms:end_ms]

    extracted_audio.export(output_path, format="wav")
    print(f"Extracted audio saved to {output_path}")


def extract_first_30_seconds(input_path="", output_path=""):
    # Load the audio file
    audio = AudioSegment.from_file(input_path)
    audio_example = audio[:30000]
    output_path = output_path

    audio_example.export(output_path, format="wav")
    print(f"Extracted audio example saved to {output_path}")


def display_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()

        # Create the main window
        root = tk.Tk()
        root.title("Transcript Viewer")

        # Create a ScrolledText widget
        text_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=100, height=30,
            font=("Times New Roman", 12)
            )
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Insert the file contents into the text area
        text_area.insert(tk.END, contents)

        # Start the GUI event loop
        root.mainloop()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def validate_audio_file(file_path):
    audio_extensions = [
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.mp4'
        ]

    if os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in audio_extensions:
            audio = AudioSegment.from_file(file_path)
            duration_in_minutes = len(audio) / (1000 * 60)

            if duration_in_minutes < 1:
                return "Error: The audio is too short."
            elif duration_in_minutes > 15:
                return "Error: The audio is too long."
            else:
                return True
        else:
            return "Error: The file is not an audio file."
    else:
        return "Error: Invalid file path."

import subprocess
from pydub import AudioSegment
import tkinter as tk
from tkinter import scrolledtext


def convert_to_wav(input_file, output_file):
    command = ['ffmpeg', '-y','-loglevel', 'quiet', '-i', input_file, '-c:a', 'pcm_s16le', output_file]
    subprocess.run(command)
    print("Audio file converted into .wav")


def extract_and_save_clips(file_path, time_segments, output_path = "../data/processed/extracted.wav"):
        # Extract clips and save it as .wav file using pydub
        # Time segments == list of touples
        audio = AudioSegment.from_file(file_path)
        extracted_audio = AudioSegment.empty()

        for start, end in time_segments:
            start_ms = start * 1000
            end_ms = end * 1000 
            extracted_audio += audio[start_ms:end_ms]

        extracted_audio.export(output_path, format="wav")
        print(f"Extracted audio saved to {output_path}")


def extract_first_30_seconds():
    # Load the audio file
    audio = AudioSegment.from_file("../data/processed/extracted.wav")
    audio_example = audio[:30000]
    output_path = "../data/processed/extracted_example.wav"

    audio_example.export(output_path, format="wav")
    print(f"Extracted audio example saved to {output_path}")

    
def time_extraction_touples(diarization_result, target_speaker):
    # Returns list of touples [{start,end},{start,end}...]
    times = []
    for turn, _, speaker in diarization_result.itertracks(yield_label=True):
        if speaker == target_speaker:
            times.append((turn.start, turn.end))
    print(f"Timestamps of {target_speaker} extracted as a list of touples")
    return times


def display_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()

        # Create the main window
        root = tk.Tk()
        root.title("Transcript Viewer")

        # Create a ScrolledText widget
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Times New Roman", 12))
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Insert the file contents into the text area
        text_area.insert(tk.END, contents)

        # Start the GUI event loop
        root.mainloop()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
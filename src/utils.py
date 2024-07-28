import subprocess
from pydub import AudioSegment

def convert_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:a', 'pcm_s16le', output_file]
    subprocess.run(command)


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


def save_diarization_result(diarization_result):
    output_path = "../data/processed/diarization_result.txt"
    with open(output_path, "w") as file:
        file.write(str(diarization_result))

    print(f"Diarization result saved to {output_path}")
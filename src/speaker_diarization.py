from pyannote.audio import Pipeline
from pyannote.core import Segment
from pyannote.audio import Audio
import matplotlib.pyplot as plt
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment

class DiarizationModel:
    def __init__(self, model_name="pyannote/speaker-diarization-3.0"):
        self.pipeline = Pipeline.from_pretrained(model_name)

    def infer_file(self, file_path, num_speakers=2):
        # Diarization of audio
        # Returns list of time-stamped segments e.g. [ 00:00:41.594 -->  00:00:44.226] AH SPEAKER_00
        with ProgressHook() as hook:
            diarization_result = self.pipeline(file_path, hook=hook, num_speakers=num_speakers)
        print("Diarization performed")
        return diarization_result

    def plot_diarization(self, diarization_result, title="Diarization for the file"):
        fig, ax = plt.subplots(figsize=(10, 2))
        for turn, _, speaker in diarization_result.itertracks(yield_label=True):
            ax.plot([turn.start, turn.end], [speaker, speaker], lw=6)
        ax.set_yticks(list(diarization_result.labels()))
        ax.set_yticklabels([f"Speaker {label}" for label in diarization_result.labels()])
        ax.set_xlabel("Time (s)")
        ax.set_title(title)
        plt.show()
        print("Diarization plot displayed")

    def time_extraction_list(self, diarization_result, target_speaker):
        # Returns list of times [start,end,start,end...]
        times = []
        for turn, _, speaker in diarization_result.itertracks(yield_label=True):
            if speaker == target_speaker:
                times.append(turn.start)
                times.append(turn.end)
        print(f"Timestamps of {target_speaker} extracted as a list")
        return times

    def time_extraction_touples(self, diarization_result, target_speaker):
        # Returns list of touples [{start,end},{start,end}...]
        times = []
        for turn, _, speaker in diarization_result.itertracks(yield_label=True):
            if speaker == target_speaker:
                times.append((turn.start, turn.end))
        print(f"Timestamps of {target_speaker} extracted as a list of touples")
        return times

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
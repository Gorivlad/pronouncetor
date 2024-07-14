from pyannote.audio import Pipeline
from pyannote.core import Segment
from pyannote.audio import Audio
import matplotlib.pyplot as plt
from pyannote.audio.pipelines.utils.hook import ProgressHook

class DiarizationModel:
    def __init__(self, model_name="pyannote/speaker-diarization-3.0"):
        self.pipeline = Pipeline.from_pretrained(model_name)

    def infer_file(self, file, num_speakers=2):
        with ProgressHook() as hook:
            diarization_result = self.pipeline(file, hook=hook, num_speakers=num_speakers)
        return diarization_result

    def display_results(self, diarization_result):
        print("Diarization_results")
        print(diarization_result)

    def plot_diarization(self, diarization_result, title="Diarization for the file"):
        fig, ax = plt.subplots(figsize=(10, 2))
        for turn, _, speaker in diarization_result.itertracks(yield_label=True):
            ax.plot([turn.start, turn.end], [speaker, speaker], lw=6)
        ax.set_yticks(list(diarization_result.labels()))
        ax.set_yticklabels([f"Speaker {label}" for label in diarization_result.labels()])
        ax.set_xlabel("Time (s)")
        ax.set_title(title)
        plt.show()

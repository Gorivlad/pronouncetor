from pyannote.audio import Pipeline
from pyannote.core import Segment
from pyannote.audio import Audio
import matplotlib.pyplot as plt
from pyannote.audio.pipelines.utils.hook import ProgressHook
from speaker_diarization import DiarizationModel

def main():
    # Get the file path from user input
    file_path = input("Insert filepath: ")

    # Initialize the diarization model
    diarization_model = DiarizationModel()

    # Perform diarization on the audio file
    diarization_result = diarization_model.infer_file(file_path)

    #Display results
    #diarization_model.display_results(diarization_result)

if __name__ == "__main__":
    main()

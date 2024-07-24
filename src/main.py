from speaker_diarization import DiarizationModel, extract_and_save_clips
from feedback_generator import Feedback
import whisper

def main():
    # Get the file path from user input
    file_path = input("Insert filepath: ")

    # Initialize the diarization model
    diarization_object = DiarizationModel()

    # Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(file_path)

    #Extract timestamps for target speaker
    time_extraction = diarization_object.time_extraction_touples(diarization_result, "SPEAKER_00")

    #Extract and save speaker segment audio
    extract_and_save_clips(file_path, time_extraction)

    #Transcribe one speaker and print text
    model = whisper.load_model("base.en")
    result = model.transcribe(audio="../data/processed/extracted.wav")
    print(result["text"][:200] + "...")

    #Provide feedback
    #feedback = Feedback(result)
    #print(feedback.feedback_base())





if __name__ == "__main__":
    main()

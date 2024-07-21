from speaker_diarization import DiarizationModel, extract_and_save_clips
import whisper

def main():
    # Get the file path from user input
    #file_path = input("Insert filepath: ")

    # Temporary integrated file_path for testing
    file_path = "/mnt/c/Personal/Coding/Study/audio_data/Callhome/audio_7.wav"

    # Initialize the diarization model
    diarization_object = DiarizationModel()

    # Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(file_path)

    #Extract timestamps for target speaker
    time_extraction = diarization_object.time_extraction_touples(diarization_result, "SPEAKER_01")

    #Extract and save speaker segment audio
    extract_and_save_clips(file_path, time_extraction)

    #Transcribe one speaker and print text
    model = whisper.load_model("base.en")
    result = model.transcribe(audio="../data/processed/extracted.wav")
    print(result["text"])




if __name__ == "__main__":
    main()

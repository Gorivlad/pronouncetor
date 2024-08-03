from speaker_diarization import DiarizationModel
from feedback_generator import Feedback
from utils import convert_to_wav, extract_and_save_clips, save_transcription_to_txt, display_txt_file, extract_first_30_seconds

import whisper


def main():
    # Get the file path from user input
    file_path = input("Insert filepath: ")


    # If not .wav then convert the file into .wav
    if not file_path.lower().endswith('.wav'):
        convert_to_wav(file_path, "../data/processed/converted.wav")
        file_path = "../data/processed/converted.wav"



    #Initialize the diarization model
    diarization_object = DiarizationModel()


    #Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(file_path)


    correct_target_speaker = False
    speaker_n = 0
    
    # Aim the target speaker
    while correct_target_speaker == False:


        #Extract timestamps for target speaker
        time_extraction = diarization_object.time_extraction_touples(diarization_result, f"SPEAKER_0{str(speaker_n)}")


        #Extract and save speaker segment audio
        extract_and_save_clips(file_path, time_extraction)



        # transcript example
        audio_example = extract_first_30_seconds()
        print("First 30s extracted")
        model = whisper.load_model("tiny.en")
        result = model.transcribe("../data/processed/extracted_example.wav")
        

        #Print example of the speaker
        print(result["text"] + "...")


        #Verify correctnes of target speaker
        is_target_speaker = input("Is this target speaker? Y/n: ")
        if is_target_speaker.lower() == "y":
            correct_target_speaker = True
        else:
            speaker_n += 1
    # Transcribe target speaker
    print(f"Transcripting SPEAKER_0{str(speaker_n)}")
    model = whisper.load_model("base.en")
    result = model.transcribe(audio = "../data/processed/extracted.wav", word_timestamps = True)


    # Save result of transcription
    transcript_path = "../data/processed/transcript.txt"
    save_transcript_to_txt(result, "../data/processed/transcript.txt" )

    # Display the transcript
    display_txt_file(transcript_path)


    #Provide feedback
    feedback = Feedback(result)
    print(feedback.feedback_base())

if __name__ == "__main__":
    main()

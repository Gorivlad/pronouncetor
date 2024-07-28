from speaker_diarization import DiarizationModel
from feedback_generator import Feedback
from utils import convert_to_wav, extract_and_save_clips

import whisper


def main():
    # Get the file path from user input
    file_path = input("Insert filepath: ")


    # If not .wav then convert the file into .wav
    if not file_path.lower().endswith('.wav'):
        convert_to_wav(file_path, "../data/processed/converted.wav")
        file_path = "../data/processed/converted.wav"
        print("Audio file converted into .wav")


    #Initialize the diarization model
    diarization_object = DiarizationModel()


    #Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(file_path)


    correct_target_speaker = False
    speaker_n = 0
    

    while correct_target_speaker == False:


        #Extract timestamps for target speaker
        time_extraction = diarization_object.time_extraction_touples(diarization_result, f"SPEAKER_0{str(speaker_n)}")


        #Extract and save speaker segment audio
        extract_and_save_clips(file_path, time_extraction)


        #Transcribe the speaker and print text
        model = whisper.load_model("base.en")
        result = model.transcribe(audio = "../data/processed/extracted.wav")
        

        #Print example of the speaker
        print(result["text"][:200] + "...")


        #Verify correctnes of target speaker
        is_target_speaker = input("Is this target speaker? Y/n: ")
        if is_target_speaker.lower() == "y":
            correct_target_speaker = True
        else:
            speaker_n += 1

        
    #Provide feedback
    feedback = Feedback(result)
    print(feedback.feedback_base())

import whisper
import threading

from speaker_diarization import DiarizationModel
from feedback_generator import Feedback, sarcastic_concise
from utils import convert_to_wav, extract_and_save_clips, display_txt_file, extract_first_30_seconds
from transcript import filter_transcript, save_transcript_to_txt


def main():

    converted_audio_path = "../data/processed/converted.wav"
    extracted_clip = "../data/processed/extracted.wav"
    transcript_path = "../data/processed/transcript.txt"


    #Get the file path from user input
    file_path = input("Insert filepath: ")

    
    #If not .wav then convert the file into .wav
    if not file_path.lower().endswith('.wav'):
        convert_to_wav(file_path, converted_audio_path)


    #Initialize the diarization model
    diarization_object = DiarizationModel()


    #Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(converted_audio_path)

    
    #Aim the target speaker
    correct_target_speaker = False
    speaker_n = 0
    while correct_target_speaker == False:

    
        #Extract timestamps of one speaker
        time_extraction = diarization_object.time_extraction_touples(diarization_result, f"SPEAKER_0{str(speaker_n)}")


        #Extract and save the speaker segment audio
        extract_and_save_clips(converted_audio_path, time_extraction, output_path=extracted_clip)



        #Transcript example
        audio_example = extract_first_30_seconds()
        print("First 30s extracted")
        model = whisper.load_model("tiny.en")
        result = model.transcribe(extracted_clip)
        

        #Print example of the speaker
        print(result["text"][:250] + "...")


        #Ask if it's the target speaker
        is_target_speaker = input("Is this target speaker? Y/n: ")
        if is_target_speaker.lower() == "y":
            correct_target_speaker = True
        else:
            speaker_n += 1
    #Transcribe the target speaker
    print(f"Transcripting SPEAKER_0{str(speaker_n)}")
    model = whisper.load_model("base.en")
    result = model.transcribe(audio=extracted_clip, word_timestamps = True)


    #Save result of transcription as .txt
    save_transcript_to_txt(result, transcript_path)


    #Save result of transcription as variable
    filtered_result = filter_transcript(result)


    #Create and start a thread for the transcript
    thread = threading.Thread(target=display_txt_file, args=(transcript_path,))
    thread.start()


    #Provide feedback
    feedback = Feedback(transcription = filtered_result, system_query = sarcastic_concise)
    print(feedback.first_message())
    user_input = " "
    while user_input.lower() != "exit":
        user_input = input("you: ")
        if user_input.lower() == "exit":
            break
        else:
            print(feedback.continuous_chat(user_input))

if __name__ == "__main__":
    main()

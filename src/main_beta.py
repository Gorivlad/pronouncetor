# Main beta transcript extracted and whole file then prompt ai to map them for feedback 
import whisper
import threading

from speaker_diarization import DiarizationModel
from feedback_generator import Feedback, system_query_beta
from utils import convert_to_wav, extract_and_save_clips, display_txt_file, extract_first_30_seconds
from transcript import filter_transcript, save_transcript_to_txt


def main():

    converted_audio_path = "../data/processed/converted.wav"
    extracted_clip = "../data/processed/extracted.wav"
    transcript_path = "../data/processed/transcript.txt"
    whole_file_transcript_path = "../data/processed/transcript_whole_file.txt"


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
        print("transcribing example")
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
    #Transcribe the target speaker and save result 
    print(f"Transcripting SPEAKER_0{str(speaker_n)}. May take a while...")
    model = whisper.load_model("small.en")
    result = model.transcribe(audio=extracted_clip)
    save_transcript_to_txt(result, transcript_path)
    filtered_result = filter_transcript(result)


    #Transcribe the whole file and save the result
    print("Transcripting whole file. May take a while...")
    model = whisper.load_model("small.en")
    result_whole = model.transcribe(audio=converted_audio_path, word_timestamps = True)
    save_transcript_to_txt(result_whole, whole_file_transcript_path)
    filtered_result_whole = filter_transcript(result_whole)


    #Create and start a thread for the whole transcript
    thread = threading.Thread(target=display_txt_file, args=(whole_file_transcript_path,))
    thread.start()

    #Ask for system style
    system_query_name = ""
    what_system = input("Short or complex feedback? S/c: ")
    if what_system.lower() == "s":
        system_query_name = "short_"
    else:
        system_query_name = "complex_"
    what_system = input("Serious or funny feedback? S/f: ")
    if what_system.lower() == "s":
        system_query_name = system_query_name + "serious"
    else:
        system_query_name = system_query_name + "funny"


    #Provide feedback
    feedback = Feedback(transcription = filtered_result_whole + filtered_result, system_query = system_query_beta[system_query_name])
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

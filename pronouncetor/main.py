import whisper
import threading

from speaker_diarization import DiarizationModel
from feedback_generator import Feedback, system_query
import utils
from transcript import filter_transcript, save_transcript_to_txt


def main():

    converted_audio_path = "../data/processed/converted.wav"
    extracted_clip = "../data/processed/extracted.wav"
    audio_example_path = "../data/processed/extracted_example.wav"
    transcript_path = "../data/processed/transcript.txt"

    # Get the file path and nun of speakers from the user input and validate it
    correct_audio = False
    while correct_audio is not True:
        file_path = input("Insert filepath: ")
        correct_audio = utils.validate_audio_file(file_path)

    while True:
        try:
            num_speakers = int(input(
                "How many speakers are on the recording? Min 1, max 3: "
                ))
            if 1 <= num_speakers <= 3:
                break
            else:
                print("Error: Please enter a number between 1 and 3.")
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer.")

    # If not .wav then convert the file into .wav
    if not file_path.lower().endswith('.wav'):
        utils.convert_to_wav(file_path, converted_audio_path)

    # Initialize the diarization model
    diarization_object = DiarizationModel()

    # Perform diarization on the audio file
    diarization_result = diarization_object.infer_file(
        converted_audio_path, num_speakers=num_speakers
        )

    # Loop until the correct target speaker is identified
    correct_target_speaker = False
    speaker_n = 0
    while correct_target_speaker is False:

        # Extract timestamps of one speaker
        time_extraction = diarization_object.time_extraction_touples(
            diarization_result, f"SPEAKER_0{str(speaker_n)}"
            )

        # Extract and save the speaker segment audio
        utils.extract_and_save_clips(
            converted_audio_path, time_extraction, output_path=extracted_clip
            )

        # Transcript example
        utils.extract_first_30_seconds(
            input_path=extracted_clip, output_path=audio_example_path
            )
        print("transcribing example...")
        model = whisper.load_model("tiny.en")
        result = model.transcribe(audio_example_path)
        print("Example transcripted")

        # Print example of the speaker
        print(result["text"][:250] + "...")

        # Ask if example is the target speaker
        is_target_speaker = input("Is this target speaker? Y/n: ")
        if is_target_speaker.lower() == "y":
            correct_target_speaker = True
        if speaker_n == num_speakers:
            print("Last speaker reached")
            break
        else:
            speaker_n += 1
    # Transcribe the target speaker
    print(f"Transcripting SPEAKER_0{str(speaker_n)}. May take a while...")
    model = whisper.load_model("small.en")
    result = model.transcribe(audio=extracted_clip, word_timestamps=True)

    # Save result of transcription as .txt
    save_transcript_to_txt(result, transcript_path)

    # Save result of transcription as variable
    filtered_result = filter_transcript(result)

    # Create and start a thread for the transcript
    thread = threading.Thread(
        target=utils.display_txt_file, args=(transcript_path,)
        )
    thread.start()

    # Determine the style and tone of the system's feedback
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

    # Generate and provide feedback
    feedback = Feedback(
        transcription=filtered_result,
        system_query=system_query[system_query_name]
        )
    print(feedback.first_message())
    user_input = " "
    while user_input.lower() != "exit":
        print("for exit type 'exit'")
        user_input = input("you: ")
        if user_input.lower() == "exit":
            break
        else:
            print(feedback.continuous_chat(user_input))


if __name__ == "__main__":
    main()

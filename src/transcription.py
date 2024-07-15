import whisper

def transcribe_audio(file_path):
    # Load the tiny model
    model = whisper.load_model("tiny")

    # Load and transcribe the audio file
    result = model.transcribe(file_path)

    # Print the transcribed text
    print(result["text"])

# Provide the path to your audio file
audio_file_path = "/mnt/c/Personal/Coding/Study/audio_data/Callhome/audio_7.wav"

# Call the function to transcribe audio
transcribe_audio(audio_file_path)

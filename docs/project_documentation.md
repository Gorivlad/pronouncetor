Introduction

This application assists language learners in improving their verbal skills by recording, analyzing,
 and providing specific feedback on their speech. It utilizes audio processing and machine learning
 to offer insights into language proficiency and pronunciation.

Scope:

	Speaker diarization: Uses Pyannote Audio for speaker diarization, identifying and segmenting speakers in audio files.
		     Pre-trained model name. Default: "pyannote/speaker-diarization-3.0".

	Speaker recognition: The code loops through audio segments, transcribes them, and asks the user to confirm the
		     target speaker until identified.

	Transcription: The code transcribes the identified speaker's audio segment using Whisper's ASR model, saving the transcription
	       to a text file and formatting it for further processing and feedback generation.

	Feedback generation: Feedback generation involves creating a personalized response based on the transcribed text, where the
		     user selects the style (short or complex) and tone (serious or funny). The system then generates
		     feedback accordingly and engages in a continuous conversation until the user exits.
	Beta: This version transcribes both the target speaker's segment and the entire audio file, saving each separately. It then 
	      combines these transcriptions for feedback generation, enhancing the completeness and context of the feedback compared
	      to the previous version, which only transcribed the target speaker.


Architecture overview:

			root/
			├── data/
			│   ├── processed/
			│   ├── raw/
			├── docs/
			│   └── project_documentation.md
			├── src/
			│   ├── __pycache__/
			│   ├── feedback_generator.py
			│   ├── main.py
			│   ├── main_beta.py
			│   ├── speaker_diarization.py
			│   ├── transcript.py
			│   └── utils.py
			├── tests/
			│   ├── test_audiorecorder.py
			│   ├── test_feedback_generator.py
			│   ├── test_interface.py
			│   ├── test_speaker_diarization.py
			│   └── test_transcription.py
			├── .gitignore
			├── README.md
			└── requirements.txt



OpenAI API integration: https://platform.openai.com/docs/quickstart?context=node 


How to Contribute: TODO


Testing Strategy: TODO


Running Tests: TODO


Common Issues: TODO


License:


Contact Information:

Citation:
	Pyannote Audio for Speaker Diarization: 
		Hervé Bredin, Antoine Laurent, et al. (2021). pyannote.audio: neural building blocks for speaker diarization.
		 In Proceedings of ICASSP 2021. Available: https://github.com/pyannote/pyannote-audio
	Whisper's ASR Model:
		Radford, A., Kim, J. W., Xu, T., et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision. 
		Available: https://github.com/openai/whisper
	OpenAI API for Feedback Generation:
		OpenAI API Documentation. (n.d.). OpenAI. Available: https://platform.openai.com/docs/quickstart
	


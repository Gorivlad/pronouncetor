Introduction

This application assists language learners in improving their verbal skills by recording, analyzing,
 and providing specific feedback on their speech. It utilizes audio processing and machine learning
 to offer insights into language proficiency and pronunciation.

Operations Overview:

Speaker diarization:
Uses Pyannote Audio for speaker diarization, identifying and segmenting speakers 
in audio files.
Pre-trained model Default: "pyannote/speaker-diarization-3.0".

Speaker recognition:
The code loops through audio segments, transcribes them, and asks the user to confirm the target speaker until identified or untill last speaker is reached.

Transcription:
The code transcribes the identified speaker's audio segment using Whisper's ASR model, saving the transcription as a text file and formatting it for further processing and feedback generation.
Default for examples in speaker recognition block: tiny.en
default for main transcript: small.en

Feedback generation:
Feedback generation involves creating a personalized response based on the transcribed text, where the user selects the style (short or complex) and tone (serious or funny). The system then generates feedback accordingly and engages in a continuous conversation until the user exits.
Default chatbot: gpt-4o

Beta:
This version transcribes both the target speaker's segment and the entire audio file, saving each separately. Then it combines these transcriptions for feedback generation, enhancing the completeness and context of the feedback compared to the alfa version, which only transcribed the target speaker.


Architecture overview:

			root/
			├── data/
			│   ├── processed/
			│   ├── raw/
			├── docs/
			│   └── pronouncetor_doc.md
			├── pronouncetor/
			│   ├── __pycache__/
			│   ├── feedback_generator.py
			│   ├── main.py
			│   ├── main_beta.py
			│   ├── speaker_diarization.py
			│   ├── transcript.py
			│   └── utils.py
			├── tests/
			│   ├── conftest.py
			│   ├── test_feedback_generator.py
			│   ├── test_utils.py
			│   ├── test_speaker_diarization.py
			│   └── test_transcription.py
			├── .gitignore
			├── README.md
			└── requirements.txt



Testing Strategy: Basic unit tests to verify the functionality of key functions and components. Using the pytest framework.
Currently, the tests are not automated and must be executed manually with command pytest


Common Issues:
Using "pyannote/speaker-diarization-3.0," Whisper ASR, and a GPT-4-based chatbot together can result in a higher error rate due to:

Speaker Diarization: Potential misidentification or segmentation errors. For details, visit https://huggingface.co/pyannote/speaker-diarization-3.1.

Whisper ASR: Transcription inaccuracies, especially in noisy conditions or with diverse accents. See https://github.com/openai/whisper#readme for optimization tips.

GPT-4 Chatbot: Possible incorrect responses. See https://openai.com/index/hello-gpt-4o.


Citation:
	Pyannote Audio for Speaker Diarization: 
		Hervé Bredin, Antoine Laurent, et al. (2021). pyannote.audio: neural building blocks for speaker diarization.
		 In Proceedings of ICASSP 2021. Available: https://github.com/pyannote/pyannote-audio
	Whisper's ASR Model:
		Radford, A., Kim, J. W., Xu, T., et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision. 
		Available: https://github.com/openai/whisper
	OpenAI API for Feedback Generation:
		OpenAI API Documentation. (n.d.). OpenAI. Available: https://platform.openai.com/docs/quickstart
	


from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()
# Space for different queries defined as Methods of object Feedback


class Feedback:
    def __init__(self, transcription):
        self.client = OpenAI()
        self.transcription = transcription


    def feedback_base(self):
        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
    {"role": "system", "content": ("You are a witty expert that provides constructive feedback"
    " on the english grammar of individuals based on their language use in a conversation. "
    "I will provide you with a transcript of one speaker's part of a conversation insluding segments ID,"
    "timestamps for segments and also words with timestamps and probability rate provided by "
    "whisper-ai base.en model. Your task is to analyze"
    " the grammar used by this speaker and give feedback aimed at improving their grammar skills."
    "With pinpointing when exactly was the misstake maked and sarcastic humor. Also provide 5 words with lowest confidence."
    " Keep your answer under 80 words and focus it on improvement tips.")},
    {"role": "user", "content": f"{self.transcription}"}
  ],
  max_tokens = 120
        )
        return (f"Here is feedback on your Grammar\n{completion.choices[0].message.content}")
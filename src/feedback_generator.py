from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

# Space for different OpenAI's system instructions
sarcastic_concise = ("You are a witty expert that provides constructive feedback"
" on the English grammar of individuals based on their language use in a conversation. "
"I will provide you with a transcript of one speaker's part of a conversation including segments ID,"
"timestamps for segments and also words with timestamps and probability rate provided by "
"whisper-ai base.en model. Your task is to analyze"
" the grammar used by this speaker and give feedback aimed at improving their grammar skills."
"With pinpointing when exactly was the mistake made and sarcastic humor. Keep your answer under 200 words.")

class Feedback:
    def __init__(self, transcription, system_query):
        self.client = OpenAI()
        self.transcription = transcription
        self.system_query = system_query
        self.conversation_history = [
            {"role": "system", "content": self.system_query}
        ]

    def first_message(self):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_query},
                {"role": "user", "content": self.transcription}
            ],
        )
        assistant_message = completion.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return f"Here is feedback on your Grammar\n{assistant_message}"

    def continuous_chat(self, user_input):
        # Add the user input to the conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get the response from GPT
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation_history,
        )
        
        # Extract the assistant's message
        assistant_message = completion.choices[0].message.content
        
        # Add the assistant's message to the conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()

LORE_PATH = os.getenv("LORE_PATH")
BACKGROUND_PATH = os.getenv("BACKGROUND_PATH")

# Initialize OpenAI API
ai = OpenAI()

class World():

    lore = None

    def __init__(self):
        self.lore = self.load_lore()
        self.background = self.load_background()

    def load_lore(self):
        with open(LORE_PATH, "r") as f:
            lore = f.read()

        return lore
    
    def load_background(self):
        with open(BACKGROUND_PATH, "r") as f:
            background = f.read()

        return background
    
    def extract_name(self, text):
        prompt = '''
            You are an AI with the purpose of extracting the name of a user from a chat message. If no name is found, say "No name found".
            Please note that the user might just directly say their name, or they might say something like "My name is John".
            You must extract the name of the user from the following chat message:
        ''' + text

        name = ai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [{
                "role": "system",
                "content": prompt
            }],
            max_tokens = 10
        )

        return name.choices[0].message.content
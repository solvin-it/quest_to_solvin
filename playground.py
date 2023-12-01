import dotenv
import os
from openai import OpenAI
import logging

logging.basicConfig(level=logging.DEBUG)

dotenv.load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
ai = OpenAI()

if __name__ == "__main__":
    messages = [{
        'role': 'system',
        'content': '''
            You are an AI with the purpose of generating NPC backstories for a medieval fantasy game. You must create one NPC and provide the following:
            - Name: The name of the NPC
            - Age: The age of the NPC
            - Profession: The profession of the NPC in the game world
            - Personality: A brief description of the NPC's personality
            - Description: A brief description of the NPC's appearance and reputation
        '''
    }]

    response = ai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )

    logging.debug(f"Choice 0: {response.choices[0].message}")
import dotenv
import os
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
ai = OpenAI()

class NPC():

    def __init__(self, name=None, age=None, profession=None, personality=None, description=None, image=None):
        if name is None:
            information = self.generate_background()
            self.name = information['Name']
            self.age = information['Age']
            self.profession = information['Profession']
            self.personality = information['Personality']
            self.description = information['Description']
        else:
            self.name = name
            self.age = age
            self.profession = profession
            self.personality = personality
            self.description = description
            self.image = image

    def generate_response(self, messages):
        system_content = f'''
            You are {self.name}, a {self.age} year old {self.profession} who is {self.personality}. You are known for {self.description}.

            You should respond in tone and style appropriate for your character. Remember that this is a medieval fantasy game, so you should use language that is appropriate for that setting and character.
            You should also repond in conversational style and not speak in long paragraphs unless the topic requires it.

            Respond in less than 150 words.
        '''

        messages.insert(0, {
            "role": "system",
            "content": system_content
        })

        response = ai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )

        return response.choices[0].message.content

    def generate_background(self, settings=None):
        try:
            generation_prompt = '''
                You are an AI with the purpose of generating NPC backstories for a medieval fantasy game. You must create one NPC and provide the following:
                    - Name: The name of the NPC
                    - Age: The age of the NPC
                    - Profession: The profession of the NPC in the game world
                    - Personality: A brief description of the NPC's personality
                    - Description: A brief description of the NPC's appearance and reputation

                Please note that the NPC's name, age, profession, personality, and description must be separated by a colon. For example, "Name: John" or "Age: 25". And each attribute must be separated by a new line. For example:
                Name: John Doe\\nAge: 25\\nProfession: Blacksmith\\nPersonality: Friendly\\nDescription: John Doe is a friendly blacksmith who is 25 years old. He is known for his skill in crafting swords and armor.
            '''

            if settings is not None:
                generation_prompt += f"\nAdditional Settings:\n {settings}"

            messages = [{
                "role": "system",
                "content": generation_prompt
            }]

            generated_npc = ai.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                max_tokens = 500
            )

            generated_npc = self.process_response(generated_npc.choices[0].message.content)

            return generated_npc
        except Exception as e:
            logging.error(e)
            logging.info(generated_npc)
            return None
    
    def process_response(self, response):
        try:
            processed_response = {}
            
            for attribute in response.split("\n"):
                if attribute:
                    attribute = attribute.split(":")
                    processed_response[attribute[0].strip()] = attribute[1].strip()

            return processed_response
        except Exception as e:
            logging.error(e)
            logging.info(response)
            return None

        
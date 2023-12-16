from openai import OpenAI
import logging
from quest import Quest

ai = OpenAI()

logging.basicConfig(level=logging.INFO)

class NPC():

    def __init__(self, name=None, age=None, profession=None, personality=None, description=None, image=None, settings=None):
        if name is None:
            information = self.generate_background(settings=settings)
            self.name = information['Name']
            self.age = information['Age']
            self.profession = information['Profession']
            self.personality = information['Personality']
            self.description = information['Description']
            self.image = self.generate_image()
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

            This is role playing and you are to act as your character. Therefore, you must respond in tone and style appropriate for your character. 
            You should also repond in conversational style and not speak in long paragraphs unless the topic requires it. The user you would be talking to would be a stranger to you so act accordingly.

            If you are unsure of what to say, you can ask the user about their name, age, profession, personality, and description. You can also ask the user about their preferred quest.

            If you have mentioned a mission or task and the user has agreed with or accepted your quest. Respond with only the words "CREATE QUEST" without punctuation or any other symbol or any other words.

            Respond in less than 100 words.
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
        generated_npc = None

        try:
            generation_prompt = '''
                You are an AI with the purpose of generating NPC backstories for a medieval fantasy game. You must create one NPC and provide the following:
                    - Name: The name of the NPC
                    - Age: The age of the NPC
                    - Profession: The profession of the NPC in the game world
                    - Personality: A brief description of the NPC's personality
                    - Description: A 2-sentence description of the NPC's appearance

                The profession of the NPC should be one of the following: Blacksmith, Farmer, Hunter, Noble, Priest, Scholar, Soldier, Thief, Wizard, Tavern Owner, Inn Keeper, Shop Keeper, Villager, or Village Chief.

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
        
    def generate_image(self):
        try:
            prompt = f'''
                You are an AI with the purpose of generating images of characters with medieval fantasy theme. You must create a 32-bit pixel art showing the character's face. The background should be the village where the character lives.

                Do not show character windows, dialog boxes, or any other UI elements. The image should be a portrait of the character.

                Please see character information below:
                Name: {self.name}
                Age: {self.age}
                Profession: {self.profession}
                Personality: {self.personality}
                Description: {self.description}
            '''

            image = ai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            return image.data[0].url
        except Exception as e:
            logging.error(e)
            logging.info("Prompt: {}", prompt)
            return None
        
    def generate_quest(self, messages):
        system_content = f'''
            As an AI dedicated to creating quests for a medieval fantasy game, your task is to generate a quest tailored to the user's level. The quest must be challenging yet achievable. Use the provided NPC information to create a contextually appropriate quest.

            NPC Information:
            - Name: {self.name}
            - Age: {self.age}
            - Profession: {self.profession}
            - Personality: {self.personality}
            - Description: {self.description}

            Generate a quest using the following format, ensuring each attribute is distinctly separated:

            Title: [Insert the title of the quest]
            Description: [Provide a detailed background and description of the quest]
            Difficulty: [Assign a difficulty level from F (easiest) to S (hardest)]
            Success Condition: [Define what constitutes successful completion of the quest]
            Failure Condition: [Specify conditions under which the quest is failed, e.g., time expiration, player's death, etc.]
            Reward: [List the reward(s) for completing the quest]

            Note: Only include the quest details in your response, formatted as above. Avoid adding any extraneous messages, as the response will be directly parsed for user display.

            Message History:
            ############################
        '''

        # Append the chat history to the prompt
        for message in messages:
            speaker = "User" if message['role'] == "user" else self.name
            system_content += f"\n{speaker}: {message['content']}"

        system_content += "\n############################"

        messages = [{
            "role": "system",
            "content": system_content
        }]

        response = ai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )

        processed_response = self.process_response(response.choices[0].message.content)

        logging.info(f"Processed Response: {processed_response}")

        quest = Quest(
            title=processed_response['Title'],
            description=processed_response['Description'],
            difficulty=processed_response['Difficulty'],
            success_condition=processed_response['Success Condition'],
            failure_condition=processed_response['Failure Condition'],
            reward=processed_response['Reward']
        )

        return quest
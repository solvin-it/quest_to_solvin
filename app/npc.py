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
            self.world_settings = settings
        else:
            self.name = name
            self.age = age
            self.profession = profession
            self.personality = personality
            self.description = description
            self.image = image

    def generate_response(self, messages):
        system_content = f'''
            You embody the character {self.name}, a {self.age}-year-old {self.profession} known for being {self.personality} and {self.description}. In this role-playing scenario, you are to interact in a manner befitting your character's traits and background. 

            Guidelines for Interaction:
            1. Adopt a conversational tone and style that reflects your character's persona.
            2. Keep responses concise, typically under 100 words, and avoid lengthy paragraphs unless necessary.
            3. Treat the user as a stranger, maintaining an appropriate demeanor based on your character's nature.

            Your Objective:
            - Engage the user in dialogue, guiding them towards a quest.
            - You may inquire about the user's name, age, profession, personality, and interests to tailor a suitable quest.
            - If asked about matters beyond your character's knowledge, respond with "I don't know" or "I'm not sure".
            - Once a mission or task is established and accepted by the user, simply respond with "CREATE QUEST" (no punctuation, symbols, or additional text).

            Remember, your interactions should be immersive, reflecting the settings. 
            
            Additional Settings: {self.world_settings}.
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
                As an AI tasked with creating medieval fantasy-themed character images, your objective is to generate a 32-bit pixel art portrait. The portrait should focus on the character's face, capturing their unique features and expressions in detail. Additionally, include a background that reflects the character's village environment or their profession, such as a smithy, tavern, inn, or a relevant setting.

                Key Instructions:
                - The image must be a close-up portrait showcasing only the character's face.
                - Background: Choose a setting that relates to either the character's village life or their profession, enhancing the character's story.
                - Avoid including character windows, dialog boxes, or any UI elements in the image. Focus on the character and the background.

                Character Information for Image Context:
                - Name: {self.name}
                - Age: {self.age}
                - Profession: {self.profession}
                - Personality: {self.personality}
                - Physical Description: {self.description}

                Please ensure that the image is a harmonious blend of the character's facial features and an appropriate background, adhering to the medieval fantasy theme.
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
            return None
        
    def generate_quest(self, messages):
        try:
            system_content = f'''
                As an AI dedicated to creating quests for a medieval fantasy game, your task is to generate a quest tailored to the user's level. The quest must be challenging yet achievable. Use the provided NPC information to create a contextually appropriate quest.

                NPC Information:
                - Name: {self.name}
                - Age: {self.age}
                - Profession: {self.profession}
                - Personality: {self.personality}
                - Description: {self.description}

                Generate a quest using the following format, ensuring each attribute is distinctly separated by a colon and each attribute is separated by a new line:

                Title: [Insert the title of the quest]\\n
                Description: [Provide a detailed background and description of the quest]\\n
                Difficulty: [Assign a difficulty level from F (easiest) to S (hardest), with possible values being F, E, D, C, B, A, and S]\\n
                Success Condition: [Define what constitutes successful completion of the quest]\\n
                Failure Condition: [Specify conditions under which the quest is failed, e.g., time expiration, player's death, etc.]\\n
                Reward: [List the reward(s) for completing the quest]

                As an example, a quest for a blacksmith NPC could be:
                Title: The Blacksmith's Apprentice\n
                Description: A blacksmith in the village is looking for an apprentice. He is willing to teach you the basics of blacksmithing if you help him with his work.\n
                Difficulty: F\n
                Success Condition: Complete the blacksmith's tasks.\n
                Failure Condition: The blacksmith dies.\n
                Reward: Learn the basics of blacksmithing.

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

            quest = Quest(
                title=processed_response['Title'],
                description=processed_response['Description'],
                difficulty=processed_response['Difficulty'],
                success_condition=processed_response['Success Condition'],
                failure_condition=processed_response['Failure Condition'],
                reward=processed_response['Reward']
            )

            return quest
        except Exception as e:
            logging.error(e)
            logging.info("Prompt: {}", system_content)
            logging.info(f"Response: {response.choices[0].message.content}")
            return None
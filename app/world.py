import dotenv
import os

dotenv.load_dotenv()

LORE_PATH = os.getenv("LORE_PATH")
BACKGROUND_PATH = os.getenv("BACKGROUND_PATH")

class World():

    def __init__(self):
        self.lore = self.load_lore()
        self.background = self.load_background()
        self.settings = '''
            The village, known as Eldertree, is a bastion of resilience, its thatched cottages and cobblestone pathways bearing the weight of countless stories.
        '''

    def load_lore(self):
        with open(LORE_PATH, "r") as f:
            lore = f.read()

        return lore
    
    def load_background(self):
        with open(BACKGROUND_PATH, "r") as f:
            background = f.read().split("\n")

        return background
    
    def get_location_image(self, location):
        return "app/static/img/{}.png".format(location)
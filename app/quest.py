class Quest():

    def __init__(self, title, description, difficulty, success_condition, failure_condition, reward):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.success_condition = success_condition
        self.failure_condition = failure_condition
        self.reward = reward

    
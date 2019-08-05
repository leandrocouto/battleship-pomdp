class Entry:
    def __init__(self, action_observation):
        #Tuple: (Action, Observation)
        self.entry = action_observation

class History:
    def __init__(self):
        self.history = []
    def add(self, action, observation):
        new_entry = Entry((action, observation))
        self.history.append(new_entry)
    def print_history(self):
        for entry in self.history:
            print('Action: ', entry[0], ' Observation: ', entry[1])
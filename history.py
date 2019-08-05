class Entry:
    def __init__(self, action, observation):
        self.action = action
        self.observation = observation

class History:
    def __init__(self):
        self.history_list = []
    def add(self, action, observation):
        new_entry = Entry(action, observation)
        self.history_list.append(new_entry)
    def print_history(self):
        for entry in self.history_list:
            print('Action: ', entry.action, ' Observation: ', entry.observation)
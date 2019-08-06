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
    def add_only_action(self, action):
        new_entry = Entry(action, -1)
        self.history_list.append(new_entry)
    def add_only_observation(self, observation):
        print('Tamanho: ', len(self.history_list))
        self.history_list[-1].observation = observation  
    def print_history(self):
        for entry in self.history_list:
            print('Action: ', entry.action, ' Observation: ', entry.observation)
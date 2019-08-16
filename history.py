class Entry:
    def __init__(self, action, observation):
        self.action = action
        self.observation = observation
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, other):
        return self.action == other.action and self.observation == other.observation

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
        self.history_list[-1].observation = observation  
    def print_history(self):
        if len(self.history_list) == 0:
            print('Empty history')
        for entry in self.history_list:
            print('**Action: ', entry.action, ' Observation: ', entry.observation)
    def __repr__(self):
        repr = ''
        for entry in self.history_list:
            repr += str(entry.action[0]) + str(entry.action[1]) + str(entry.observation)
        return repr
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, other):
        if other == -1:
            if len(self.history_list) == 0:
                 return True
            else:
                return False
        else:
            for i in range(len(self.history_list)):
                if self.history_list[i] != other.history_list[i]:
                    return False
            return True
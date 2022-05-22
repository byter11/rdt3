import threading

class StateMachine(threading.Thread):
    def __init__(self):
        self.handlers = {}
        self.startState = None

    def add(self, name, handler):
        self.startState = self.startState or name
        self.handlers[name.lower()] = handler

    def run(self, cargo):
        if not self.startState:
            return
            
        handler = self.handlers[self.startState]

        while True:
            newState, cargo = handler(cargo)
            print(newState, cargo)
            if newState.lower() == 'end':
                return
            handler = self.handlers[newState]

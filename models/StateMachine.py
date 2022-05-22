import threading


class StateMachine(threading.Thread):
    def __init__(self, exitState='end'):
        self.handlers = {'end': lambda: 0}
        self.startState = None
        self.exitState = exitState

    def add(self, name, handler):
        self.startState = self.startState or name
        self.handlers[name.lower()] = handler

    def run(self, cargo):
        if not self.startState:
            return

        handler = self.handlers[self.startState]

        while True:
            newState, cargo = handler(cargo)

            handler = self.handlers[newState]
            if newState.lower() == self.exitState:
                return

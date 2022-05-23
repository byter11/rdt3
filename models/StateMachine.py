import threading


class StateMachine(threading.Thread):
    def __init__(self, exitState):
        self.handlers = {}
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
            if cargo is not None:
                newState, cargo = handler(cargo)
            else:
                newState, cargo = handler()

            handler = self.handlers[newState]
            if newState == self.exitState:
                handler()
                break

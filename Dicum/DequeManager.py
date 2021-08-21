import logging
import os
import random
import yaml


class GreenCard():
    yaml_tag = "!GreenCard"
    def __init__(self):
        self.kind = "green"

    def __repr__(self):
        return f"{self.__class__.__name__}(kind={self.kind})"


class BlackCard():
    yaml_tag = "!BlackCard"
    def __init__(self, hours):
        self.kind = "black"
        self.hours = hours

    def __repr__(self):
        return f"{self.__class__.__name__}(kind={self.kind}, hours={self.hours})"


class YellowCard():
    yaml_tag = "!YellowCard"
    def __init__(self, number):
        self.kind = "Yellow"
        self.number = number
    
    def __repr__(self):
        return f"{self.__class__.__name__}(kind={self.kind}, number={self.number})"


class RedCard():
    yaml_tag = "!RedCard"
    def __init__(self, action, hours=12):
        self.kind = "red"
        self.action = action
        self.hours = hours

    def __repr__(self):
        return f"{self.__class__.__name__}(kind={self.kind}, action={self.action}, hours={self.hours})"


class DequeManager():
    def __init__(self, filename):
        self.filename = filename
        self.load_deque()
        if not self.deque:
            logging.warning("Loaded deque is empty.")
        random.shuffle(self.deque)

    def get_size(self):
        return len(self.deque)

    def get_card(self):
        return self.deque.pop()

    @staticmethod
    def save_specific_deque(filename, deque):
        with open(filename, "w") as file:
            file.write(yaml.dump(deque))

    def save_deque(self):
        save_specific_deque(self.filename, self.deque)

    def load_deque(self):
        with open(self.filename, "r") as file:
            text = file.read()
            logging.debug(text)
            self.deque = yaml.load(text, Loader=yaml.Loader)
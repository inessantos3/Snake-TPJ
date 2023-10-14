import pygame
from snake import Actor

class Command():
    def execute():
        raise NotImplemented

class Up(Command):
    def execute(self,actor:Actor):
        actor.up()

class Down(Command):
    def execute(self,actor:Actor):
        actor.down()

class Left(Command):
    def execute(self,actor:Actor):
        actor.left()

class Right(Command):
    def execute(self,actor:Actor):
        actor.right()

class NoCommand(Command):
    def execute(self,actor:Actor):
        pass

class InputHandler:

    def __init__(self,keymap):
        self.command = keymap

    def handleInput(self,event):
        key = event.key
        if key in self.command:
            return self.command[key]
        else:
            return NoCommand
    
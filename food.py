import random
import pygame
from constants import *

class foodClass:
    def __init__(self,sprite):
        self.position = (random.randrange(WIDTH), random.randrange(HEIGHT))
        self.food_sprite = pygame.image.load(sprite)

    def display_food(self,display):
        display.blit(self.food_sprite, (SCALE * self.position[0], SCALE * self.position[1], SCALE, SCALE))

    def move_food(self):
        self.position = (random.randrange(WIDTH), random.randrange(HEIGHT))

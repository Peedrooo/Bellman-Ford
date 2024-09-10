import pygame
from src.front.colors import *


class Node:
    def __init__(self, id, pos):
        self.color = BLUE
        self.id = id
        self.pos = pos

    def toggle_color(self, color):
        if self.color == color:
            self.color = BLUE
        else:
            self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.pos, 13)
        pygame.draw.circle(screen, self.color, self.pos, 11)

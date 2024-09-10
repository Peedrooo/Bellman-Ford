from typing import Any
from src.front.colors import WHITE
import pygame
import math

class Edge:
    def __init__(self, start_node, end_node, cost):
        self.start = start_node
        self.end = end_node
        self.cost = cost
        self.color = WHITE


    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start.pos, self.end.pos, 2)

        direction = (self.end.pos[0] - self.start.pos[0], self.end.pos[1] - self.start.pos[1])
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        direction = (direction[0] / length, direction[1] / length)

        size = 8

        point = (self.end.pos[0] - direction[0] * (size + 15 ), 
                 self.end.pos[1] - direction[1] * (size + 15 ))

        angle = math.pi / 4 
        left = (point[0] - math.cos(math.atan2(direction[1], direction[0]) + angle) * size,
                point[1] - math.sin(math.atan2(direction[1], direction[0]) + angle) * size)
        right = (point[0] - math.cos(math.atan2(direction[1], direction[0]) - angle) * size,
                 point[1] - math.sin(math.atan2(direction[1], direction[0]) - angle) * size)

        pygame.draw.polygon(screen, WHITE, [self.end.pos, left, right])

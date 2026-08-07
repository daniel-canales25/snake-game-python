import random
import pygame
from ..utils.constants import gridSize, cellSize, red, scoreAreaHeight

class Food:

    def __init__(self):
        self.position = None
        self.respawn()

    def respawn(self, snakeBody=None):
        if snakeBody is None:
            snakeBody = []
        while True:
            pos = (random.randint(0, gridSize - 1),
                random.randint(scoreAreaHeight, gridSize - 1))
            if pos not in snakeBody:
                self.position = pos
                break

    def draw(self, screen):
        if self.position:
            x = self.position[0] * cellSize
            y = self.position[1] * cellSize
            pygame.draw.circle(screen, red,
                            (x + cellSize//2, y + cellSize//2),
                              cellSize //2 - 2)

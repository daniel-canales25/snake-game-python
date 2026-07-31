import pygame
from ..utils.constants import cellSize, initialSnake, initialDirection, green, darkGreen

class Snake:

    def __init__(self):
        self.body = initialSnake.copy()
        self.direction = initialDirection
        self.nextDirection = initialDirection
        self.isGrowing = False

    def move(self):
        self.direction = self.nextDirection
        headX, headY = self.body[0]
        newHead = (headX + self.direction[0], headY + self.direction[1])
        self.body.insert(0, newHead)
        if not self.isGrowing:
            self.body.pop()
        else:
            self.isGrowing = False

    def grow(self):
        self.isGrowing = True

    def change_direction(self, newDirection):
        if (newDirection[0] * -1, newDirection[1] * -1) != self.direction:
            self.nextDirection = newDirection

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            x = segment[0] * cellSize
            y = segment[1] * cellSize
            color = darkGreen if i == 0 else green
            pygame.draw.rect(screen, color, (x, y, cellSize, cellSize))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, cellSize, cellSize), 1)

    @property
    def head(self):
        return self.body[0]

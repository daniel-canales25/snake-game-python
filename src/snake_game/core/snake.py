import pygame
from ..utils.constants import cellSize, initialSnake, initialDirection, green, darkGreen, scoreAreaHeight

class Snake:

    def __init__(self):
        self.body = initialSnake.copy()
        self.direction = initialDirection
        self.nextDirection = initialDirection
        self.isGrowing = False

    def move(self):
        self.direction = self.nextDirection
        #Desempaquetado de tuplas de body x , y
        headX, headY = self.body[0]
        #Al moverse 1 cuadro la cabeza ahora cambia de lugar
        newHead = (headX + self.direction[0], headY + self.direction[1])
        if newHead[1] < scoreAreaHeight:
            newHead = (newHead[0], scoreAreaHeight)
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
            
            
    #La funcion draw se encarga de convertir los valores de grid a pixeles 
    # (que es lo que necesita pygame)
    def draw(self, screen):
        #enumerate sirve para recorrer un elemento iterable como una lista 
        # y se puede obtiene el indice y su valor
        for i, segment in enumerate(self.body):
            #Coordenada x
            x = segment[0] * cellSize
            #Coordenada y
            y = segment[1] * cellSize
            color = darkGreen if i == 0 else green
            #funcion de pygame pygame.draw.rect(superficie, color, rect, ancho=0)
            pygame.draw.rect(screen, color, (x, y, cellSize, cellSize))
            #animacion de borde negro(0,0,0) y tamaño de 1 pixel para contorno de cada cuadro de la serpiente
            pygame.draw.rect(screen, (0, 0, 0), (x, y, cellSize, cellSize), 1)

    @property
    def head(self):
        return self.body[0]

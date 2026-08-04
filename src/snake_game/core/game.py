import pygame
from .snake import Snake
from .food import Food
from ..utils.constants import gridSize, black, white

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.isGameOver = False

    def update(self):
        if not self.isGameOver:
            self.snake.move()
            self.check_collisions()

    def draw(self):
        self.screen.fill(black)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.display_score()

    def display_score(self):
        #Funcion Font los parametros son Font(fuente, tamaño en pixeles)
        font = pygame.font.Font(None, 36)
        #Funcion render los parametros son render(texto, anti-aliasing, color del texto)
        scoreText = font.render(f"Puntuación: {self.score}", True, white)
        #Funcion blit dibuja el texto en pantalla y lo posiciona 
        # blit(texto en pantalla , posicion (x,y ) en pixeles)
        self.screen.blit(scoreText, (10, 10))

    def check_collisions(self):
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.respawn(self.snake.body)

        head = self.snake.head
        if (head[0] < 0 or head[0] >= gridSize or
            head[1] < 0 or head[1] >= gridSize or
            head in self.snake.body[1:]):
            self.game_over()

    def game_over(self):
        self.isGameOver = True
        print("Game Over! - Fin del juego")

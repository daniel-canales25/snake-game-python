import pygame
from .snake import Snake
from .food import Food
from ..utils.constants import gridSize, black, white, scoreAreaHeight, gridColor, cellSize, windowWidth, windowHeight, gameTitleText, titleFontSize, titleColor

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
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.display_score()
        self.display_title()

    def draw_grid(self):
        startY = scoreAreaHeight * cellSize
        for row in range(scoreAreaHeight, gridSize):
            y = row * cellSize
            pygame.draw.line(self.screen, gridColor, (0, y), (windowWidth, y), 1)
        for col in range(gridSize):
            x = col * cellSize
            pygame.draw.line(self.screen, gridColor, (x, startY), (x, windowHeight), 1)

    def display_score(self):
        font = pygame.font.Font(None, 36)
        scoreText = font.render(f"Puntuación: {self.score}", True, white)
        self.screen.blit(scoreText, (10, 10))

    def display_title(self):
        font = pygame.font.SysFont('courier', titleFontSize)
        textSurface = font.render(gameTitleText, True, titleColor)
        textRect = textSurface.get_rect(center=(windowWidth // 2, 50))
        self.screen.blit(textSurface, textRect)

    def check_collisions(self):
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.respawn(self.snake.body)

        head = self.snake.head
        if (head[0] < 0 or head[0] >= gridSize or
            head[1] < scoreAreaHeight or head[1] >= gridSize or
            head in self.snake.body[1:]):
            self.game_over()

    def game_over(self):
        self.isGameOver = True
        print("Game Over!")

    def restart(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.isGameOver = False

    def draw_game_over(self):
        self.screen.fill(black)
        font = pygame.font.SysFont('courier', 72)
        textSurface = font.render("GAME OVER", True, white)
        textRect = textSurface.get_rect(center=(windowWidth // 2, windowHeight // 2))
        self.screen.blit(textSurface, textRect)

        fontSmall = pygame.font.SysFont('courier', 24)
        restartText = fontSmall.render("ESPACIO - Reiniciar", True, white)
        exitText = fontSmall.render("ESC - Salir", True, white)
        restartRect = restartText.get_rect(center=(windowWidth // 2, windowHeight // 2 + 60))
        exitRect = exitText.get_rect(center=(windowWidth // 2, windowHeight // 2 + 90))
        self.screen.blit(restartText, restartRect)
        self.screen.blit(exitText, exitRect)

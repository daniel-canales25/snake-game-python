import pygame
import sys
from .core.game import Game
from .utils.constants import windowWidth, windowHeight, gameTitle, fps

def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(gameTitle)
    clock = pygame.time.Clock()
    game = Game(screen)
    running = True
    while running:
        game.update()
        game.draw()
        if game.isGameOver:
            game.draw_game_over()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.isGameOver:
                    if event.key == pygame.K_SPACE:
                        game.restart()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_RIGHT:
                        game.snake.change_direction((1, 0))
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_UP:
                        game.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction((0, 1))
        

if __name__ == "__main__":
    main()

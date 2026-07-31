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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()

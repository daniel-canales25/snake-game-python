import pygame
import sys
from .core.game import Game
from .core.start_screen import StartScreen
from .core.name_input import NameInput
from .utils.constants import windowWidth, windowHeight, gameTitle, fps, defaultName
from .utils.score_manager import save_score

def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(gameTitle)
    clock = pygame.time.Clock()

    current_state = "START_SCREEN"
    start_screen = StartScreen(screen)
    name_input = None
    game = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == "START_SCREEN":
                if start_screen.handle_event(event):
                    current_state = "PLAYING"
                    game = Game(screen)

            elif current_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if game.isGameOver:
                        if event.key == pygame.K_SPACE:
                            game = Game(screen)
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    else:
                        if event.key == pygame.K_RIGHT:
                            game.snake.change_direction((1, 0))
                        elif event.key == pygame.K_LEFT:
                            game.snake.change_direction((-1, 0))
                        elif event.key == pygame.K_UP:
                            game.snake.change_direction((0, -1))
                        elif event.key == pygame.K_DOWN:
                            game.snake.change_direction((0, 1))

            elif current_state == "NAME_INPUT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game = Game(screen)
                        current_state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        name = name_input.name if name_input.name.strip() else defaultName
                        save_score(name, game.score)
                        start_screen.refresh()
                        current_state = "START_SCREEN"
                    else:
                        name_input.handle_event(event)

        if current_state == "START_SCREEN":
            start_screen.draw()
        elif current_state == "PLAYING":
            game.update()
            game.draw()
            if game.isGameOver:
                current_state = "NAME_INPUT"
                name_input = NameInput(screen, game.score)
        elif current_state == "NAME_INPUT":
            name_input.update_cursor()
            name_input.draw()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

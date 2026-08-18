import pygame
from ..utils.constants import (
    windowWidth, windowHeight, black, white, green, red,
    gridColor, maxNameLength, defaultName
)


class NameInput:

    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.name = ""
        self.inputBox = pygame.Rect(
            windowWidth // 2 - 120, windowHeight // 2 + 20, 240, 50
        )
        self.active = True
        self.cursorTimer = 0
        self.showCursor = True

    def draw(self):
        self.screen.fill(black)

        fontGameOver = pygame.font.SysFont("courier", 72)
        goSurface = fontGameOver.render("FIN DEL JUEGO", True, red)
        goRect = goSurface.get_rect(center=(windowWidth // 2, windowHeight // 2 - 120))
        self.screen.blit(goSurface, goRect)

        fontScore = pygame.font.SysFont("courier", 36)
        scoreText = fontScore.render(f"Tu puntaje: {self.score}", True, white)
        scoreRect = scoreText.get_rect(center=(windowWidth // 2, windowHeight // 2 - 50))
        self.screen.blit(scoreText, scoreRect)

        fontLabel = pygame.font.SysFont("courier", 22)
        labelSurface = fontLabel.render("Ingresa tu nombre (max 5 caracteres):", True, gridColor)
        labelRect = labelSurface.get_rect(center=(windowWidth // 2, windowHeight // 2 - 10))
        self.screen.blit(labelSurface, labelRect)

        boxColor = green if self.active else gridColor
        pygame.draw.rect(self.screen, boxColor, self.inputBox, 2, border_radius=5)

        fontInput = pygame.font.SysFont("courier", 32)
        displayText = self.name
        if self.active and self.showCursor:
            displayText += "_"
        inputSurface = fontInput.render(displayText, True, white)
        inputRect = inputSurface.get_rect(center=self.inputBox.center)
        self.screen.blit(inputSurface, inputRect)

        charCount = fontLabel.render(f"{len(self.name)}/{maxNameLength}", True, gridColor)
        countRect = charCount.get_rect(midleft=(self.inputBox.right + 10, self.inputBox.centery))
        self.screen.blit(charCount, countRect)

        fontHint = pygame.font.SysFont("courier", 20)
        enterHint = fontHint.render("ENTER - Guardar", True, green)
        spaceHint = fontHint.render("ESPACIO - Reiniciar", True, white)
        escHint = fontHint.render("ESC - Salir", True, red)

        enterRect = enterHint.get_rect(center=(windowWidth // 2, windowHeight // 2 + 110))
        spaceRect = spaceHint.get_rect(center=(windowWidth // 2, windowHeight // 2 + 140))
        escRect = escHint.get_rect(center=(windowWidth // 2, windowHeight // 2 + 170))

        self.screen.blit(enterHint, enterRect)
        self.screen.blit(spaceHint, spaceRect)
        self.screen.blit(escHint, escRect)

        if len(self.name) == 0:
            defaultHint = fontHint.render(f'(Si no escribes nada se guardara como "{defaultName}")', True, gridColor)
            defaultRect = defaultHint.get_rect(center=(windowWidth // 2, windowHeight // 2 + 210))
            self.screen.blit(defaultHint, defaultRect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                name = self.name if self.name.strip() else defaultName
                return ("confirm", name)
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.unicode.isalnum() and len(self.name) < maxNameLength:
                self.name += event.unicode.upper()
        return None

    def update_cursor(self):
        self.cursorTimer += 1
        if self.cursorTimer >= 30:
            self.cursorTimer = 0
            self.showCursor = not self.showCursor

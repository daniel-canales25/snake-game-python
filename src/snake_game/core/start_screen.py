import pygame
from ..utils.constants import (
    windowWidth, windowHeight, black, white, green,
    gameTitleText, titleFontSize, titleColor, gridColor
)
from ..utils.score_manager import get_top_scores, get_total_scores


class StartScreen:

    def __init__(self, screen):
        self.screen = screen
        self.scores = get_top_scores()
        self.totalScores = get_total_scores()
        self.playButton = pygame.Rect(
            windowWidth // 2 - 100, windowHeight - 150, 200, 60
        )
        self.hoverPlay = False

    def refresh(self):
        self.scores = get_top_scores()
        self.totalScores = get_total_scores()

    def draw(self):
        self.screen.fill(black)

        fontTitle = pygame.font.SysFont("courier", titleFontSize)
        titleSurface = fontTitle.render(gameTitleText, True, titleColor)
        titleRect = titleSurface.get_rect(center=(windowWidth // 2, 80))
        self.screen.blit(titleSurface, titleRect)

        fontHeader = pygame.font.SysFont("courier", 28)
        headerSurface = fontHeader.render("MEJORES PUNTUACIONES", True, white)
        headerRect = headerSurface.get_rect(center=(windowWidth // 2, 160))
        self.screen.blit(headerSurface, headerRect)

        tableX = windowWidth // 2 - 200
        tableY = 210
        rowHeight = 45
        colWidths = [50, 150, 150]

        fontRow = pygame.font.SysFont("courier", 24)

        headers = ["#", "NOMBRE", "PUNTAJE"]
        for i, header in enumerate(headers):
            x = tableX + sum(colWidths[:i])
            surface = fontRow.render(header, True, green)
            self.screen.blit(surface, (x, tableY))

        pygame.draw.line(
            self.screen, gridColor,
            (tableX, tableY + 35),
            (tableX + sum(colWidths), tableY + 35), 2
        )

        if not self.scores:
            fontEmpty = pygame.font.SysFont("courier", 22)
            emptySurface = fontEmpty.render("No hay partidas registradas", True, gridColor)
            emptyRect = emptySurface.get_rect(center=(windowWidth // 2, tableY + 80))
            self.screen.blit(emptySurface, emptyRect)
        else:
            for idx, entry in enumerate(self.scores):
                y = tableY + 50 + idx * rowHeight
                rank = str(idx + 1)
                name = entry["name"][:5]
                score = str(entry["score"])

                rankSurface = fontRow.render(rank, True, white)
                nameSurface = fontRow.render(name, True, white)
                scoreSurface = fontRow.render(score, True, white)

                self.screen.blit(rankSurface, (tableX, y))
                self.screen.blit(nameSurface, (tableX + colWidths[0], y))
                self.screen.blit(scoreSurface, (tableX + colWidths[0] + colWidths[1], y))

        if self.totalScores > 10:
            fontMsg = pygame.font.SysFont("courier", 18)
            msgSurface = fontMsg.render("No has alcanzado a los mejores 10 puntajes", True, (255, 200, 0))
            msgRect = msgSurface.get_rect(center=(windowWidth // 2, tableY + 50 + 10 * rowHeight + 20))
            self.screen.blit(msgSurface, msgRect)

        mousePos = pygame.mouse.get_pos()
        self.hoverPlay = self.playButton.collidepoint(mousePos)

        buttonColor = green if self.hoverPlay else (0, 180, 0)
        pygame.draw.rect(self.screen, buttonColor, self.playButton, border_radius=10)
        pygame.draw.rect(self.screen, white, self.playButton, 2, border_radius=10)

        fontButton = pygame.font.SysFont("courier", 32)
        buttonText = fontButton.render("JUGAR", True, black)
        buttonRect = buttonText.get_rect(center=self.playButton.center)
        self.screen.blit(buttonText, buttonRect)

        fontHint = pygame.font.SysFont("courier", 18)
        hintSurface = fontHint.render("Click en JUGAR o presiona ESPACIO para iniciar", True, gridColor)
        hintRect = hintSurface.get_rect(center=(windowWidth // 2, windowHeight - 70))
        self.screen.blit(hintSurface, hintRect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.playButton.collidepoint(event.pos):
                return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False

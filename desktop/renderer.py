import math
import random

import pygame

from config import SETTINGS


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.board = screen.subsurface(
            (0, SETTINGS.HUD_HEIGHT, SETTINGS.WIDTH, SETTINGS.HEIGHT)
        )
        self.font = pygame.font.SysFont("dejavusans", 22, bold=True)
        self.large_font = pygame.font.SysFont("dejavusans", 42, bold=True)
        self.small_font = pygame.font.SysFont("dejavusansmono", 13)
        self.background = self._make_background()
        self.glows = {
            color: self._make_glow(color)
            for color in (SETTINGS.SNAKE_HEAD, SETTINGS.FOOD, SETTINGS.METEOR)
        }

    def _make_background(self) -> pygame.Surface:
        background = pygame.Surface(self.board.get_size())
        for y in range(SETTINGS.HEIGHT):
            shade = int(8 * y / SETTINGS.HEIGHT)
            color = tuple(channel + shade for channel in SETTINGS.BACKGROUND)
            pygame.draw.line(background, color, (0, y), (SETTINGS.WIDTH, y))
        for x in range(0, SETTINGS.WIDTH, SETTINGS.CELL_SIZE):
            pygame.draw.line(background, SETTINGS.GRID, (x, 0), (x, SETTINGS.HEIGHT))
        for y in range(0, SETTINGS.HEIGHT, SETTINGS.CELL_SIZE):
            pygame.draw.line(background, SETTINGS.GRID, (0, y), (SETTINGS.WIDTH, y))
        rng = random.Random(7)
        for _ in range(95):
            center = (rng.randrange(SETTINGS.WIDTH), rng.randrange(SETTINGS.HEIGHT))
            shade = rng.randrange(60, 135)
            pygame.draw.circle(background, (shade, shade, shade + 35), center, 1)
        return background

    def _make_glow(self, color) -> pygame.Surface:
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)
        for radius in range(39, 0, -1):
            pygame.draw.circle(glow, (*color, int(55 * (1 - radius / 40) ** 2)),
                               (40, 40), radius)
        return glow

    def _glow(self, center, color) -> None:
        self.board.blit(self.glows[color], (center[0] - 40, center[1] - 40))

    def _cell_center(self, position):
        cell = SETTINGS.CELL_SIZE
        return (position[0] * cell + cell // 2, position[1] * cell + cell // 2)

    def draw(self, game) -> None:
        self.board.blit(self.background, (0, 0))
        self._draw_food(game)
        self._draw_snake(game)
        self._draw_meteors(game)
        pygame.draw.rect(self.board, (54, 76, 100), self.board.get_rect(), 1)
        self._draw_score(game)
        if game.game_over:
            self._draw_game_over(game)

    def _draw_snake(self, game) -> None:
        cell = SETTINGS.CELL_SIZE
        self._glow(self._cell_center(game.snake.head), SETTINGS.SNAKE_HEAD)
        for index, (x, y) in enumerate(reversed(game.snake.body)):
            is_head = index == len(game.snake.body) - 1
            color = SETTINGS.SNAKE_HEAD if is_head else SETTINGS.SNAKE
            rect = pygame.Rect(x * cell + 2, y * cell + 2, cell - 4, cell - 4)
            pygame.draw.rect(self.board, (8, 37, 48), rect.move(0, 3), border_radius=7)
            pygame.draw.rect(self.board, color, rect, border_radius=7)
            pygame.draw.line(self.board, SETTINGS.SNAKE_HEAD,
                             (rect.left + 5, rect.top + 3),
                             (rect.right - 6, rect.top + 3), 2)
        cx, cy = self._cell_center(game.snake.head)
        dx, dy = game.snake.direction
        for side in (-1, 1):
            eye = (cx + dx * 5 - dy * side * 5, cy + dy * 5 + dx * side * 5)
            pygame.draw.circle(self.board, SETTINGS.BACKGROUND, eye, 3)

    def _draw_food(self, game) -> None:
        cx, cy = self._cell_center(game.food.position)
        self._glow((cx, cy), SETTINGS.FOOD)
        radius = 11 + int(2 * math.sin(game.elapsed * 4))
        pygame.draw.circle(self.board, (97, 86, 147), (cx, cy), radius, 1)
        points = [(cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)]
        pygame.draw.polygon(self.board, SETTINGS.FOOD, points)
        pygame.draw.line(self.board, SETTINGS.TEXT, (cx - 3, cy), (cx, cy - 3), 2)

    def _draw_meteors(self, game) -> None:
        cell = SETTINGS.CELL_SIZE
        radius = round(SETTINGS.METEOR_RADIUS * cell)
        for meteor in game.meteors:
            cx, cy = round(meteor.x * cell), round(meteor.y * cell)
            self._glow((cx, cy), SETTINGS.METEOR)
            sway = int(3 * math.sin(game.elapsed * 15 + meteor.x))
            pygame.draw.polygon(self.board, (116, 53, 48), [
                (cx - radius, cy), (cx + sway, cy - 65), (cx + radius, cy),
            ])
            pygame.draw.polygon(self.board, SETTINGS.METEOR, [
                (cx - radius + 3, cy), (cx - sway, cy - 38), (cx + radius - 3, cy),
            ])
            pygame.draw.circle(self.board, (255, 208, 120), (cx, cy), radius + 1)
            pygame.draw.polygon(self.board, (110, 69, 63), [
                (cx - radius, cy - 2), (cx - 4, cy - radius),
                (cx + 5, cy - radius + 2), (cx + radius, cy + 3),
                (cx + 3, cy + radius), (cx - 6, cy + radius - 2),
            ])
            pygame.draw.circle(self.board, (64, 44, 48), (cx - 3, cy - 2), 3)
            pygame.draw.circle(self.board, (170, 104, 72), (cx + 4, cy + 3), 2)

    def _draw_score(self, game) -> None:
        pygame.draw.rect(self.screen, SETTINGS.BACKGROUND,
                         (0, 0, SETTINGS.WIDTH, SETTINGS.HUD_HEIGHT))
        title = self.font.render("SNAKE / ÓRBITA", True, SETTINGS.SNAKE_HEAD)
        controls = self.small_font.render("WASD / FLECHAS · ESQUIVA LOS METEORITOS",
                                          True, SETTINGS.MUTED_TEXT)
        self.screen.blit(title, (20, 10))
        self.screen.blit(controls, (20, 44))
        score = self.font.render(f"{game.score:02d}", True, SETTINGS.TEXT)
        label = self.small_font.render("ENERGÍA", True, SETTINGS.FOOD)
        self.screen.blit(score, score.get_rect(topright=(SETTINGS.WIDTH - 22, 8)))
        self.screen.blit(label, label.get_rect(topright=(SETTINGS.WIDTH - 22, 43)))

    def _draw_game_over(self, game) -> None:
        overlay = pygame.Surface(self.board.get_size(), pygame.SRCALPHA)
        overlay.fill(SETTINGS.GAME_OVER_OVERLAY)
        self.board.blit(overlay, (0, 0))
        card = pygame.Rect(0, 0, 490, 250)
        card.center = self.board.get_rect().center
        pygame.draw.rect(self.board, SETTINGS.BACKGROUND, card, border_radius=18)
        pygame.draw.rect(self.board, SETTINGS.METEOR, card, 1, border_radius=18)
        self._center_text(self.small_font.render("MISIÓN TERMINADA", True, SETTINGS.METEOR),
                          card.top + 35)
        self._center_text(self.large_font.render("FIN DEL JUEGO", True, SETTINGS.TEXT),
                          card.top + 83)
        self._center_text(self.small_font.render(game.over_reason, True, SETTINGS.MUTED_TEXT),
                          card.top + 124)
        self._center_text(self.font.render(f"Energía recogida: {game.score}", True, SETTINGS.FOOD),
                          card.top + 164)
        self._center_text(self.small_font.render("R · REINTENTAR     ESC · SALIR", True, SETTINGS.TEXT),
                          card.top + 215)

    def _center_text(self, surface: pygame.Surface, y: int) -> None:
        self.board.blit(surface, surface.get_rect(center=(SETTINGS.WIDTH // 2, y)))

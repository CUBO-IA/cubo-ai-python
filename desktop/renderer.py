import pygame

from config import SETTINGS


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font = pygame.font.Font(None, 30)
        self.large_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 24)

    def draw(self, game) -> None:
        self.screen.fill(SETTINGS.BACKGROUND)

        self._draw_grid()
        self._draw_food(game)
        self._draw_snake(game)
        self._draw_score(game)

        if game.game_over:
            self._draw_game_over(game)

    def _draw_grid(self) -> None:
        cell = SETTINGS.CELL_SIZE

        for x in range(0, SETTINGS.WIDTH, cell):
            pygame.draw.line(
                self.screen,
                SETTINGS.GRID,
                (x, 0),
                (x, SETTINGS.HEIGHT),
            )

        for y in range(0, SETTINGS.HEIGHT, cell):
            pygame.draw.line(
                self.screen,
                SETTINGS.GRID,
                (0, y),
                (SETTINGS.WIDTH, y),
            )

    def _draw_snake(self, game) -> None:
        cell = SETTINGS.CELL_SIZE

        for index, (x, y) in enumerate(game.snake.body):
            color = SETTINGS.SNAKE_HEAD if index == 0 else SETTINGS.SNAKE

            rect = pygame.Rect(
                x * cell + 2,
                y * cell + 2,
                cell - 4,
                cell - 4,
            )

            pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def _draw_food(self, game) -> None:
        cell = SETTINGS.CELL_SIZE
        x, y = game.food.position

        center = (
            x * cell + cell // 2,
            y * cell + cell // 2,
        )

        pygame.draw.circle(self.screen, SETTINGS.FOOD, center, cell // 3)

    def _draw_score(self, game) -> None:
        text = self.font.render(
            f"SCORE  {game.score}",
            True,
            SETTINGS.TEXT,
        )

        self.screen.blit(text, (20, 18))

    def _draw_game_over(self, game) -> None:
        overlay = pygame.Surface(
            (SETTINGS.WIDTH, SETTINGS.HEIGHT),
            pygame.SRCALPHA,
        )

        overlay.fill(SETTINGS.GAME_OVER_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        title = self.large_font.render("GAME OVER", True, SETTINGS.TEXT)
        score = self.font.render(
            f"Score: {game.score}",
            True,
            SETTINGS.MUTED_TEXT,
        )
        restart = self.small_font.render(
            "Presiona R para reiniciar",
            True,
            SETTINGS.TEXT,
        )

        self._center_text(title, SETTINGS.HEIGHT // 2 - 55)
        self._center_text(score, SETTINGS.HEIGHT // 2 + 5)
        self._center_text(restart, SETTINGS.HEIGHT // 2 + 45)

    def _center_text(self, surface: pygame.Surface, y: int) -> None:
        rect = surface.get_rect(center=(SETTINGS.WIDTH // 2, y))
        self.screen.blit(surface, rect)

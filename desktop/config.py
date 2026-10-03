from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Ventana
    WIDTH: int = 800
    HEIGHT: int = 600
    TITLE: str = "Snake"

    # Tablero
    CELL_SIZE: int = 25

    # Juego
    FPS: int = 60
    INITIAL_SPEED: float = 0.12
    SPEED_INCREMENT: float = 0.002

    # Colores
    BACKGROUND: tuple = (18, 18, 20)
    GRID: tuple = (30, 30, 33)
    SNAKE: tuple = (110, 231, 183)
    SNAKE_HEAD: tuple = (167, 243, 208)
    FOOD: tuple = (248, 113, 113)
    TEXT: tuple = (245, 245, 245)
    MUTED_TEXT: tuple = (150, 150, 155)
    GAME_OVER_OVERLAY: tuple = (0, 0, 0, 150)


SETTINGS = Settings()

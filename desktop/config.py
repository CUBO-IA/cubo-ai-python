from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Ventana
    WIDTH: int = 800
    HEIGHT: int = 600
    TITLE: str = "Snake · Órbita"
    HUD_HEIGHT: int = 76

    # Tablero
    CELL_SIZE: int = 25

    # Juego
    FPS: int = 60
    INITIAL_SPEED: float = 0.12
    SPEED_INCREMENT: float = 0.002
    METEOR_INTERVAL: float = 1.4
    METEOR_SPEED: tuple = (4.5, 7.0)  # Celdas por segundo.
    METEOR_RADIUS: float = 0.36

    # Colores
    BACKGROUND: tuple = (12, 19, 39)
    GRID: tuple = (23, 35, 57)
    SNAKE: tuple = (69, 203, 194)
    SNAKE_HEAD: tuple = (169, 255, 224)
    FOOD: tuple = (189, 164, 255)
    METEOR: tuple = (255, 139, 67)
    TEXT: tuple = (242, 242, 230)
    MUTED_TEXT: tuple = (139, 160, 185)
    GAME_OVER_OVERLAY: tuple = (5, 10, 24, 190)


SETTINGS = Settings()

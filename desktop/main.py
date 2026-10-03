import pygame

from config import SETTINGS
from game import Game
from input_handler import InputHandler
from renderer import Renderer


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SETTINGS.WIDTH, SETTINGS.HEIGHT))
    pygame.display.set_caption(SETTINGS.TITLE)

    clock = pygame.time.Clock()

    game = Game()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True

    while running:
        delta_time = clock.tick(SETTINGS.FPS) / 1000.0

        running = input_handler.process(game)
        game.update(delta_time)

        renderer.draw(game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

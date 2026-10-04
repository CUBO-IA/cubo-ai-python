import os

from config import SETTINGS
from game import Game, Meteor


def test_meteors():
    game = Game()
    game.move_interval = 100
    game.update(SETTINGS.METEOR_INTERVAL - 0.01)
    assert not game.meteors
    game.update(0.02)
    assert len(game.meteors) == 1
    meteor = game.meteors[0]
    assert 0.5 <= meteor.x <= game.columns - 0.5
    assert SETTINGS.METEOR_SPEED[0] <= meteor.speed <= SETTINGS.METEOR_SPEED[1]
    old_y = meteor.y
    game.update(0.01)
    assert meteor.y > old_y

    assert Meteor(5.5, 5.5, 0).hits([(5, 5)])
    assert not Meteor(7, 5.5, 0).hits([(5, 5)])
    assert not Meteor(4.8, 6.3, 0).hits([(5, 5)])
    assert Meteor(5.5, 8, 10).hits([(5, 5)], previous_y=2)

    game.restart()
    tail_x, tail_y = game.snake.body[-1]
    game.meteors = [Meteor(tail_x + 0.5, tail_y - 2, 20)]
    game.update(0.3)  # Cruza el cuerpo entero entre dos fotogramas.
    assert game.game_over and game.over_reason == "Te alcanzó un meteorito"
    elapsed = game.elapsed
    game.update(1)
    assert game.elapsed == elapsed
    game.restart()
    assert not game.meteors and not game.game_over
    assert game.elapsed == game.meteor_timer == game.score == 0
    assert game.over_reason == ""

    x, y = game.snake.head
    game.meteors = [Meteor(x + 1.5, y + 0.5, 0)]
    game.update(game.move_interval)  # La cabeza entra en un meteorito.
    assert game.game_over

    game.restart()
    game.meteors = [Meteor(0.5, game.rows + 1, 5)]
    game.update(0.01)
    assert not game.meteors
    x, y = game.snake.head
    game.food.position = (x + 1, y)
    game.update(game.move_interval)
    assert game.score == 1 and len(game.snake.body) == 4


def test_renderer():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    import pygame
    from renderer import Renderer

    pygame.display.init()
    pygame.font.init()
    try:
        screen = pygame.display.set_mode(
            (SETTINGS.WIDTH, SETTINGS.HEIGHT + SETTINGS.HUD_HEIGHT)
        )
        renderer = Renderer(screen)
        game = Game()
        game.meteors = [Meteor(5.5, 8, 5), Meteor(0.5, -0.36, 5)]
        renderer.draw(game)
        game.game_over = True
        game.over_reason = "Te alcanzó un meteorito"
        renderer.draw(game)
        game.restart()
        renderer.draw(game)
    finally:
        pygame.quit()


if __name__ == "__main__":
    test_meteors()
    test_renderer()
    print("OK: caída, colisiones, reinicio y renderizado")

import pygame


class InputHandler:
    DIRECTIONS = {
        pygame.K_UP: (0, -1),
        pygame.K_w: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_s: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_a: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_d: (1, 0),
    }

    def process(self, game) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_r and game.game_over:
                    game.restart()
                    continue

                direction = self.DIRECTIONS.get(event.key)

                if direction and not game.game_over:
                    game.snake.change_direction(direction)

        return True

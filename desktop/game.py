from config import SETTINGS
from food import Food
from snake import Snake


class Game:
    def __init__(self):
        self.columns = SETTINGS.WIDTH // SETTINGS.CELL_SIZE
        self.rows = SETTINGS.HEIGHT // SETTINGS.CELL_SIZE

        self.game_over = False
        self.score = 0
        self.move_timer = 0.0
        self.move_interval = SETTINGS.INITIAL_SPEED

        self.snake = None
        self.food = None

        self.restart()

    def restart(self) -> None:
        center_x = self.columns // 2
        center_y = self.rows // 2

        self.snake = Snake(
            body=[
                (center_x, center_y),
                (center_x - 1, center_y),
                (center_x - 2, center_y),
            ]
        )

        self.food = Food(self.columns, self.rows)
        self.food.spawn(self.snake.body)

        self.game_over = False
        self.score = 0
        self.move_timer = 0.0
        self.move_interval = SETTINGS.INITIAL_SPEED

    def update(self, delta_time: float) -> None:
        if self.game_over:
            return

        self.move_timer += delta_time

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0.0

        next_head = (
            self.snake.head[0] + self.snake.next_direction[0],
            self.snake.head[1] + self.snake.next_direction[1],
        )

        # Colisión con las paredes
        if (
            next_head[0] < 0
            or next_head[0] >= self.columns
            or next_head[1] < 0
            or next_head[1] >= self.rows
        ):
            self.game_over = True
            return

        # Colisión consigo misma
        if next_head in self.snake.body[:-1]:
            self.game_over = True
            return

        ate_food = next_head == self.food.position

        self.snake.move(grow=ate_food)

        if ate_food:
            self.score += 1
            self.food.spawn(self.snake.body)

            # La serpiente aumenta ligeramente su velocidad.
            self.move_interval = max(
                0.045,
                self.move_interval - SETTINGS.SPEED_INCREMENT,
            )

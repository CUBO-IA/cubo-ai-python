import random
from dataclasses import dataclass

from config import SETTINGS
from food import Food
from snake import Snake


@dataclass
class Meteor:
    x: float
    y: float
    speed: float

    def hits(self, body, previous_y=None) -> bool:
        # Barre toda la caída para no atravesar la serpiente entre fotogramas.
        top = self.y if previous_y is None else previous_y
        for x, y in body:
            dx = max(x - self.x, 0, self.x - (x + 1))
            dy = max(y - self.y, 0, top - (y + 1))
            if dx * dx + dy * dy < SETTINGS.METEOR_RADIUS ** 2:
                return True
        return False


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
        self.meteors = []
        self.meteor_timer = 0.0
        self.elapsed = 0.0
        self.over_reason = ""

    def update(self, delta_time: float) -> None:
        if self.game_over:
            return

        self.elapsed += delta_time
        for meteor in self.meteors:
            previous_y = meteor.y
            meteor.y += meteor.speed * delta_time
            if meteor.hits(self.snake.body, previous_y):
                self.game_over = True
                self.over_reason = "Te alcanzó un meteorito"
                return

        self.meteors = [
            meteor for meteor in self.meteors
            if meteor.y - SETTINGS.METEOR_RADIUS < self.rows
        ]
        self.meteor_timer += delta_time
        if self.meteor_timer >= SETTINGS.METEOR_INTERVAL:
            self.meteor_timer %= SETTINGS.METEOR_INTERVAL
            self.meteors.append(Meteor(
                x=random.uniform(0.5, self.columns - 0.5),
                y=-SETTINGS.METEOR_RADIUS,
                speed=random.uniform(*SETTINGS.METEOR_SPEED),
            ))

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
            self.over_reason = "Saliste de la órbita"
            return

        # Colisión consigo misma
        if next_head in self.snake.body[:-1]:
            self.game_over = True
            self.over_reason = "Chocaste con tu serpiente"
            return

        ate_food = next_head == self.food.position

        self.snake.move(grow=ate_food)

        if any(meteor.hits(self.snake.body) for meteor in self.meteors):
            self.game_over = True
            self.over_reason = "Te alcanzó un meteorito"
            return

        if ate_food:
            self.score += 1
            self.food.spawn(self.snake.body)

            # La serpiente aumenta ligeramente su velocidad.
            self.move_interval = max(
                0.045,
                self.move_interval - SETTINGS.SPEED_INCREMENT,
            )

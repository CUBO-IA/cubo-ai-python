from dataclasses import dataclass
from typing import List, Tuple

Position = Tuple[int, int]


@dataclass
class Snake:
    body: List[Position]
    direction: Position = (1, 0)
    next_direction: Position = (1, 0)

    @property
    def head(self) -> Position:
        return self.body[0]

    def change_direction(self, direction: Position) -> None:
        # Evita que la serpiente pueda girar directamente en dirección opuesta.
        if (
            direction[0] + self.direction[0] == 0
            and direction[1] + self.direction[1] == 0
        ):
            return

        self.next_direction = direction

    def move(self, grow: bool = False) -> None:
        self.direction = self.next_direction

        new_head = (
            self.head[0] + self.direction[0],
            self.head[1] + self.direction[1],
        )

        self.body.insert(0, new_head)

        if not grow:
            self.body.pop()

    def contains(self, position: Position) -> bool:
        return position in self.body

    def collides_with_self(self) -> bool:
        return self.head in self.body[1:]

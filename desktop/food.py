import random
from typing import List, Tuple

Position = Tuple[int, int]


class Food:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
        self.position = (0, 0)

    def spawn(self, occupied: List[Position]) -> None:
        available = [
            (x, y)
            for x in range(self.columns)
            for y in range(self.rows)
            if (x, y) not in occupied
        ]

        if available:
            self.position = random.choice(available)

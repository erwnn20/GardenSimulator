from dataclasses import dataclass
from enum import Enum

from utils.prompt import Prompt


@dataclass
class Fertilizer:
    turn: int
    efficiency: float

    def __str__(self):
        return f'{self.efficiency:.2f} for {self.turn} turn(s)'


class FertilizerType(Enum):
    COMPOST = Fertilizer(turn=3, efficiency=0.15)
    MANURE = Fertilizer(turn=5, efficiency=0.2)
    CHEMICAL = Fertilizer(turn=7, efficiency=0.5)
    SLOW_RELEASE = Fertilizer(turn=10, efficiency=0.1)
    ORGANIC = Fertilizer(turn=4, efficiency=0.2)
    POTASSIUM = Fertilizer(turn=6, efficiency=0.3)
    LIQUID = Fertilizer(turn=2, efficiency=0.25)
    ASH = Fertilizer(turn=3, efficiency=0.1)

    def __str__(self):
        return f'{self.name.capitalize()}: {self.value}'

    @staticmethod
    def select() -> 'FertilizerType':
        return Prompt.select(
            'Choose a fertilizer:',
            [f for f in FertilizerType],
            lambda f: str(f)).element

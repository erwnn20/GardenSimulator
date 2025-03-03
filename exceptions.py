from abc import ABC

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plants.plant import Plant


class PlantException(ABC):
    class Growth(Exception):
        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)

    class Dead(Exception):
        def __init__(self, plant: 'Plant'):
            self.message = f'This {type(plant).__name__} is dead'
            super().__init__(self.message)


class PlantationException(ABC):
    class Seed(Exception):
        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)

    class Soil(Exception):
        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)

    class Water(Exception):
        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)


class UserException(ABC):
    class Money(Exception):
        def __init__(self, message: str):
            self.message = message
            super().__init__(self.message)

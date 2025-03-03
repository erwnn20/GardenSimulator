from abc import ABC


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
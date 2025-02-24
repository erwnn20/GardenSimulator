from abc import ABC


class PlantationException(ABC):
    class Seed(Exception): pass

    class Soil(Exception): pass

    class Water(Exception): pass

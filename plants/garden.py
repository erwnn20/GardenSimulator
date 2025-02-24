from plants.plantation import Plantation


class Garden:
    def __init__(self, name: str):
        self.name = name
        self.plants = []

    def __add__(self, new_plant: Plantation | list[Plantation]):
        self.plants += new_plant if isinstance(new_plant, list) else [new_plant]
        return self

import os
import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plants.garden import Garden
    from user.user import User


@dataclass
class Save:
    name: str
    user: 'User'
    garden: 'Garden'

    def __str__(self) -> str:
        return (f'{self.name}'
                '\n' + '\n'.join(
            [f'  {key.capitalize()}: {value.to_str()}' for key, value in vars(self).items()
             if isinstance(value, Data)]))


class Data(ABC):
    _dir: str = './data/saves/'

    @abstractmethod
    def to_str(self) -> str:
        pass

    @staticmethod
    def save(filename: str, data: dict[str, Save]) -> str:
        filepath = os.path.join(Data._dir, filename)
        os.makedirs(Data._dir, exist_ok=True)

        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
        return filepath

    @staticmethod
    def load(filename: str) -> dict[str, Save]:
        filepath = os.path.join(Data._dir, filename)

        try:
            with open(filepath, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

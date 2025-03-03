import random
from dataclasses import dataclass
from enum import Enum

@dataclass
class ProductValues:
    emoji: str
    price: float

class Product(Enum):
    # herbs
    BASIL = ProductValues(emoji='🌿', price=3)
    MINT = ProductValues(emoji='🍃', price=2)
    PARSLEY = ProductValues(emoji='🌱', price=2.5)
    CHIVES = ProductValues(emoji='🧄', price=2)
    ROSEMARY = ProductValues(emoji='🌾', price=4)
    THYME = ProductValues(emoji='🌿', price=3.5)

    # trees
    OAK_WOOD = ProductValues(emoji='🪵', price=20)
    PINE_WOOD = ProductValues(emoji='🪵', price=15)
    MAPLE_SYRUP = ProductValues(emoji='🍁', price=7.5)
    WILLOW_WOOD = ProductValues(emoji='🪵', price=17.5)
    APPLE = ProductValues(emoji='🍎', price=5)

    # vegetables
    CARROT = ProductValues(emoji='🥕', price=2)
    TOMATO = ProductValues(emoji='🍅', price=3)
    LETTUCE = ProductValues(emoji='🥬', price=1.5)
    POTATO = ProductValues(emoji='🥔', price=2.5)
    PEPPER = ProductValues(emoji='🌶️', price=3.5)
    CUCUMBER = ProductValues(emoji='🥒', price=2.75)

    def __str__(self):
        return f'{self.value.emoji} {self.name.capitalize()} (${self.value.price:.2f})'

    @classmethod
    def end_turn(cls):
        for product in cls:
            product.value.price *= random.uniform(0.9, 1.1)
        print('Prices of products on the market have evolved')

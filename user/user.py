from data.save import Data
from exceptions import UserException, PlantException
from plants.plant import Plant
from product.product import Product
from utils.prompt import Prompt


class User(Data):
    def __init__(self, name: str, *, money: float = 0, products: dict[Product, int] = None):
        self.name = name
        self.money = money
        self.products: dict[Product, int] = products or {}

    def __str__(self):
        return f'{self.name} (${self.money:.2f}) - {sum(self.products.values())} product(s)'

    def __add__(self, money: float) -> 'User':
        self.money += money
        return self

    def __sub__(self, money: float) -> 'User':
        if money > self.money:
            raise UserException.Money(f"{self.name} doesn't have enough money")

        self.money -= money
        return self

    def to_str(self) -> str:
        return f'{self.name} (${self.money:.2f})'

    def details(self) -> str:
        return (f'{self}:' +
                ('\n  - ' if sum(self.products.values()) > 0 else '') +
                '\n  - '.join([f'{product}{f" - quantity: {quantity}" if quantity > 0 else ""}' for product, quantity in self.products.items()]))

    def buy(self, prompt: str = 'This', *, cost: float) -> bool:
        if Prompt.get_bool(f'{prompt} will cost you ${cost:.2f} - Confirm ? [y/n]:',
                           true_values=['y', 'yes'], false_values=['n', 'no']):
            try:
                self - cost
                return True
            except UserException.Money as e:
                print(f'Transaction cancelled. {e.message}')
                return False

        print('Transaction cancelled.')
        return False

    def refund(self, money: float) -> 'User':
        self + money
        return self

    def collect(self, plant: Plant) -> bool:
        try:
            if plant.product not in self.products:
                self.products[plant.product] = 0

            self.products[plant.product] += plant.collect()
            return True
        except (PlantException.Dead, PlantException.Growth) as e:
            print(f'{self.name} cannot collect {plant.product.name} form {plant.emojis}{type(plant).__name__}. {e.message}')
            return False

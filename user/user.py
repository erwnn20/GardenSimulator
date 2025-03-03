from data.save import Data
from exceptions import UserException
from product.product import Product
from utils.prompt import Prompt


class User(Data):
    def __init__(self, name: str, *, money: float = 0, products: dict[Product, int] = None):
        self.name = name
        self.money = money
        self.products: dict[Product, int] = products or {}

    def __str__(self):
        return f'{self.name} (${self.money:.2f}) - {len(self.products)} products'

    def __add__(self, money: float) -> 'User':
        self.money += money
        return self

    def __sub__(self, money: float) -> 'User':
        if money > self.money:
            raise UserException.Money(f"{self.name} doesn't have enough money")

        self.money -= money
        return self

    def str(self) -> str:
        return f'{self.name} (${self.money:.2f})'

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

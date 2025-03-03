from data.save import Data
from exceptions import UserException
from product.product import Product


class User(Data):
    def __init__(self, name: str, *, money: float = 0, products: dict[Product, int] = None):
        self.name = name
        self.money = money
        self.products: dict[Product, int] = products or {}

    def __str__(self):
        return f'{self.name} (${self.money:.2f}) - {len(self.products)} products'

    def str(self) -> str:
        return f'{self.name} (${self.money:.2f})'

    def buy(self, money: float) -> 'User':
        if money > self.money:
            raise UserException.Money(f"{self.name} doesn't have enough money")

        self.money -= money
        return self

    def refund(self, money: float) -> 'User':
        money += self.money
        return self

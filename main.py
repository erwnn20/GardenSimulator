import os
import random

from data.save import Data
from data.save import Save
from plants.garden import Garden
from plants.plantation import Plantation
from plants.soil import SoilType
from product.product import Product
from user.user import User
from utils.prompt import Prompt

clear = lambda: os.system('cls')


class Game:
    saves_filename = 'games.save'
    saves: dict[str, Save] = Data.load(saves_filename)

    def __init__(self):
        self.save: Save | None = None

    def _select_save(self) -> Save:
        return self.saves.get(
            list(self.saves.keys())[Prompt.select(
                prompt='Select save :',
                choices=[str(save) for save in list(self.saves.values())],
                display_func=lambda s: s
            ).index - 1])

    def select_save(self):
        match Prompt.select('What do you want to do ?', ['New game', 'Load a save'], lambda x: x) if len(
            self.saves) > 0 else 1:
            case 1:
                self.save = Save(
                    name='',
                    user=User(name=Prompt.get('Enter your name : ', expected_type=str), money=120.5),
                    garden=Garden(
                        Prompt.get('Enter garden name : ', expected_type=str),
                        plantations=[Plantation(size=5, soil=random.choice(list(SoilType)).value(), water_content=10)]
                    ),
                )
            case 2:
                self.save = self._select_save()
            case _:
                raise IndexError('Invalid game start option selection')

    def garden(self) -> bool:
        print(f'Your garden: {self.save.garden}\n')

        match Prompt.select('Select an action',
                            [
                                'Collect plantations products',
                                'Maintain your plantations',
                                'Manage your plantations',
                                'Exit',
                            ], lambda x: x).index:
            case 1:
                return game.save.garden.collect(game.save.user)
            case 2:
                return game.save.garden.maintain()
            case 3:
                return game.save.garden.manage(game.save.user)
            case _:
                return False

    def details(self):
        print('User:', self.save.user.details())
        print('\nGarden:', self.save.garden)

    def market(self) -> bool:
        sell = False

        saleable_items = [product for product, quantity in self.save.user.products.items() if quantity > 0]

        if not saleable_items:
            print('You have no products to sell')
            return False

        while True:
            selected_item = Prompt.select('What do you want to sell?',
                                          [*saleable_items, 'Exit'],
                                          lambda
                                              x: f'{x}{f" - quantity: {self.save.user.products[x]}" if isinstance(x, Product) else ""}'
                                          ).element
            match selected_item:
                case 'Exit':
                    return sell
                case _:
                    number_of_items = Prompt.get('How many do you want to sell?',
                                                 expected_type=int,
                                                 excluded_condition=lambda x: not 0 <= x <= self.save.user.products[
                                                     selected_item])
                    if 0 < number_of_items <= self.save.user.products[selected_item]:
                        money: float = selected_item.value.price * number_of_items
                        self.save.user + money
                        self.save.user.products[selected_item] -= number_of_items
                        print(f'You sold {number_of_items} item(s) of {selected_item} for ${money:.2f}.\n')

    def end_turn(self):
        self.save.garden.end_turn()
        Product.end_turn()

    @staticmethod
    def next():
        input('\nPress ENTER to continue ')
        clear()


game = Game()

if __name__ == '__main__':
    clear()
    print('Welcome to Garden Simulator')
    game.next()
    clear()

    game.select_save()
    while True:
        clear()
        actions = 3
        while actions > 0:
            print(f'Remaining actions: {actions}')
            match Prompt.select('Where do you want to go ?',
                                [
                                    'My details',
                                    'My Garden',
                                    'Market',
                                    'End turn',
                                ], lambda x: x).index:
                case 1:
                    clear()
                    game.details()
                    game.next()
                case 2:
                    clear()
                    actions -= 1 if game.garden() else 0
                    game.next()
                case 3:
                    clear()
                    actions -= 1 if game.market() else 0
                    game.next()
                case 4:
                    clear()
                    actions = 0

        game.end_turn()

        game.next()

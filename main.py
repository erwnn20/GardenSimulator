import os
import random

from data.save import Data
from data.save import Save
from plants.garden import Garden
from plants.plantation import Plantation
from plants.soil import SoilType
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
                    user=None,
                    garden=Garden(input('Enter garden name : '),
                                  plantations=[Plantation(size=5, soil=random.choice(list(SoilType)).value())]),
                )
            case 2:
                self.save = self._select_save()
            case _:
                raise IndexError('Invalid game start option selection')

    def garden(self) -> bool:
        print(f'Your garden: {self.save.garden}\n')

        match Prompt.select('Select an action',
                            [
                                'Maintain your plantations',
                                'Manage your plantations',
                                'Exit',
                            ], lambda x: x).index:
            case 1:
                return game.save.garden.maintain()
            case 2:
                return game.save.garden.manage(game.save.user)
            case _:
                return False


game = Game()

if __name__ == '__main__':
    clear()
    print('Welcome to Garden Simulator')
    input('Press ENTER to continue')
    clear()

    game.select_save()
    while True:
        actions = 3
        while actions > 0:
            clear()
            match Prompt.select('Where do you want to go ?',
                                [
                                    'My details',
                                    'My Garden',
                                    'Market',
                                    'End turn',
                                ], lambda x: x).index:
                case 1:
                    game.user()
                case 2:
                    actions -= 1 if game.garden() else 0
                case 3:
                    actions -= 1 if game.market() else 0
                case 4:
                    actions = 0

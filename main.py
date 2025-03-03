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
    prompt = Prompt()
    saves_filename = 'games.save'
    saves: dict[str, Save] = Data.load(saves_filename)

    def __init__(self):
        self.save: Save | None = None

    def _select_save(self) -> Save:
        return self.saves.get(
            list(self.saves.keys())[self.prompt.select(
                prompt='Select save :',
                choices=[str(save) for save in list(self.saves.values())],
                display_func=lambda s: s
            ).index - 1])

    def select_save(self):
        match self.prompt.select('What do you want to do ?', ['New game', 'Load a save'], lambda x: x) if len(
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


game = Game()

if __name__ == '__main__':
    clear()
    print('Welcome to Garden Simulator')
    input('Press ENTER to continue')
    clear()

    while True:
        game.select_save()

        actions = 3
        while actions > 0:
            clear()
            print(f'Your garden: {game.save.garden}\n')

            match game.prompt.select('Select an action',
                                     [
                                         'Maintain your plantations',
                                         'Manage your plantations',
                                         'End turn',
                                         'Save and Quit',
                                     ], lambda x: x).index:
                case 1:
                    actions -= 1 if game.save.garden.maintain() else 0
                case 2:
                    actions -= 1 if game.save.garden.manage(game.save.user) else 0

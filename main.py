import os

from data.save import Data
from data.save import Save
from plants.garden import Garden
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
                choices=self.saves,
                display_func=lambda _save: str(self.saves[_save])).index - 1])

    def select_save(self):
        match self.prompt.select('What do you want to do ?', ['New game', 'Load a save'], lambda x: x) if len(
            self.saves) > 0 else 1:
            case 1:
                self.save = Save(
                    name='',
                    user=None,
                    garden=Garden(input('Enter garden name : ')),
                )
            case 2:
                self.save = self._select_save()
            case _:
                raise IndexError('Invalid game start option selection')

    def maintain(self) -> bool:
        match self.prompt.select('What do you want to do ?',
                                 [
                                     'Watering',
                                     'Fertilizing',
                                     'Pruning/Maintenance',
                                     'Exit'
                                 ], lambda x: x).element:
            case 'Watering':
                return game.save.garden.watering()
            case 'Fertilizing':
                return game.save.garden.fertilizing()
            case 'Pruning/Maintenance':
                return game.save.garden.maintain()
            case 'Exit':
                return True
        return False

    def manage(self) -> bool:
        match self.prompt.select('What do you want to do ?',
                                 [
                                     'Plant a new seed',
                                     'Uproot a plant',
                                     'Change soil',
                                     'Exit'
                                 ], lambda x: x).element:
            case 'Plant a new seed':
                return game.save.garden.plant_new()
            case 'Uproot a plant':
                return game.save.garden.uproot(self.save.user)
            case 'Change soil':
                return game.save.garden.change_soil()
            case 'Exit':
                pass

        return False


game = Game()

if __name__ == '__main__':
    clear()
    print('Welcome to Garden Simulator')
    input('Press ENTER to continue')
    clear()

    while True:
        game.select_save()

        end_turn = False
        while not end_turn:
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
                    end_turn = game.maintain()
                case 2:
                    end_turn = game.manage()

from enum import Enum
from typing import Callable

from data.save import Data
from exceptions import PlantationException, PlantException
from plants.add.fertilizer import FertilizerType
from plants.plant import PlantType, Plant
from plants.plantation import Plantation
from plants.soil import SoilType
from user.user import User
from utils.prompt import Prompt


class Garden(Data):
    def __init__(self, name: str, *, plantations: list[Plantation] = None):
        self.name = name
        self._plantations: list[Plantation] = plantations or []

    def __str__(self) -> str:
        return (
                f'{self.name}: {len(self.plantations(Garden.PlantationSelectType.SEEDED))}/{len(self.plantations())} plant(s)' +
                ('\n  - ' if len(self.plantations()) > 0 else '') +
                '\n  - '.join([str(p) for p in self.plantations()]))

    def __add__(self, new_plant: Plantation | list[Plantation]):
        self._plantations += new_plant if isinstance(new_plant, list) else [new_plant]
        return self

    class PlantationSelectType(Enum):
        ALL = 0
        EMPTY = 1
        SOILED = 2
        SOILED_NO_SEED = 3
        SEEDED = 4

    def plantations(self, plantation_select_type: PlantationSelectType = PlantationSelectType.ALL) -> list[Plantation]:
        return [plantation for plantation in self._plantations if {
            Garden.PlantationSelectType.ALL: True,
            Garden.PlantationSelectType.EMPTY: plantation.is_empty,
            Garden.PlantationSelectType.SOILED: plantation.is_soiled,
            Garden.PlantationSelectType.SOILED_NO_SEED: plantation.is_soiled_no_seed,
            Garden.PlantationSelectType.SEEDED: plantation.is_seeded,
        }[plantation_select_type]]

    def to_str(self) -> str:
        avg_health = 0.0 if len(self.plantations(Garden.PlantationSelectType.SEEDED)) == 0 else sum(
            [p1.plant.health for p1 in self.plantations(Garden.PlantationSelectType.SEEDED)]) / len(
            self.plantations(Garden.PlantationSelectType.SEEDED))
        avg_growth = 0.0 if len(self.plantations(Garden.PlantationSelectType.SEEDED)) == 0 else sum(
            [p2.plant.growth for p2 in self.plantations(Garden.PlantationSelectType.SEEDED)]) / len(
            self.plantations(Garden.PlantationSelectType.SEEDED))

        return (
            f"Garden {self.name}: {len(self.plantations(Garden.PlantationSelectType.SEEDED))}/{len(self.plantations(Garden.PlantationSelectType.ALL))} plant(s) "
            f"[avg -> health: {avg_health:.1f}% ; growth: {avg_growth * 100:.1f}%] ")

    def select_plantations(self, message: str, *, plantation_select_type: PlantationSelectType, size: int | None = None,
                           plantation_str: Callable[[Plantation], str] = lambda p: str(p)) -> list[Plantation]:
        out_list: list[Plantation] = []
        plant_list: list[Plantation] = self.plantations(plantation_select_type)

        if not plant_list:
            print(
                f'there are no {plantation_select_type.name.lower() if plantation_select_type != Garden.PlantationSelectType.ALL else ""} plantation in {self.name}')
            return out_list

        while (len(out_list) < size) if size else True:
            choices = []
            if not size: choices.append('All')
            choices.extend([p for p in plant_list if p not in out_list])
            if not size: choices.append('Exit')

            selected = Prompt.select(message, choices,
                                     lambda x: plantation_str(x) if isinstance(x, Plantation) else str(x)).element
            match selected:
                case 'All':
                    return plant_list
                case 'Exit':
                    return out_list
                case _:
                    out_list.append(selected)
                    print()

        return out_list

    def maintain(self) -> bool:
        match Prompt.select('What do you want to do ?',
                            [
                                'Watering',
                                'Fertilizing',
                                'Pruning/Maintenance',
                                'Exit'
                            ], lambda x: x).element:
            case 'Watering':
                return self.watering()
            case 'Fertilizing':
                return self.fertilizing()
            case 'Pruning/Maintenance':
                return self.maintain_plant()
            case _:
                return False

    def collect(self, user: User) -> bool:
        plantations = self.select_plantations('Which plantations do you want to collect?',
                                              plantation_select_type=Garden.PlantationSelectType.SEEDED)
        if not plantations: return False

        for plantation in plantations:
            if user.collect(plantation.plant):
                print(f'You have collected {plantation.plant.emojis}{type(plantation.plant).__name__} products.')

        return True

    def watering(self) -> bool:
        plantation_str: Callable[[Plantation], str] = lambda p: (f'Soil: {type(p.soil).__name__} | '
                                                                 f'{"Plant: " + f"{p.plant.emojis}{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, water needs: {p.plant.water_needs:.2f} L)" if p.plant else f"No plantation"} | '
                                                                 f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L')

        plantations = self.select_plantations('Which plantations do you want to water?',
                                              plantation_select_type=Garden.PlantationSelectType.SOILED,
                                              plantation_str=plantation_str)

        print()
        if plantations:
            print((f'Selected:\n'
                   '  - ' + '\n  - '.join([plantation_str(p) for p in plantations])))
            all_plantations = Prompt.select('You want to :',
                                            [
                                                'water all plantations equally',
                                                'choose the quantity of water for each plantation'
                                            ], lambda x: x).index == 1

            water: float | None = None
            if all_plantations:
                water = Prompt.get(
                    prompt='Enter the amount of water you want to use per plantation :',
                    expected_type=float,
                    excluded_condition=lambda x: x < 0.0
                )

            for plantation in plantations:
                if not all_plantations: print()
                plantation.watering_up(water if all_plantations else Prompt.get(
                    prompt=f'{type(plantation).__name__}: {plantation_str(plantation)}\n'
                           'Enter the amount of water you want to use for this plantation:',
                    expected_type=float,
                    excluded_condition=lambda x: x < 0.0
                ))

            print(f"\nYou've watered {len(plantations)} plantations in the {self.name} garden.\n")
            return True

        print('You have not selected any plantations to water.\n')
        return False

    def fertilizing(self) -> bool:
        fertilizer = FertilizerType.select()
        print()
        plantations = self.select_plantations('Which plantations do you want to fertilize?',
                                              plantation_select_type=Garden.PlantationSelectType.SOILED,
                                              plantation_str=lambda p: (
                                                  f'Soil: {type(p.soil).__name__} {"(fertilized) " if any(value > 0 for value in p.soil.fertilizers.values()) else ""}| '
                                                  f'{"Plant: " + f"{p.plant.emojis}{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, fertilize quantity: {p.plant.fertilizer_quantity:.2f}/{p.plant.fertilizer_limit:.2f})" if p.plant else f"No plantation"} | '
                                                  f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L'))

        print()
        if plantations:
            for plantation in plantations: plantation.fertilize(fertilizer)
            print(
                f'You have fertilized {len(plantations)} plantations in the {self.name} garden with {fertilizer.name.capitalize()}.')
            return True
        else:
            print('You have not selected any plantations to fertilize.')
        print()

        return False

    def maintain_plant(self) -> bool:
        if self.plantations(Garden.PlantationSelectType.SEEDED):
            for plantation in self.plantations(Garden.PlantationSelectType.SEEDED):
                try:
                    plantation.plant.maintain()
                except PlantException.Dead:
                    pass

            print(
                f"You've tended the {len(self.plantations(Garden.PlantationSelectType.SEEDED))} plants of the {self.name} garden.\n")
            return True

        print(f'There are no plants to maintain in the {self.name} garden.\n')
        return False

    def manage(self, user: User) -> bool:
        match Prompt.select('What do you want to do ?',
                            [
                                'Buy a new plantation',
                                'Plant a new seed',
                                'Uproot a plant',
                                'Change soil',
                                'Exit'
                            ], lambda x: x).element:
            case 'Buy a new plantation':
                return self.new_plantation(user)
            case 'Plant a new seed':
                return self.plant_new(user)
            case 'Uproot a plant':
                return self.uproot(user)
            case 'Change soil':
                return self.change_soil(user)
            case _:
                return False

    def new_plantation(self, user: User) -> bool:
        size = Prompt.get('Select the size of the plantation (between 1 and 10):',
                          expected_type=int,
                          excluded_condition=lambda x: (not 0 < x <= 10) or not isinstance(x, int))
        cost = 10 * size
        extra_cost = 2.5

        if not user.buy(f'Current money: ${user.money:.2f}. This plantation', cost=cost): return False

        print()
        soil_type = SoilType.select()
        print()

        plant: Plant | None = None
        plant_new = user.buy('Would you like to add a seed? It', cost=extra_cost)
        plant_payment_done = plant_new

        while True:
            if plant_new:
                plant = PlantType.select()()

            try:
                plantation = Plantation(
                    size=size,
                    soil=soil_type(),
                    plant=plant
                )
                self + plantation
                print(f'\nPlantation ({plantation}) added to the {self.name} garden')
                return True
            except PlantationException.Seed as ex:
                print(f'Error on plant type selection. {ex.message.title()}.\n')
                plant = None
                plant_new = Prompt.get_bool(
                    prompt=f'Would you like to select another plant ? {f"It will cost you an extra ${extra_cost:.2f}" if not plant_payment_done else ""}[y/n]:',
                    true_values=['yes', 'y'], false_values=['n', 'no'])

            if not plant_new and plant_payment_done:
                user.refund(extra_cost)

    def plant_new(self, user: User) -> bool:
        if len(self.plantations(Garden.PlantationSelectType.SOILED_NO_SEED)) == 0:
            print(f'You have no free space to plant a new seed in the {self.name} garden.')
            return False

        cost = 5.0
        if not user.buy(f'Current money: ${user.money:.2f}. Planting a new plant', cost=cost): return False

        plantation = self.select_plantations('Where do you want to plant your seed ?',
                                             plantation_select_type=Garden.PlantationSelectType.SOILED_NO_SEED,
                                             size=1)[0]

        print(f'Selected: {plantation}')
        plant_type = PlantType.select()

        try:
            plantation.plant_seed(plant_type())
            print(f'\nNew {plant_type.__name__} planted!')
            return True
        except (PlantationException.Seed, PlantationException.Soil) as ex:
            print(f'You cannot plant your {plant_type} in this plantation.\n'
                  f'{ex.message.capitalize()}.')
            user.refund(cost)
            return False

    def uproot(self, user: User) -> bool:
        plant = self.select_plantations('Which plants do you want to uproot?',
                                        plantation_select_type=Garden.PlantationSelectType.SEEDED,
                                        size=1)[0].dig_up()
        print(f'A {type(plant).__name__} has been removed from the {self.name} garden')

        if user.collect(plant):
            print(f'You have collected {plant} products.')
        return True

    def change_soil(self, user: User) -> bool:
        plantation = self.select_plantations('Where do you want to change the soil ?',
                                             plantation_select_type=Garden.PlantationSelectType.SOILED,
                                             size=1)[0]

        cost = 5 * plantation.size
        if not user.buy(f'Current money: ${user.money:.2f}. Changing soil', cost=cost): return False

        print(f'Selected: {plantation}')
        soil_type = SoilType.select()

        try:
            plantation.change_soil(soil_type())
            print(f'\nSoil changed to {soil_type.__name__}.')
            return True
        except PlantationException.Soil as ex:
            print(f'{ex.message.capitalize()}. Please remove this plant before changing the soil.')
            user.refund(cost)
            return False

    def end_turn(self):
        for plantation in self.plantations():
            plantation.end_turn()

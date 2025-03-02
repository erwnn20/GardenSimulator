from enum import Enum
from typing import Callable

from data.save import Data
from exceptions import PlantationException
from plants.add.fertilizer import FertilizerType
from plants.plant import PlantType
from plants.plantation import Plantation
from plants.soil import SoilType
from user.user import User
from utils.prompt import Prompt


class Garden(Data):
    def __init__(self, name: str):
        self.name = name
        self._plantations: list[Plantation] = []

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

    def str(self) -> str:
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

    def watering(self) -> bool:
        plant_str: Callable[[Plantation], str] = lambda p: (f'Soil: {type(p.soil).__name__} | '
                                                            f'{"Plant: " + f"{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, water needs: {p.plant.water_needs:.2f} L)" if p.plant else f"No plant"} | '
                                                            f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L')

        plants = self.select_plantations('Which plants do you want to water?',
                                         plantation_select_type=Garden.PlantationSelectType.SOILED,
                                         plantation_str=plant_str)

        print()
        if plants:
            print((f'Selected:\n'
                   '  - ' + '\n  - '.join([plant_str(p) for p in plants])))
            all_plants = Prompt.select('You want to :',
                                       [
                                           'water all plantations equally',
                                           'choose the quantity of water for each plantation'
                                       ], lambda x: x).index == 1

            water: float | None = None
            if all_plants:
                water = float(Prompt.get(
                    prompt='Enter the amount of water you want to use per plant :',
                    excluded_condition=lambda x: x < 0.0
                ))

            for plant in plants:
                if not all_plants: print()
                plant.watering_up(water if all_plants else float(Prompt.get(
                    prompt=f'{type(plant).__name__}: {plant_str(plant)}\n'
                           'Enter the amount of water you want to use for this plant:',
                    excluded_condition=lambda x: x < 0.0
                )))

            print(f"\nYou've watered {len(plants)} plants in the {self.name} garden.\n")
            return True

        print('You have not selected any plants to water.\n')
        return False

    def fertilizing(self) -> bool:
        fertilizer = FertilizerType.select()
        print()
        plants = self.select_plantations('Which plants do you want to fertilize?',
                                         plantation_select_type=Garden.PlantationSelectType.SOILED,
                                         plantation_str=lambda p: (
                                             f'Soil: {type(p.soil).__name__} {"(fertilized) " if any(value > 0 for value in p.soil.fertilizers.values()) else ""}| '
                                             f'{"Plant: " + f"{type(p.plant).__name__} (health: {p.plant.health:.1f}%, growth: {p.plant.growth:.1f}%, fertilize quantity: {p.plant.fertilizer_quantity:.2f}/{p.plant.fertilizer_limit:.2f})" if p.plant else f"No plant"} | '
                                             f'Water: {p.water_content:.2f}/{p.max_water_content:.2f} L'))

        print()
        if plants:
            for plant in plants: plant.fertilize(fertilizer)
            print(
                f'You have fertilized {len(plants)} plants in the {self.name} garden with {fertilizer.name.capitalize()}.')
        else:
            print('You have not selected any plants to fertilize.')
        print()

        return False

    def maintain(self) -> bool:
        if self.plantations(Garden.PlantationSelectType.SEEDED):
            for plantation in self.plantations(Garden.PlantationSelectType.SEEDED): plantation.plant.maintain()

            print(
                f"You've tended the {len(self.plantations(Garden.PlantationSelectType.SEEDED))} plants of the {self.name} garden.\n")
            return True

        print(f'There are no plants to maintain in the {self.name} garden.\n')
        return False

    def plant_new(self) -> bool:
        if len(self.plantations(Garden.PlantationSelectType.SOILED_NO_SEED)) == 0:
            print(f'You have no free space to plant a new seed in the {self.name} garden.')
            return False

        plantation = self.select_plantations('Where do you want to plant your seed ?',
                                             plantation_select_type=Garden.PlantationSelectType.SOILED_NO_SEED,
                                             size=1)[0]

        print(f'Selected: {plantation}')
        plant_type = PlantType.select()

        try:
            plantation.plant_seed(plant_type())
        except (PlantationException.Seed, PlantationException.Soil) as ex:
            print(f'You cannot plant your {plant_type} in this plantation.\n'
                  f'{ex.message.capitalize()}.')
            return False

        return True

    def uproot(self, user: User) -> bool:
        plant = self.select_plantations('Which plants do you want to uproot?',
                                        plantation_select_type=Garden.PlantationSelectType.SEEDED,
                                        size=1)[0].dig_up()

        return False

    def change_soil(self) -> bool:
        plantation = self.select_plantations('Where do you want to change the soil ?',
                                             plantation_select_type=Garden.PlantationSelectType.SOILED,
                                             size=1)[0]

        print(f'Selected: {plantation}')
        soil_type = SoilType.select()

        try:
            plantation.change_soil(soil_type())
        except PlantationException.Soil as ex:
            print(f'{ex.message.capitalize()}. Please remove this plant before changing the soil.')
            return False

        return True

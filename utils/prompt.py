from dataclasses import dataclass
from typing import Callable, TypeVar, List

T = TypeVar('T')


class Prompt:
    @dataclass
    class SelectOutput:
        index: int
        element: T

    @staticmethod
    def select(prompt: str, choices: List[T], display_func: Callable[[T], str]) -> SelectOutput:
        if not choices:
            raise IndexError("Vous devez avoir au moins un choix")
        if len(choices) == 1:
            return Prompt.SelectOutput(1, choices[0])

        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"    {i} : {display_func(choice)}".replace("\n", "\n        "))

        index = Prompt.get("-> ", excluded_condition=lambda x: x < 1 or x > len(choices))
        return Prompt.SelectOutput(index, choices[index - 1])

    @staticmethod
    def get(prompt: str, *, excluded_condition: Callable[[T], bool] = lambda _: False) -> T:
        while True:
            try:
                value = input(f"{prompt} ").strip()
                if not value:
                    raise ValueError("Entrée vide non autorisée")

                converted_value = eval(value)
                if excluded_condition(converted_value):
                    print(f" - '{value}' n'est pas une entrée valide. Veuillez en saisir un autre.")
                    continue

                return converted_value
            except Exception:
                print(" - Entrée invalide.")

    # @staticmethod
    # def input(*, prompt: str = '', excluded_condition: Callable[[str], bool] = lambda _: False) -> str:
    #     if prompt:
    #         print(prompt, end='', flush=True)
    #
    #     user_input = ''
    #     while True:
    #         # key = sys.stdin.read(1)
    #         key = keyboard.read_key()
    #         if key == "\n":
    #             break
    #         if key == "\b" and user_input:
    #             user_input = user_input[:-1]
    #             sys.stdout.write("\b \b")
    #             sys.stdout.flush()
    #         elif not excluded_condition(key):
    #             user_input += key
    #             sys.stdout.write(key)
    #             sys.stdout.flush()
    #
    #     return user_input.strip()

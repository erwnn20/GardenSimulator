from dataclasses import dataclass
from typing import Callable, TypeVar, List, Type

T = TypeVar('T', int, float, str)


class Prompt:
    @dataclass
    class SelectOutput:
        index: int
        element: T

    @staticmethod
    def select(prompt: str, choices: List[T], display_func: Callable[[T], str]) -> SelectOutput:
        if not choices:
            raise IndexError("You must have at least one choice")
        if len(choices) == 1:
            return Prompt.SelectOutput(1, choices[0])

        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"    {i} : {display_func(choice)}".replace("\n", "\n        "))

        index = Prompt.get("-> ", expected_type=int, excluded_condition=lambda x: x < 1 or x > len(choices))
        return Prompt.SelectOutput(index, choices[index - 1])

    @staticmethod
    def get_bool(prompt: str, *, true_values: list[str], false_values: list[str]) -> bool:
        if not true_values:
            raise IndexError("You must have at least one 'true_values'")
        if not false_values:
            raise IndexError("You must have at least one 'false_values'")

        value = Prompt.get(prompt, expected_type=str,
                           excluded_condition=lambda x: x not in [*true_values, *false_values])

        if value in true_values: return True
        if value in false_values: return False
        raise IndexError(f"'{value}' is not a valid value for '{prompt}'")

    @staticmethod
    def get(prompt: str, *, expected_type: Type[T], excluded_condition: Callable[[T], bool] = lambda _: False) -> T:
        while True:
            try:
                value = input(f"{prompt} ").strip()
                if not value:
                    raise ValueError("Unauthorized empty entry")

                converted_value = expected_type(value)
                if excluded_condition(converted_value):
                    print(f" - '{value}' is not a valid entry. Please enter a new one.")
                    continue

                return converted_value
            except Exception:
                print(" - Invalid input.")

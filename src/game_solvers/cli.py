"""Module holding PyApp CLI entrypoint.

Logic to be kept to a minimum in this module and call out to other modules.
"""

from pyapp.app import CliApplication, argument

from game_solvers.games.wordle import Wordle

app = CliApplication(
    description="Matt's Game Solver",
)
cli_main = app.dispatch

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WORDLE_POS_DIGITS = "12345"


class WordleCLI:
    """Group of CLI commands that help solve wordle problems."""

    group = app.create_command_group(
        "wordle", help_text="Wordle solvers and helper functions"
    )

    # Input Parsers
    @staticmethod
    def parse_green(input_value: str | None) -> list[tuple[str, int]]:
        """Validate and parse input data for green wordle values.

        :param input_value: input provided by the user for green letters.
        :return: Validated list of green letters and positions
        """
        if not input_value:
            return []

        greens = []
        for split in input_value.split(","):
            if len(split) != 2:
                raise ValueError(
                    f"Each input for green letters must a letter "
                    f"followed by a number from 1-5. Input {split} is invalid."
                )

            if split[0].upper() not in LETTERS:
                raise ValueError(
                    f"Each input for green letters must a letter "
                    f"followed by a number from 1-5. Input {split} is invalid."
                )

            if split[1] not in WORDLE_POS_DIGITS:
                raise ValueError(
                    f"Each input for green letters must a letter "
                    f"followed by a number from 1-5. Input {split} is invalid."
                )

            greens.append((split[0].upper(), int(split[1])))

        return greens

    @staticmethod
    def parse_yellow(input_value: str | None) -> list[tuple[str, list[int]]]:
        """Validate and parse input data for yellow wordle values.

        :param input_value: input provided by the user for yellow letters.
        :return: Validated list of yellow letters and non-positions
        """
        if not input_value:
            return []

        yellows = []
        for split in input_value.split(","):
            if not 2 <= len(split) <= 5:
                raise ValueError(
                    f"Each input for yellow letters must a letter followed by "
                    f"one to four numbers from 1-5. Input {split} is invalid."
                )

            if split[0].upper() not in LETTERS:
                raise ValueError(
                    f"Each input for yellow letters must a letter followed by "
                    f"one to four numbers from 1-5. Input {split} is invalid."
                )

            for should_be_digit in split[1:]:
                if should_be_digit not in WORDLE_POS_DIGITS:
                    raise ValueError(
                        f"Each input for yellow letters must a letter followed by "
                        f"one to four numbers from 1-5. Input {split} is invalid."
                    )

            yellows.append((split[0].upper(), [int(digit) for digit in split[1:]]))

        return yellows

    @staticmethod
    def parse_grey(input_value: str | None) -> list[str]:
        """Validate and parse input data for grey wordle values.

        :param input_value: input provided by the user for grey letters.
        :return: Validated list of grey letters
        """
        if not input_value:
            return []

        greys = []
        for split in input_value.split(","):
            if len(split) > 1:
                raise ValueError(
                    f"Each input for grey letters must a single letter. "
                    f"Input {split} is invalid."
                )

            if split.upper() not in LETTERS:
                raise ValueError(
                    f"Each input for grey letters must a single letter. "
                    f"Input {split} is invalid."
                )

            greys.append(split.upper())

        return greys

    # Commands
    @staticmethod
    @group.command(
        help_text=(
            "Given the current state of a wordle game, "
            "provide the five best solutions"
        )
    )
    def solutions(
        *,
        green_letters: str = argument(
            "--green",
            default=None,
            help_text=(
                "A letter with a known position. "
                "Should be provided as a comma seperated list "
                "of letters and their position. "
                "e.g. `--green A2,Y5`"
            ),
        ),
        yellow_letters: str = argument(
            "--yellow",
            default=None,
            help_text=(
                "A letter known to be in the word, "
                "but with an unknown position. "
                "Should be provided as a comma-seperated list "
                "letters and all the positions it cannot be. "
                "e.g. `--yellow A13,Y1234`"
            ),
        ),
        grey_letters: str = argument(
            "--grey",
            default=None,
            help_text=(
                "A letter known not to be in the word. "
                "Should be provided as a comma-seperated list letters"
                "e.g. `--grey R,C`"
            ),
        ),
    ):
        """Given the current state of a wordle game, provide the five best solutions."""
        greens = WordleCLI.parse_green(green_letters)
        yellows = WordleCLI.parse_yellow(yellow_letters)
        greys = WordleCLI.parse_grey(grey_letters)

        Wordle(greens, yellows, greys).solutions()

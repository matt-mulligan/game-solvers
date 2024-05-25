"""Module for WordleSolver game solver functionality."""

from ..common.resources import read_data_resource


class WordleSolver:
    """WordleSolver class."""

    def __init__(
        self,
        greens: list[tuple[str, int]],
        yellows: list[tuple[str, list[int]]],
        greys: list[str],
    ):
        """Initialize the WordleSolver game solver class."""
        self.greens: list[tuple[str, int]] = greens
        self.yellows: list[tuple[str, list[int]]] = yellows
        self.greys: list[str] = greys
        self.dictionary = self.prep_words()

    @staticmethod
    def prep_words() -> list[str]:
        """Load wordle game words from resources. Set all to capitals."""
        return [word.upper() for word in read_data_resource("words_alpha_five_letters.txt")[0]]

    def solutions(self) -> None:
        """Attempt to solve wordle game."""
        pass

    def valid_word(self, word: str) -> bool:
        """Check given word against the known letter information.

        :param word: the word to check
        """
        # rule out any words that do not have the green letters in the known position
        # note index access is zero-index and user input is one-index, hence the `-1`
        if not all(word[pos - 1] == green for green, pos in self.greens):
            return False

        # rule out any words that don't have the required yellow letters in possible correct positions
        # note index access is zero-index and user input is one-index, hence the `-1`
        for yellow, incorrect_positions in self.yellows:
            possible_positions = [pos for pos in [0, 1, 2, 3, 4] if pos + 1 not in incorrect_positions]
            if not any(word[pos] == yellow for pos in possible_positions):
                return False

        # rule out any words containing a known letter to not be in the word
        if any(grey in word for grey in self.greys):
            return False

        return True

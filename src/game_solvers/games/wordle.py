"""Module for WordleSolver game solver functionality."""

import logging

from ..common.reporting import report_wordle_solutions
from ..common.resources import read_data_resource

logger = logging.getLogger("WordleSolver")


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
        self.distribution = self.calculate_distribution(self.dictionary)

    @staticmethod
    def prep_words() -> list[str]:
        """Load wordle game words from resources. Set all to capitals.

        :return: list of five-letter words, all in upper case.
        """
        return [word.upper() for word in read_data_resource("words_alpha_five_letters.txt")[0]]

    @staticmethod
    def calculate_distribution(words: list[str]) -> dict[str, int]:
        """Calculate distribution of letters for the given words.

        :return: dictionary containing all letters and their occurrence count in given words
        """
        distribution = {letter: 0 for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        for word in words:
            for letter in word:
                distribution[letter] += 1

        return distribution

    def solutions(self) -> None:
        """Attempt to solve wordle game."""
        valid_words = [word for word in self.dictionary if self.valid_word(word)]

        scored_words = self._generate_scored_words(valid_words)
        non_repeating_words = self._generate_non_repeating_words(scored_words)
        new_char_words = self._generate_new_char_words(self.dictionary)

        report_wordle_solutions(
            self.greens, self.yellows, self.greys, scored_words[:10], non_repeating_words[:10], new_char_words[:10]
        )

    def valid_word(self, word: str) -> bool:
        """Check given word against the known letter information.

        :param word: the word to check
        :return: True if word is valid, False otherwise
        """
        # rule out any words that do not have the green letters in the known position
        # note index access is zero-index and user input is one-index, hence the `-1`
        if not all(word[pos - 1] == green for green, pos in self.greens):
            return False

        # rule out any words that don't have the required yellow letters in possible correct positions
        # note index access is zero-index and user input is one-index, hence the `-1`
        for yellow, incorrect_positions in self.yellows:
            # rule out any word with a yellow letter in a known incorrect position
            if any(word[pos - 1] == yellow for pos in incorrect_positions):
                return False

            # rule out any word without the yellow letter in one of the possible positions
            # must also account for already green instances of the same letter
            green_already = [green_pos for green_letter, green_pos in self.greens if green_letter == yellow]
            not_allowed_positions = green_already + incorrect_positions

            possible_positions = [pos for pos in [0, 1, 2, 3, 4] if pos + 1 not in not_allowed_positions]
            if not any(word[pos] == yellow for pos in possible_positions):
                return False

        # rule out any words containing a known letter to not be in the word
        if any(grey in word for grey in self.greys):
            return False

        return True

    @staticmethod
    def score_word(word: str, distribution: dict[str, int]) -> int:
        """Score given word based on distribution of letters provided.

        Note each reoccurrence of a letter in a word is scored with a 50% reduction stacked

        :param word: the word to score
        :param distribution: dictionary containing all letters and their occurrence count
        :return: total score of the word
        """
        seen: dict[str, int] = {}
        score: int = 0

        for letter in word:
            base_score = distribution.get(letter, 0)
            seen_count = seen.get(letter, 0)

            score += {
                0: base_score,
                1: int(round(base_score * 0.5, 0)),
                2: int(round(base_score * 0.25, 0)),
                3: int(round(base_score * 0.125, 0)),
                4: int(round(base_score * 0.0675, 0)),
            }[seen_count]

            seen[letter] = seen_count + 1

        return score

    def _generate_scored_words(self, words: list[str]) -> list[tuple[str, int]]:
        """Generate an ordered list of valid words and their scores based on the base scoring distribution.

        :param words: List of valid words for the solution that require scoring.
        :return: ordered list of tuples containing valid words and their scores.
        """
        scored_words = [(word, self.score_word(word, self.distribution)) for word in words]

        return sorted(scored_words, key=lambda word_tuple: word_tuple[1], reverse=True)

    @staticmethod
    def _generate_non_repeating_words(scored_words: list[tuple[str, int]]) -> list[tuple[str, int]]:
        """Generate a list of scored valid words that do not contain repeated letters.

        :param scored_words: ordered list of tuples containing valid words and their scores.
        :return: ordered list of tuples containing valid words, without any repeating characters,
            and their scores
        """
        return [(word, score) for word, score in scored_words if len(word) == len(set(word))]

    def _generate_new_char_words(self, all_words: list[str]) -> list[tuple[str, int]]:
        """Generate a list of scored valid words only contain letters never used before in this game.

        :param all_words: ordered list of tuples containing valid words and their scores.
        :return: ordered list of tuples containing valid words, with only letters never used before in this game,
            and their scores
        """
        used_letters = {*[green[0] for green in self.greens], *[yellow[0] for yellow in self.yellows], *self.greys}

        new_char_words = [
            (word, self.score_word(word, self.distribution))
            for word in all_words
            if all(letter not in used_letters for letter in word)
        ]

        return sorted(new_char_words, key=lambda word_tuple: word_tuple[1], reverse=True)

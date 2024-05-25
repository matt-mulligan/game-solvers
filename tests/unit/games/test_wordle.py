from unittest.mock import patch

from game_solvers.games.wordle import WordleSolver
from pytest import fixture, mark


class TestWordleSolver:
    @fixture
    def solver_empty(self):
        """Empty Solver, Beginning Game State."""
        return WordleSolver([], [], [])

    @fixture
    def solver_greens(self):
        """Solver setup with two green letters and nothing else"""
        return WordleSolver([("A", 3), ("D", 5)], [], [])

    @fixture
    def solver_yellows(self):
        """Solver setup with two green letters and nothing else"""
        return WordleSolver([], [("M", [3, 4]), ("Y", [1])], [])

    @fixture
    def solver_greys(self):
        """Solver setup with two green letters and nothing else"""
        return WordleSolver([], [], ["Z", "W", "H", "C"])

    @fixture
    def solver_full(self):
        """Solver setup with two green letters and nothing else"""
        return WordleSolver([("A", 3), ("D", 5)], [("Y", [4, 5])], ["Z", "N", "C", "H"])

    @patch("game_solvers.games.wordle.WordleSolver.prep_words")
    def test_when_init_and_no_args_then_correct_values_set(self, prep_words):
        prep_words.return_value = ["AAHED", "AALII", "AARGH", "AARON"]

        actual = WordleSolver([], [], [])

        assert actual.greens == []
        assert actual.yellows == []
        assert actual.greys == []
        assert actual.dictionary == ["AAHED", "AALII", "AARGH", "AARON"]

        prep_words.assert_called_once_with()

    @patch("game_solvers.games.wordle.WordleSolver.prep_words")
    def test_when_init_and_all_args_then_correct_values_set(self, prep_words):
        prep_words.return_value = ["AAHED", "AALII", "AARGH", "AARON"]

        actual = WordleSolver([("A", 3), ("D", 5)], [("M", [3, 4]), ("Y", [1])], ["Z", "W", "H", "C"])

        assert actual.greens == [("A", 3), ("D", 5)]
        assert actual.yellows == [("M", [3, 4]), ("Y", [1])]
        assert actual.greys == ["Z", "W", "H", "C"]
        assert actual.dictionary == ["AAHED", "AALII", "AARGH", "AARON"]

        prep_words.assert_called_once_with()

    @patch("game_solvers.games.wordle.read_data_resource")
    def test_when_prep_words_then_all_words_upper_case(self, read_data_resource, solver_empty):
        read_data_resource.return_value = [["aahed", "aalii", "aargh", "aaron"]]

        actual = solver_empty.prep_words()
        assert actual == ["AAHED", "AALII", "AARGH", "AARON"]
        read_data_resource.assert_called_once_with("words_alpha_five_letters.txt")

    @mark.parametrize("word", ["ABAMA", "CUBIC", "HEIRS", "SHRIP", "ZOSMA"])
    def test_when_valid_word_and_no_info_then_all_words_pass(self, word, solver_empty):
        assert solver_empty.valid_word(word)

    @mark.parametrize(
        "word, valid_state",
        [
            ("ABAMA", False),
            ("PLAUD", True),
            ("HEIRS", False),
            ("STAND", True),
            ("SPEND", False),
        ],
    )
    def test_when_valid_word_and_green_info_then_words_correctly_checked(self, word, valid_state, solver_greens):
        assert solver_greens.valid_word(word) is valid_state

    @mark.parametrize(
        "word, valid_state",
        [
            ("ABAMA", False),
            ("AMPLY", True),
            ("HEIRS", False),
            ("MAYER", True),
            ("SPEND", False),
        ],
    )
    def test_when_valid_word_and_yellow_info_then_words_correctly_checked(self, word, valid_state, solver_yellows):
        assert solver_yellows.valid_word(word) is valid_state

    @mark.parametrize(
        "word, valid_state",
        [
            ("ZEBRA", False),
            ("AMPLY", True),
            ("HEIRS", False),
            ("MAYER", True),
            ("CATCH", False),
        ],
    )
    def test_when_valid_word_and_grey_info_then_words_correctly_checked(self, word, valid_state, solver_greys):
        assert solver_greys.valid_word(word) is valid_state

    @mark.parametrize(
        "word, valid_state",
        [
            ("ZEBRA", False),
            ("AMPLY", False),
            ("HEIRS", False),
            ("MAYER", False),
            ("YEARD", True),
        ],
    )
    def test_when_valid_word_and_all_info_then_words_correctly_checked(self, word, valid_state, solver_full):
        assert solver_full.valid_word(word) is valid_state

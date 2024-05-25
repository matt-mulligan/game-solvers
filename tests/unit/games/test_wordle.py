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

    @patch("game_solvers.games.wordle.WordleSolver.calculate_distribution")
    @patch("game_solvers.games.wordle.WordleSolver.prep_words")
    def test_when_init_and_no_args_then_correct_values_set(self, prep_words, calculate_distribution):
        prep_words.return_value = ["AAHED", "AALII", "AARGH", "AARON"]
        calculate_distribution.return_value = {"A": 8, "D": 5, "H": 5}

        actual = WordleSolver([], [], [])

        assert actual.greens == []
        assert actual.yellows == []
        assert actual.greys == []
        assert actual.dictionary == ["AAHED", "AALII", "AARGH", "AARON"]
        assert actual.distribution == {"A": 8, "D": 5, "H": 5}

        prep_words.assert_called_once_with()
        calculate_distribution.assert_called_once_with(["AAHED", "AALII", "AARGH", "AARON"])

    @patch("game_solvers.games.wordle.WordleSolver.calculate_distribution")
    @patch("game_solvers.games.wordle.WordleSolver.prep_words")
    def test_when_init_and_all_args_then_correct_values_set(self, prep_words, calculate_distribution):
        prep_words.return_value = ["AAHED", "AALII", "AARGH", "AARON"]
        calculate_distribution.return_value = {"A": 8, "D": 5, "H": 5}

        actual = WordleSolver([("A", 3), ("D", 5)], [("M", [3, 4]), ("Y", [1])], ["Z", "W", "H", "C"])

        assert actual.greens == [("A", 3), ("D", 5)]
        assert actual.yellows == [("M", [3, 4]), ("Y", [1])]
        assert actual.greys == ["Z", "W", "H", "C"]
        assert actual.dictionary == ["AAHED", "AALII", "AARGH", "AARON"]
        assert actual.distribution == {"A": 8, "D": 5, "H": 5}

        prep_words.assert_called_once_with()
        calculate_distribution.assert_called_once_with(["AAHED", "AALII", "AARGH", "AARON"])

    @patch("game_solvers.games.wordle.read_data_resource")
    def test_when_prep_words_then_all_words_upper_case(self, read_data_resource, solver_empty):
        read_data_resource.return_value = [["aahed", "aalii", "aargh", "aaron"]]

        actual = solver_empty.prep_words()
        assert actual == ["AAHED", "AALII", "AARGH", "AARON"]
        read_data_resource.assert_called_once_with("words_alpha_five_letters.txt")

    def test_when_calculate_distribution_and_subset_words_then_correct_dict_returned(self, solver_empty):
        actual = solver_empty.calculate_distribution(["AAHED", "AALII", "AARGH", "AARON"])
        assert actual == {
            "A": 8,
            "B": 0,
            "C": 0,
            "D": 1,
            "E": 1,
            "F": 0,
            "G": 1,
            "H": 2,
            "I": 2,
            "J": 0,
            "K": 0,
            "L": 1,
            "M": 0,
            "N": 1,
            "O": 1,
            "P": 0,
            "Q": 0,
            "R": 2,
            "S": 0,
            "T": 0,
            "U": 0,
            "V": 0,
            "W": 0,
            "X": 0,
            "Y": 0,
            "Z": 0,
        }

    def test_when_calculate_distribution_and_full_dictionary_then_correct_dict_returned(self, solver_empty):
        actual = solver_empty.calculate_distribution(solver_empty.dictionary)
        assert actual == {
            "A": 8393,
            "B": 2090,
            "C": 2744,
            "D": 2813,
            "E": 7802,
            "F": 1238,
            "G": 1971,
            "H": 2284,
            "I": 5067,
            "J": 376,
            "K": 1743,
            "L": 4247,
            "M": 2494,
            "N": 4044,
            "O": 5219,
            "P": 2299,
            "Q": 139,
            "R": 5144,
            "S": 6537,
            "T": 4189,
            "U": 3361,
            "V": 878,
            "W": 1171,
            "X": 361,
            "Y": 2522,
            "Z": 474,
        }

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

    @mark.parametrize(
        "word, expected",
        [
            ("ABAMA", 29763),
            ("PLAUD", 21113),
            ("HEIRS", 26834),
            ("STAND", 25976),
            ("SPEND", 23495),
        ],
    )
    def test_when_score_word_then_correct_scores_produced(self, word, expected, solver_empty):
        actual = solver_empty.score_word(word, solver_empty.distribution)
        assert actual == expected

"""Rule tests use synthetic words, not instructor resources."""

import unittest

from game import GameFinishedError, HangmanGame, InvalidGuessError


class GameTests(unittest.TestCase):
    def test_initial_public_state(self):
        self.assertEqual(HangmanGame("Apple").to_state(), {
            "pattern": "_ _ _ _ _", "guessed_letters": [],
            "incorrect_letters": [], "remaining_guesses": 6, "status": "playing",
        })

    def test_correct_guess_reveals_all_positions(self):
        state = HangmanGame("apple").guess("P")
        self.assertEqual(state["pattern"], "_ p p _ _")
        self.assertEqual(state["guessed_letters"], ["p"])
        self.assertEqual(state["remaining_guesses"], 6)
        self.assertNotIn("word", state)

    def test_wrong_guess_costs_one_life(self):
        state = HangmanGame("apple").guess("z")
        self.assertEqual(state["incorrect_letters"], ["z"])
        self.assertEqual(state["remaining_guesses"], 5)

    def test_invalid_guesses_do_not_mutate(self):
        for letter in ("", "ab", " a", "a ", "1", "!", "é", "İ", "\n", None, 1, [], {}):
            with self.subTest(letter=letter):
                game = HangmanGame("apple")
                before = game.to_state()
                with self.assertRaises(InvalidGuessError):
                    game.guess(letter)
                self.assertEqual(before, game.to_state())

    def test_duplicates_are_case_insensitive_and_do_not_mutate(self):
        for letter in ("a", "z"):
            with self.subTest(letter=letter):
                game = HangmanGame("apple")
                before = game.guess(letter)
                with self.assertRaises(InvalidGuessError):
                    game.guess(letter.upper())
                self.assertEqual(before, game.to_state())

    def test_win_reveals_word_and_blocks_further_guesses(self):
        game = HangmanGame("apple")
        game.guess("z")
        for letter in "aple":
            state = game.guess(letter)
        self.assertEqual(state["status"], "won")
        self.assertEqual(state["word"], "apple")
        self.assertEqual(state["pattern"], "a p p l e")
        self.assertEqual(state["remaining_guesses"], 5)
        with self.assertRaises(GameFinishedError):
            game.guess("x")
        self.assertEqual(state, game.to_state())

    def test_loss_occurs_on_sixth_miss_and_blocks_further_guesses(self):
        game = HangmanGame("apple")
        for index, letter in enumerate("bcdfgh", start=1):
            state = game.guess(letter)
            self.assertEqual(state["remaining_guesses"], 6 - index)
            self.assertEqual(state["status"], "lost" if index == 6 else "playing")
            self.assertEqual("word" in state, index == 6)
        self.assertEqual(state["word"], "apple")
        with self.assertRaises(GameFinishedError):
            game.guess("a")
        self.assertEqual(state, game.to_state())

    def test_snapshots_cannot_modify_game(self):
        game = HangmanGame("apple")
        snapshot = game.guess("z")
        snapshot["guessed_letters"].append("a")
        snapshot["incorrect_letters"].clear()
        snapshot["status"] = "won"
        self.assertEqual(game.to_state()["guessed_letters"], ["z"])
        self.assertEqual(game.to_state()["incorrect_letters"], ["z"])
        self.assertEqual(game.status, "playing")

    def test_games_are_independent(self):
        first, second = HangmanGame("apple"), HangmanGame("apple")
        first.guess("a")
        self.assertEqual(second.to_state()["guessed_letters"], [])

    def test_invalid_words(self):
        for word in ("", "two words", "a-b", "café", "123", None, 5):
            with self.subTest(word=word), self.assertRaises(ValueError):
                HangmanGame(word)

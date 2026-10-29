"""Temporary synthetic lists exercise the loader without instructor data."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from game import HangmanGame
from word_manager import WordListError, WordManager


class WordManagerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.samples = {"easy": "cat", "medium": "planet", "hard": "astronomy"}
        for difficulty, word in self.samples.items():
            (self.directory / f"{difficulty}.txt").write_text(word + "\n", encoding="utf-8")

    def test_all_difficulties_select_usable_words(self):
        manager = WordManager(self.directory)
        for difficulty, expected in self.samples.items():
            with self.subTest(difficulty=difficulty):
                word = manager.choose_word(difficulty)
                self.assertEqual(word, expected)
                self.assertEqual(HangmanGame(word).status, "playing")

    def test_normalization_deduplication_and_random_selection_pool(self):
        (self.directory / "easy.txt").write_text("\ufeff CAT \n\ncat\nDog\n", encoding="utf-8")
        manager = WordManager(self.directory)
        with patch("word_manager.random.choice", return_value="dog") as choose:
            self.assertEqual(manager.choose_word("easy"), "dog")
            choose.assert_called_once_with(("cat", "dog"))

    def test_invalid_difficulty(self):
        manager = WordManager(self.directory)
        for difficulty in ("Easy", "", "expert", None, [], 1):
            with self.subTest(difficulty=difficulty), self.assertRaises(ValueError):
                manager.choose_word(difficulty)

    def test_each_missing_list_is_reported(self):
        for difficulty in self.samples:
            path = self.directory / f"{difficulty}.txt"
            path.unlink()
            with self.subTest(difficulty=difficulty), self.assertRaisesRegex(WordListError, difficulty):
                WordManager(self.directory)
            path.write_text(self.samples[difficulty], encoding="utf-8")

    def test_empty_list_is_rejected(self):
        (self.directory / "easy.txt").write_text(" \n\n", encoding="utf-8")
        with self.assertRaisesRegex(WordListError, "empty"):
            WordManager(self.directory)

    def test_invalid_entries_report_line(self):
        for word in ("two words", "can't", "café", "abc1", "a-b", "Kelvin"):
            (self.directory / "easy.txt").write_text("cat\n" + word, encoding="utf-8")
            with self.subTest(word=word), self.assertRaisesRegex(WordListError, "line 2"):
                WordManager(self.directory)

    def test_invalid_encoding_is_reported(self):
        (self.directory / "easy.txt").write_bytes(b"\xff")
        with self.assertRaisesRegex(WordListError, "Cannot read"):
            WordManager(self.directory)


class ProjectWordListTests(unittest.TestCase):
    def test_shipped_lists_are_valid_and_playable_for_every_difficulty(self):
        directory = Path(__file__).resolve().parents[1] / "words"
        manager = WordManager(directory)
        for difficulty in WordManager.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                words = (directory / f"{difficulty}.txt").read_text(encoding="utf-8").splitlines()
                self.assertTrue(words)
                self.assertEqual(len(words), len(set(words)))
                for word in words:
                    self.assertRegex(word, r"^[a-z]+$")
                    game = HangmanGame(word)
                    for letter in dict.fromkeys(word):
                        game.guess(letter)
                    self.assertEqual(game.status, "won")
                self.assertIn(manager.choose_word(difficulty), words)

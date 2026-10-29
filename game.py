"""Hangman rules, independent of HTTP and user interfaces."""

import re


class InvalidGuessError(ValueError):
    """A guess is malformed or has already been used."""


class GameFinishedError(ValueError):
    """A finished game cannot accept another guess."""


class HangmanGame:
    """One game; callers supply a word selected by the word manager."""

    MAX_INCORRECT = 6

    def __init__(self, word: str):
        if not isinstance(word, str) or not re.fullmatch(r"[a-zA-Z]+", word):
            raise ValueError("Word must contain only ASCII letters.")
        self._word = word.lower()
        self._guessed = []
        self._incorrect = []

    @property
    def status(self) -> str:
        if len(self._incorrect) == self.MAX_INCORRECT:
            return "lost"
        if all(letter in self._guessed for letter in self._word):
            return "won"
        return "playing"

    def guess(self, letter: str) -> dict:
        """Accept a new letter or raise without changing the game."""
        if self.status != "playing":
            raise GameFinishedError("This game has ended. Start a new game.")
        if not isinstance(letter, str) or not re.fullmatch(r"[a-zA-Z]", letter):
            raise InvalidGuessError("Guess one ASCII letter (A-Z).")
        letter = letter.lower()
        if letter in self._guessed:
            raise InvalidGuessError("That letter has already been guessed.")
        self._guessed.append(letter)
        if letter not in self._word:
            self._incorrect.append(letter)
        return self.to_state()

    def to_state(self) -> dict:
        """Return a fresh public snapshot; never expose an active answer."""
        state = {
            "pattern": " ".join(
                letter if letter in self._guessed else "_" for letter in self._word
            ),
            "guessed_letters": list(self._guessed),
            "incorrect_letters": list(self._incorrect),
            "remaining_guesses": self.MAX_INCORRECT - len(self._incorrect),
            "status": self.status,
        }
        if state["status"] != "playing":
            state["word"] = self._word
        return state

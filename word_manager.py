"""Load validated server-side word lists and select words by difficulty."""

from pathlib import Path
import random
import re


class WordListError(ValueError):
    """A required word list is missing, unreadable, empty, or invalid."""


class WordManager:
    DIFFICULTIES = ("easy", "medium", "hard")

    def __init__(self, words_dir=None):
        directory = Path(words_dir) if words_dir is not None else Path(__file__).parent / "words"
        self._words = {}
        for difficulty in self.DIFFICULTIES:
            path = directory / f"{difficulty}.txt"
            try:
                lines = path.read_text(encoding="utf-8-sig").splitlines()
            except (OSError, UnicodeError) as exc:
                raise WordListError(f"Cannot read required word list: {path}") from exc
            words = []
            seen = set()
            for number, line in enumerate(lines, start=1):
                word = line.strip()
                if not word:
                    continue
                if not re.fullmatch(r"[a-zA-Z]+", word):
                    raise WordListError(f"Invalid word in {path}, line {number}: use ASCII letters only.")
                word = word.lower()
                if word not in seen:
                    words.append(word)
                    seen.add(word)
            if not words:
                raise WordListError(f"Required word list is empty: {path}")
            self._words[difficulty] = tuple(words)

    def choose_word(self, difficulty: str) -> str:
        """Choose randomly from the requested list; never silently fall back."""
        if not isinstance(difficulty, str) or difficulty not in self.DIFFICULTIES:
            raise ValueError("Difficulty must be easy, medium, or hard.")
        return random.choice(self._words[difficulty])

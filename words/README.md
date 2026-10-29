# Required game resources

`easy.txt`, `medium.txt`, and `hard.txt` each contain five words supplied by the
student in chat on October 28, 2026. These are the project's initial playable
lists, not the instructor's original lists. Difficulty reflects familiarity
as well as spelling; word length alone does not determine difficulty.

The loader trims whitespace, lowercases entries, skips blank lines, removes
duplicates, and rejects invalid or empty lists. Lists are intentionally small
and words may recur across games. Categories are not implemented: the current
assignment uses Easy, Medium, and Hard. Unit tests also generate separate
synthetic lists in temporary directories; those are test data only.

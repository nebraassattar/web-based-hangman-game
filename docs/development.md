# Development evidence

## Phase 1 — October 28, 2026

Prompt: “Okay let's start phase 1”. The earlier planning request required
original, understandable Python code and prohibited copying the instructor's
completed implementation.

Implemented an independent engine in `game.py`, a file-based word manager in
`word_manager.py`, and standard-library `unittest` tests. No Flask or UI code
has been added. Phase 1 requires no package installation. The real instructor
lists remain missing; `words/README.md` explains the outstanding resources.

The engine stores the word and guess history privately, calculates status from
those values, and creates a public snapshot. Correct letters expose every
matching position. Six misses cause a loss. Duplicate, malformed, and post-game
guesses raise errors before mutation. Snapshot lists are copied so changing a
returned response cannot change the game. Only final snapshots include `word`.

Word loading is separate so tests can supply synthetic lists. The loader reads
all three difficulties at initialization, accepts UTF-8 with an optional BOM,
trims whitespace, validates ASCII letters before lowercasing, removes duplicates,
and rejects missing, unreadable, invalid, or empty resources. Validating before
lowercasing prevents Unicode characters such as the Kelvin sign from becoming
an accepted ASCII letter. Random choice uses Python's standard library.

Verification command: `python -m unittest discover -s tests -v`.
Result: 17 tests passed on Python 3.11.5. Tests cover masking/repeated positions,
case normalization, life counting, invalid input, duplicate guesses, wins/losses,
post-game immutability, isolated games, snapshot isolation, all difficulties,
normalization/deduplication, selection pool, and list failures. Synthetic words
are created in temporary directories and are not production/instructor lists.

Initial remaining work was to obtain word lists and validate their contents.
The student subsequently supplied five example words for each difficulty in chat.
These have been added as the initial project lists with explicit student
provenance, completing Phase 1 without claiming instructor resources are present.
Category-based lists were suggested as an alternative and remain deferred.

Final verification: the same unittest command passes 18 tests. The additional
resource test validates the shipped lists, checks selection stays within each
difficulty, and plays every word to a win. The lists have five unique lowercase
ASCII entries each. Their small size means repeat selections are possible.
No Phase 2 work has started. The student should review the implementation and
explain guess → validation → state change → safe snapshot before proceeding.

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

## GitHub synchronization and Phase 2 — October 28, 2026

Prompt: “cool let's push everything to github then continue”. Network access
required an elevated execution because sandbox DNS resolution failed. Fetched
GitHub's initial `main` commit, preserved its UTF-16 README as
`docs/reference/github-initial-README.md`, and merged both unrelated histories.
The working README remained the detailed project README. Renamed the local
branch to `main` and pushed without force, preserving the original remote commit.

Implemented `server.py` with an application factory, one in-memory game store
per application, UUID game IDs, all three required routes, strict JSON field
validation, and consistent errors. A process-local lock protects state changes
and snapshots from concurrent requests. Each API response uses the engine's
safe serializer with game ID and difficulty added. Active answers are omitted;
ended games disclose the answer. API responses use `Cache-Control: no-store`.
Malformed and invalid input returns 400, unknown games 404, post-game guesses
409, and non-JSON POSTs 415. Framework routing errors are also JSON while
retaining HTTP headers such as Allow. Unknown game IDs take precedence over
body validation on the guess route.

Request flow: Flask parses and validates JSON, locates the game, passes a letter
to the engine, and serializes the resulting public snapshot. Flask does not
duplicate the engine's rules. Phase 3 will render that JSON in the browser.

Created a project-local virtual environment instead of changing the existing
global Flask 2.0.2 installation. Installed Flask 3.1.3 and its dependencies from
`requirements.txt`. Tests use Flask's test client and standard-library unittest;
fixed words are injected only in tests, never accepted through the public API.
Reference: https://flask.palletsprojects.com/en/stable/testing/

Verification: `.venv/Scripts/python.exe -m unittest discover -s tests -v` passes
27 tests (18 engine/resource tests plus 9 API tests). API checks include all
difficulties, full win/loss/restart flows, repeated and malformed input,
unsupported content types, separate games/applications, routing errors, and
answer disclosure on create/get/guess. `pip check` reports no broken requirements.
A temporary real local HTTP server passed POST-create, GET-state, and POST-guess
checks and was shut down afterward. `git diff --check` passed.

Known limits: browser and deployment pending; `/` returns JSON 404 for now.
In-memory games vanish on restart, are not shared between processes, and have
no automatic expiry. Phase 2 is complete; Phase 3 has not started.

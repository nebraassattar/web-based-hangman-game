# Web-Based Hangman

An individual assignment to build an original Python/Flask server and an
HTML/CSS/JavaScript browser client, then deploy it to a public HTTPS URL.

**Current status: Phase 1 partially complete.** The independent engine and word
loader are implemented and tested. Instructor word lists are still missing.
There is no Flask server, browser interface, or deployed URL yet.

## Documents and authority

- [Reduced specification](SPECIFICATION.md): assignment scope and planned contract.
- [Phased roadmap](TODO.md): unchecked work and verification criteria.
- [Original specification](docs/reference/Specification.md) and
  [original instructor TODO](docs/reference/TODO.md): preserved unchanged.
- [Reference provenance](docs/reference/README.md): sources and availability.

The assignment requirements supplied in chat override the larger reference
specification. The instructor transcript guides incremental development and
debugging; it is not a source of completed code to copy. Original implementation
and the ability to explain every component are part of the assignment.

## Planned architecture

The browser submits difficulty and letters using same-origin `fetch()` requests.
Flask validates JSON, locates an isolated game by ID, invokes the independent
Python engine, and returns safe public state. JavaScript renders that response.
The engine owns rules, guesses, six incorrect guesses, masking, and outcomes;
word management loads and randomly selects server-side words by difficulty.
The hidden word appears in responses only after a win or loss.

Architecture (engine, loader, tests, and resource instructions now exist;
server and browser files are planned for later phases):

```text
game.py                 Independent game engine
word_manager.py         Word loading and random selection
server.py               Flask application, routes, in-memory games
templates/index.html    Browser page
static/style.css        Responsive presentation
static/app.js           API requests, controls, and drawing
words/{easy,medium,hard}.txt
tests/                  Engine, word-management, and API tests
requirements.txt        Phase 1 needs only the Python standard library
```

Required routes are `POST /api/games`, `GET /api/games/{game_id}`, and
`POST /api/games/{game_id}/guess`. See the specification for fields and errors.
Flask will also serve `/`. In-memory storage requires one production worker;
restarts clear games. Deployment configuration will be verified in Phase 5.

## Phased workflow

1. Project setup, independent engine, word management, and unit tests.
2. Flask REST API and API tests.
3. Responsive browser interface with clickable letters, keyboard input, drawing, and restart.
4. Integration checks, accessibility, browser verification, and debugging.
5. Deployment preparation and public deployment verification.
6. PDF development report and demonstration/submission checklist.

Work on one phase at a time. Review and explain the code, run relevant checks,
record evidence, update TODO only after verification, and commit each phase.
Later documentation will provide tested installation, local run, test, and
deployment commands. Chrome Developer Tools inspection of a request and JSON
response is required for learning and the demonstration.

## Missing resources

`words/easy.txt`, `words/medium.txt`, and `words/hard.txt` are currently missing.
No word lists were found in the supplied reference folder either. The transcript
describes the instructor's historical files, which are not present here. Obtain
and verify those resources before claiming the instructor lists are installed.

## Phase 1 setup and tests

Use Python 3.10 or newer. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

No third-party packages are needed for this phase. Alternatively, run
`python -m unittest discover -s tests -v` using your existing Python installation.
Verified on Python 3.11.5: 17 tests pass. Tests create temporary synthetic word
lists and do not establish that the instructor's resources are available.

`HangmanGame(word)` accepts a server-selected word. `guess(letter)` validates
and updates it, and `to_state()` returns a fresh safe snapshot. Invalid or
duplicate guesses raise `InvalidGuessError`; ended games raise
`GameFinishedError`. Neither changes the state. The API will add game IDs and
difficulty to these snapshots in Phase 2.

`WordManager()` loads the three expected files relative to the module, or accepts
an explicit directory for tests. `choose_word("easy")` selects randomly from
that difficulty's validated list. Missing resources raise `WordListError`;
there is no fallback list. See [development notes](docs/development.md).

## Repository and delivery

Intended origin: https://github.com/nebraassattar/web-based-hangman-game.git

Initial inspection found an empty local repository on `master`, no commits,
and no remote. The planning setup adds the requested origin without replacing
content or rewriting history. A remote-ref query failed because network name
resolution was unavailable, so remote contents/history are not yet verified.
No push or deployment is part of this planning step. Inspect/fetch remote history
before the first push; reconcile any existing work without force-pushing.

Final delivery through HuskyCT includes the GitHub URL, public HTTPS application
URL, a 1–2 page PDF report, and an approximately 2–3 minute recording. Record
process, tests, deployment evidence, a challenge/fix, reflection, and representative
prompts as development proceeds. Keep credentials out of the repository.

Terminal clients, bots, evaluations, leaderboards, and replay are out of scope.

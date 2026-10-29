# Web-Based Hangman

An individual assignment to build an original Python/Flask server and an
HTML/CSS/JavaScript browser client, then deploy it to a public HTTPS URL.

**Play online: https://web-based-hangman-game.onrender.com**

**Current status: Phases 1–5 complete.** The independent engine, word loader,
student-supplied lists, Flask REST API, and responsive browser interface are
implemented and tested. Integration and targeted accessibility checks are
recorded in [testing evidence](docs/testing.md). Public Render deployment and
HTTPS verification passed. The report and demonstration remain in Phase 6.

## Submission materials

- [Two-page development report](output/pdf/hangman-development-report.pdf).
- [Editable report source](docs/submission/development_report.md).
- [Timed demonstration script and hand-in checklist](docs/submission/demonstration.md).

The report includes the student's supplied reflection. Review it before submitting. The
approximately 2-3 minute screen recording and HuskyCT submission still need to
be completed. The script includes the public URL, a full game, restart, and a
Chrome Developer Tools request/JSON response. No recording is included yet.

To regenerate the PDF after editing its Markdown source, install `reportlab`
in a document-authoring environment and run `python docs/submission/build_report.py`.
Report tooling is separate from the Flask runtime dependencies. Confirm the
regenerated report remains 1-2 pages and visually review it before submission.

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

Current architecture:

```text
game.py                 Independent game engine
word_manager.py         Word loading and random selection
server.py               Flask application, routes, in-memory games
templates/index.html    Browser page
static/style.css        Responsive presentation
static/app.js           API requests, controls, and drawing
words/{easy,medium,hard}.txt
tests/                  Engine, word-management, and API tests
requirements.txt        Flask dependency; unittest is part of Python
```

Required routes are `POST /api/games`, `GET /api/games/{game_id}`, and
`POST /api/games/{game_id}/guess`. See the specification for fields and errors.
Flask serves the browser at `/`. In-memory storage requires one production worker;
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

## Word resources

`words/easy.txt`, `words/medium.txt`, and `words/hard.txt` each contain five words
supplied by the student in chat. The instructor's original lists remain
unavailable. These small initial lists support all three difficulties but may
repeat words across games. See [provenance](words/README.md). Difficulty uses
familiarity and spelling, rather than word length alone; categories are deferred.

## Local setup, API, and tests

Use Python 3.10 or newer. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe server.py
```

Open `http://127.0.0.1:5000` in your browser. Choose a difficulty, click Start
game, then click letters or type them on your keyboard. A wrong guess adds a
body part; after six misses the game ends. New game starts again without a
reload. The browser displays outcomes from Flask and never receives an active
answer. Stop the server with Ctrl+C. Debug mode is off.

Use a separate PowerShell window to try the API:

```powershell
$game = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/games -ContentType application/json -Body '{"difficulty":"easy"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/games/$($game.game_id)"
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/games/$($game.game_id)/guess" -ContentType application/json -Body '{"letter":"e"}'
```

Verified with Python 3.11.5 and Flask 3.1.3: 29 tests pass. Tests cover the
engine, synthetic and shipped lists, API flows, and page/asset serving. Live
browser verification covered all difficulties, mouse/keyboard input, a complete
win/loss, restart, outage/stale-game recovery, and desktop/mobile layouts.
See `docs/testing.md` for fixes, contrast measurements, DevTools evidence,
and limits such as unverified screen-reader speech.

The client uses plain JavaScript, with no build step. Pending requests disable
submissions; network failures trigger a state refresh before further play.
There is no saved-game restoration after a page reload. Optional Google Fonts
enhance typography; system fonts work when the font service is unavailable.

`HangmanGame(word)` accepts a server-selected word. `guess(letter)` validates
and updates it, and `to_state()` returns a fresh safe snapshot. Invalid or
duplicate guesses raise `InvalidGuessError`; ended games raise
`GameFinishedError`. Neither changes the state. The API adds game IDs and
difficulty to these snapshots.

`WordManager()` loads the three expected files relative to the module, or accepts
an explicit directory for tests. `choose_word("easy")` selects randomly from
that difficulty's validated list. Missing resources raise `WordListError`;
there is no fallback list. See [development notes](docs/development.md).

## Repository and delivery

Intended origin: https://github.com/nebraassattar/web-based-hangman-game.git

The initial local `master` history was merged with GitHub's initial `main`
commit without rewriting either history. The local branch is now `main` and
tracks `origin/main`. The remote's initial README is preserved byte-for-byte
in `docs/reference/github-initial-README.md` as well as in Git history.

Games are held in one process and operations use a lock to avoid overlapping
updates. Restarting clears games; multiple workers would not share them. There
is no persistence or game cleanup yet, so memory use grows with created games.
`render.yaml` configures a free Render Python service, runs tests during build,
and starts Gunicorn with one worker and four threads. See
[deployment instructions and verification record](docs/deployment.md).
The configuration has passed local Linux production-server smoke checks.
The public HTTPS service has passed the same HTTP smoke check and a complete
browser game/restart with no local server running. Free hosting sleeps when
idle; allow it to wake before starting a game or demonstrating it. Memory-only
games are lost when it restarts. Recheck availability before grading.

Final delivery through HuskyCT includes the GitHub URL, public HTTPS application
URL, a 1–2 page PDF report, and an approximately 2–3 minute recording. Record
process, tests, deployment evidence, a challenge/fix, reflection, and representative
prompts as development proceeds. Keep credentials out of the repository.

Terminal clients, bots, evaluations, leaderboards, and replay are out of scope.

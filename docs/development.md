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

## Phase 3 — October 28, 2026

Prompt: “Cool let's move on”. Built an original paper-and-ink interface in
`templates/index.html`, `static/style.css`, and `static/app.js`, served at `/`.
Used the Sites skill's local-only preview workflow with the existing Flask
checkout; cloud hosting remains scheduled for Phase 5.

The client sends difficulty or a letter through `fetch()`, then renders only
the server response. It has no word lists, word selection, or independent
win/loss logic. Six SVG body parts reflect the incorrect-letter count. A
shared request wrapper disables controls while pending, applies a timeout,
and attempts GET-state recovery if a response fails. If recovery fails, it
requires a new game rather than inventing local state. Error messages use
an alert region; outcomes use a live status region. Keys are real buttons,
used letters show correct/incorrect text labels, and shortcuts/form input are
excluded from physical keyboard guessing.

Validation: 28 Python tests pass, including page and static asset serving;
`node --check static/app.js` and `git diff --check` pass. In the live browser,
verified six misses caused loss and answer disclosure, then restarted without
reloading. Won MONKEY with a physical M key and clickable remaining letters.
Started Easy, Medium, and Hard games; checked disabled used keys and pending
controls. Verified six-part drawing progression and life indicators.

Inspected the default narrow layout and desktop at 1280×900. A 320px viewport
revealed clipped settings controls; stacked the difficulty label and reduced
word-slot sizing, then visually rechecked. Document width matched the viewport
without horizontal overflow. SVG visibility uses the hidden attribute, which
is explicitly handled in CSS. Temporary viewport overrides were reset.

Known limits: no reload persistence; five words per difficulty; optional Google
Fonts require network access with system-font fallbacks. Full keyboard/focus,
contrast, assistive-technology, network-error, unknown-game, and Chrome DevTools
request/response inspection belong to Phase 4 and are not claimed complete.

## Phase 4 — October 29, 2026

Prompt: “let's push it and move on”. Confirmed Phase 3 was already on GitHub
(`git push` returned “Everything up-to-date”), then completed the next phase.

Found and fixed focus loss during pending requests, stale word display when
state recovery fails, and weak disabled-letter contrast. Added a concurrent
duplicate-guess regression test. All 29 tests pass, as do dependency and
JavaScript syntax checks. Verified Chrome mouse/keyboard wins/losses, restart,
all difficulties, repeated/invalid keyboard input, server-outage feedback,
stale-game 404 recovery, desktop/mobile layouts, and focus placement.

Inspected a real guess payload and active-game response in Chrome Developer
Tools: a letter was sent and the updated JSON omitted the hidden answer.
Recorded the browser/Flask/engine/JSON sequence and selected color contrast
measurements. Full evidence, reproduction instructions, and remaining limits
are in `docs/testing.md`. Screen-reader speech and cross-browser certification
are not claimed. Phase 5 (deployment) has not started.

## Phase 5 preparation — October 29, 2026

Prompt: “okay cool let's do it”. Added `render.yaml`, a tracked `.python-version`
for Python 3.11, and Gunicorn as a Linux-only dependency while pinning Flask to
the verified 3.1.3 release. The build runs tests; production uses `server:app`,
the Render PORT, one worker, and four threads. Documented free-service idle
behavior, memory reset/scaling limits, setup steps, and cloud verification.

Fresh Ubuntu Python 3.12.3 installation passed 29 tests and dependency checks.
The repeatable HTTP smoke script passed against actual local Gunicorn 23.0.0,
including all difficulties, complete games, restart, validation, and hidden-word
protection. Gunicorn cannot run natively on Windows; testing under Ubuntu avoids
claiming that Flask's development server proves the production command works.
Windows Python 3.11.5 still passes all 29 tests with the platform marker skipping
Gunicorn. See `docs/deployment.md` for commands and verification limits.

Discovered an available Render integration and offered it for connection. The
browser dashboard requires sign-in. Public deployment remains pending account
access; no service or deployed URL is claimed. Phase 6 has not started.

### Phase 5 deployment completed

The student confirmed Render was connected and authorized the Free plan in
“My Workspace”. Created `web-based-hangman-game` in Virginia using the GitHub
main branch. Render's first build passed 29 tests on Python 3.11.18 and became
live at https://web-based-hangman-game.onrender.com.

Public HTTPS smoke checks passed for all three API routes and difficulties,
validation, complete games, final disclosure, active-answer omission, and restart.
Played a complete loss and restarted Medium/Hard games in Chrome with the local
server stopped. Recorded service/deploy identifiers, commands, and evidence in
`docs/deployment.md`. Updated the Blueprint region to match the actual service.
Documented free idle shutdown and the need to recheck near grading. Phase 5 is
complete; the report and recording remain Phase 6 work.

Follow-up: GitHub documentation commit `7182e41` was pushed, but Render still
reported only the initial live deployment during final checks despite its
auto-deploy setting. Runtime source is unchanged; current public gameplay is
verified. Future automatic deploys need repository-integration verification.
This limitation is recorded rather than claiming the documentation push was
deployed or triggering a duplicate deploy with auto-deploy enabled.

## Phase 6 preparation — October 29, 2026

Prompt: “let's do it”. Prepared a two-page PDF development report, editable
Markdown source, a ReportLab regeneration script, and an approximately
2 minute 40 second demonstration plan with submission checklist. The report
covers the observed process, original architecture, testing, deployment,
focus/recovery fixes, three actual prompts, and a reflection draft for the
student to review. It does not invent personal learning or claim student review.

Rendered both PDF pages with Poppler and inspected their layout after revising
page breaks and prompt spacing. Verified the final PDF has exactly two pages.
Rechecked the repository contents and GitHub remote, ran all 29 tests, and
repeated the public HTTPS smoke checks successfully. The Render service remained
unsuspended. ReportLab is document tooling, not a deployed runtime dependency.

Outstanding student work: review/personalize the report, practice explaining
the implementation, record and review a narrated screen demonstration including
Chrome Network details, recheck grading availability, and submit through HuskyCT.
Phase 6 remains partially complete; no video or submission is claimed.

### Personal reflection update

The student supplied their reflection describing phased work, AI assistance,
personal review/testing, server authority, browser-discovered bugs, and word
selection. Incorporated it into the report, removed the bracketed prompt to add
more detail, and corrected the word provenance to examples supplied in chat
rather than the assignment handout. Removed reflection-draft labels and updated
the PDF and submission guidance. Final student review, recording, and hand-in
remain outstanding.

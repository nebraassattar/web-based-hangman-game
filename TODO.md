# Assignment Roadmap

Phases 1–5 are complete. Phase 6 report and demonstration guidance are prepared;
student review, recording, and HuskyCT submission remain.
Follow `SPECIFICATION.md`, with the assignment requirements taking precedence.
Finish and verify one phase before proceeding; update checkboxes only after
verification and commit each completed phase. Record meaningful prompts,
decisions, failures, fixes, and evidence for the report. Write original code
and review it until you can explain it.

## Phase 1: Project setup, game engine, word management, and unit tests

- [x] Confirm word-list provenance: use the student's supplied examples as the initial lists; instructor originals remain unavailable.
- [x] Create the planned Python, resource, and test structure and dependency setup.
- [x] Add and validate `words/easy.txt`, `words/medium.txt`, and `words/hard.txt`; document provenance.
- [x] Implement independent word loading, normalization, deduplication, validation, and random selection by difficulty.
- [x] Implement independent Python game state, guess validation, masking, guessed/incorrect letters, and six incorrect guesses.
- [x] Implement win/loss detection, duplicate rejection, post-game rejection, and safe state serialization.
- [x] Add unit tests for game rules, all difficulties, word loading failures, and answer disclosure.
- [x] Run unit tests and review/explain the engine; record results and commit the verified implementation progress.

Verification: Python 3.11.5, `python -m unittest discover -s tests -v` —
18 tests passed, including verification of the shipped lists. See `docs/development.md`.

Completion: engine and word manager work under tests without Flask or a browser.

## Phase 2: Flask REST API and API tests

- [x] Configure Flask and isolated in-memory game storage with unique IDs.
- [x] Implement `POST /api/games` and validate difficulty input.
- [x] Implement `GET /api/games/{game_id}` with safe public state.
- [x] Implement `POST /api/games/{game_id}/guess` and server-authoritative updates.
- [x] Implement consistent JSON errors and documented 400/404/409/415 status behavior.
- [x] Test malformed/missing/extra fields, invalid and duplicate guesses, unknown games, and ended games.
- [x] Test full wins/losses, separate game states, and answer omission on every active-game response.
- [x] Run engine/API tests, explain the request flow, record results, and commit the verified phase.

Verification: 27 tests passed in the project virtual environment, plus a live
local HTTP create/get/guess smoke check and a successful dependency check.

Completion: required API supports a complete game without the browser.

## Phase 3: Browser interface

- [x] Serve an HTML/CSS/JavaScript interface from Flask.
- [x] Add Easy/Medium/Hard selection and start/new-game controls using `fetch()`.
- [x] Render server-provided pattern, guessed/incorrect letters, lives, and outcome.
- [x] Add clickable alphabet buttons and physical keyboard handling.
- [x] Disable used letters, pending submissions, and guesses after game completion.
- [x] Draw six progressive Hangman parts from server-reported incorrect guesses.
- [x] Implement win/loss answer display and restart without page reload.
- [x] Add responsive layout, semantic controls, focus styles, and loading/error feedback.
- [x] Verify a browser game, review the client for hidden-word leakage, and commit the verified phase.

Verification: 28 tests passed, JavaScript syntax check passed, and live browser
checks covered mouse/keyboard play, all difficulties, win/loss, restart, and
responsive layouts. Broader accessibility/failure checks remain in Phase 4.

Completion: browser can play and restart using only API results for game decisions.

## Phase 4: Integration testing, accessibility, and debugging

- [x] Run all engine/API tests and resolve regressions.
- [x] Manually test all difficulties, correct/incorrect/repeated/invalid input, win, six-miss loss, and restart.
- [x] Verify mouse/keyboard input, progressive drawing, pending requests, network failures, and unknown-game recovery.
- [x] Verify desktop/mobile layouts, keyboard-only navigation, focus, contrast, status-announcement semantics, and drawing text alternatives (screen-reader speech remains unverified).
- [x] Inspect at least one guess request/JSON response in Chrome Developer Tools and confirm the hidden word is absent during play.
- [x] Explain and record the browser → HTTP → Flask → engine → JSON → browser update sequence.
- [x] Record test evidence, bugs/fixes, and known limitations; commit the verified phase.

Verification: 29 tests pass. Chrome gameplay, outage/restart recovery, responsive
layouts, focus, selected color contrast, and DevTools payload/response checks
are recorded in `docs/testing.md`, including explicit verification limits.

Completion: integrated behavior and accessibility checks have recorded evidence.

## Phase 5: Deployment preparation and deployment verification

- [x] Finalize dependencies and production configuration for Render or another suitable Python host.
- [x] Configure a WSGI entry point, environment port binding, one worker for in-memory games, and debug disabled.
- [x] Document game loss on restart and one-process storage limitations.
- [x] Confirm secrets are excluded and a fresh local installation works from README instructions.
- [x] Push verified work to the intended GitHub repository while preserving history.
- [x] Deploy and record the actual public HTTPS URL and configuration.
- [x] Verify public UI and all three API endpoints independently of the local development server.
- [x] Play a complete deployed game and restart; verify all difficulties and no active-answer leakage.
- [x] Record evidence and availability steps for grading; commit configuration and documentation updates (recheck availability in Phase 6).

Verified October 29, 2026: https://web-based-hangman-game.onrender.com.
Render build passed 29 tests; public HTTP smoke checks and a complete Chrome
game/restart passed with the local server stopped. See `docs/deployment.md`.

Completion: the public HTTPS application supports complete games without local setup.

## Phase 6: Submission report and demonstration checklist

- [x] Finish README setup/run/test/deployment instructions and known limitations.
- [x] Verify repository includes original specification, reduced specification, updated TODO, word lists, code, tests, dependencies, and deployment configuration.
- [x] Prepare a 1–2 page PDF covering process, implementation, testing, deployment, challenge/resolution, and reflection (draft for student review).
- [x] Include two or three representative prompts and explain the original implementation.
- [x] Incorporate the student's personal reflection and remove its placeholder.
- [ ] Review/personalize reflection, confirm understanding, and approve the final report before submitting.
- [ ] Record an approximately 2–3 minute demonstration of the deployed page, game start, guesses, a win/loss, and restart.
- [ ] Show a Chrome Developer Tools HTTP request and JSON response in the recording.
- [ ] Recheck repository/public URLs, report, recording, and grading availability; submit through HuskyCT.

Prepared `output/pdf/hangman-development-report.pdf` (two pages, rendered and
visually verified), editable source and regeneration script under
`docs/submission/`, and a timed demonstration/hand-in checklist. All 29 tests
and the public HTTPS smoke check passed again October 29, 2026. No video or
HuskyCT submission has been created or claimed.

Completion: all assignment deliverables are verified and ready for submission.

## Out of scope

Terminal clients, bots, evaluations, leaderboards, competitive scoring, and replay
features are excluded. Do not implement the larger reference roadmap's extensions.

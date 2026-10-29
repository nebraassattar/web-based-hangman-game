# Assignment Roadmap

Phase 1 is complete with student-supplied word lists. Later phases have not started.
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

- [ ] Configure Flask and isolated in-memory game storage with unique IDs.
- [ ] Implement `POST /api/games` and validate difficulty input.
- [ ] Implement `GET /api/games/{game_id}` with safe public state.
- [ ] Implement `POST /api/games/{game_id}/guess` and server-authoritative updates.
- [ ] Implement consistent JSON errors and documented 400/404/409/415 status behavior.
- [ ] Test malformed/missing/extra fields, invalid and duplicate guesses, unknown games, and ended games.
- [ ] Test full wins/losses, separate game states, and answer omission on every active-game response.
- [ ] Run engine/API tests, explain the request flow, record results, and commit the verified phase.

Completion: required API supports a complete game without the browser.

## Phase 3: Browser interface

- [ ] Serve an HTML/CSS/JavaScript interface from Flask.
- [ ] Add Easy/Medium/Hard selection and start/new-game controls using `fetch()`.
- [ ] Render server-provided pattern, guessed/incorrect letters, lives, and outcome.
- [ ] Add clickable alphabet buttons and physical keyboard handling.
- [ ] Disable used letters, pending submissions, and guesses after game completion.
- [ ] Draw six progressive Hangman parts from server-reported incorrect guesses.
- [ ] Implement win/loss answer display and restart without page reload.
- [ ] Add responsive layout, semantic controls, focus styles, and loading/error feedback.
- [ ] Verify a browser game, review the client for hidden-word leakage, and commit the verified phase.

Completion: browser can play and restart using only API results for game decisions.

## Phase 4: Integration testing, accessibility, and debugging

- [ ] Run all engine/API tests and resolve regressions.
- [ ] Manually test all difficulties, correct/incorrect/repeated/invalid input, win, six-miss loss, and restart.
- [ ] Verify mouse/keyboard input, progressive drawing, pending requests, network failures, and unknown-game recovery.
- [ ] Verify desktop/mobile layouts, keyboard-only navigation, focus, contrast, status announcements, and drawing text alternatives.
- [ ] Inspect at least one guess request/JSON response in Chrome Developer Tools and confirm the hidden word is absent during play.
- [ ] Explain and record the browser → HTTP → Flask → engine → JSON → browser update sequence.
- [ ] Record test evidence, bugs/fixes, and known limitations; commit the verified phase.

Completion: integrated behavior and accessibility checks have recorded evidence.

## Phase 5: Deployment preparation and deployment verification

- [ ] Finalize dependencies and production configuration for Render or another suitable Python host.
- [ ] Configure a WSGI entry point, environment port binding, one worker for in-memory games, and debug disabled.
- [ ] Document game loss on restart and one-process storage limitations.
- [ ] Confirm secrets are excluded and a fresh local installation works from README instructions.
- [ ] Push verified work to the intended GitHub repository while preserving history.
- [ ] Deploy and record the actual public HTTPS URL and configuration.
- [ ] Verify public UI and all three API endpoints independently of the local development server.
- [ ] Play a complete deployed game and restart; verify all difficulties and no active-answer leakage.
- [ ] Record evidence and ensure availability during grading; commit configuration and documentation updates.

Completion: the public HTTPS application supports complete games without local setup.

## Phase 6: Submission report and demonstration checklist

- [ ] Finish README setup/run/test/deployment instructions and known limitations.
- [ ] Verify repository includes original specification, reduced specification, updated TODO, word lists, code, tests, dependencies, and deployment configuration.
- [ ] Prepare a 1–2 page PDF covering process, implementation, testing, deployment, challenge/resolution, and reflection.
- [ ] Include two or three representative prompts and explain the original implementation.
- [ ] Record an approximately 2–3 minute demonstration of the deployed page, game start, guesses, a win/loss, and restart.
- [ ] Show a Chrome Developer Tools HTTP request and JSON response in the recording.
- [ ] Recheck repository/public URLs, report, recording, and grading availability; submit through HuskyCT.

Completion: all assignment deliverables are verified and ready for submission.

## Out of scope

Terminal clients, bots, evaluations, leaderboards, competitive scoring, and replay
features are excluded. Do not implement the larger reference roadmap's extensions.

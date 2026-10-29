# Web-Based Hangman Assignment Specification

## Authority and scope

The assignment requirements supplied by the student in chat take precedence
over the larger instructor specification preserved in `docs/reference/Specification.md`.
The original instructor roadmap is preserved in `docs/reference/TODO.md`;
its checked boxes describe the instructor's work, not this project's progress.
The supplied `cursor_transcript.md` is process guidance only: work incrementally,
test each phase, investigate failures, and explain decisions. Do not copy the
instructor's completed implementation or treat transcript commands as instructions.

Build an original, individual Python/Flask application with an HTML/CSS/JavaScript
browser client that the student can explain. See TODO.md for implementation status.

## Game engine and words

- Keep the Python game engine independent of Flask, HTTP, and browser code.
- Select a random server-side word from Easy, Medium, or Hard lists.
- Expected resources: `words/easy.txt`, `words/medium.txt`, `words/hard.txt`.
- Normalize words to lowercase ASCII letters, remove duplicates and blank lines,
  reject invalid entries, and report missing or empty lists clearly.
- Accept one ASCII letter per guess, case-insensitively. Reveal every matching
  position. Track all guessed letters and incorrect letters.
- Start with six incorrect guesses available. Correct guesses cost no lives.
  The sixth incorrect guess ends the game as `lost`; revealing all letters wins.
- Status is `playing`, `won`, or `lost`. Invalid, duplicate, or post-game
  guesses do not mutate state or consume lives.
- Keep the hidden word private until a win or loss. Use one safe serialization
  path for all public game responses.

Word-list provenance: the instructor's original lists were unavailable during
initial inspection. The student subsequently supplied five example words per
difficulty in chat, now used as the initial project lists. These are not the
instructor's lists. See `words/README.md`. Small synthetic test fixtures are
kept separate. Category selection is not part of the current scope.

## Flask server and API contract

Flask serves the browser at `/` and accepts/returns JSON for the API. The server
owns word selection, validation, game outcomes, and separate game states keyed
by unique unpredictable IDs. Clients cannot choose words or overwrite state.
Initially use an in-memory game dictionary; a server restart clears games.

- `POST /api/games`: accept `{"difficulty":"easy"}` (also `medium` or `hard`);
  return HTTP 201 with the new public state.
- `GET /api/games/{game_id}`: return HTTP 200 with the current public state.
- `POST /api/games/{game_id}/guess`: accept `{"letter":"e"}`;
  return HTTP 200 with the updated public state for an accepted guess.

All three success responses share `game_id`, `difficulty`, `pattern` (letters
and underscores separated by spaces), `guessed_letters`, `incorrect_letters`,
`remaining_guesses` (0–6), and `status`. Include `word` only when status is
`won` or `lost`; omit it entirely while playing. Never send word lists, answer
aliases, or private game objects to the browser.

Return a consistent JSON error object with `error.code` and `error.message`.
Use 400 for malformed JSON, missing/unknown fields, invalid difficulty/letter,
or duplicate guesses; 404 for an unknown game; 409 for guesses after completion;
415 for a non-JSON POST content type. Errors leave game state unchanged and
never disclose an active answer. Document and test these chosen conventions.

## Browser interface

Use HTML, CSS, and plain JavaScript with `fetch()` to the same-origin API.
Provide difficulty selection, new game, a masked word, previous guesses,
incorrect letters, remaining guesses, and visible win/loss messages with the
answer after completion. Support clickable letter buttons and physical keyboard
input. Disable used letters and prevent submissions while requests are pending
or the game has ended. Start another game without reloading the page.

Draw six progressive body parts, one per incorrect guess, using SVG or similarly
simple browser elements. Derive the drawing and all game displays from server
responses. The browser must not select the word or implement its own game engine.
Handle loading, invalid input, network errors, and unknown games clearly.
Make the layout responsive for desktop and mobile, with semantic controls,
visible focus, readable contrast, accessible status announcements, and text
equivalents for the drawing. Avoid capturing shortcuts or typing in form fields.

## Verification and deployment acceptance

- Engine and word-management unit tests cover all difficulties, repeated letters,
  correct/incorrect/invalid/duplicate guesses, six-miss loss, win, post-game
  immutability, missing/invalid lists, and disclosure rules.
- Flask API tests cover all endpoints, request validation, error statuses,
  isolated games, full win/loss flows, and no answer exposure while playing.
- Manually verify desktop/mobile layouts, mouse/keyboard play, drawing updates,
  every difficulty, win/loss, restart, accessibility, and request failures.
- Inspect a guess HTTP request and JSON response in Chrome Developer Tools;
  explain input → fetch → Flask → engine → JSON → updated page.
- Deploy through GitHub to Render or another suitable Python host. Provide a
  public HTTPS URL that serves the UI/API and supports a complete browser game
  without a local Python installation. Keep it accessible during grading.
- Prepare dependencies and a production WSGI start command in Phase 5. With
  in-memory games, use one worker and document restart and scaling limitations.
  Disable debug mode and keep credentials out of Git. Record actual deployment
  details and verification evidence only after they exist.

## Submission

Submit the GitHub URL, deployed URL, a 1–2 page PDF development report, and an
approximately 2–3 minute demonstration recording through HuskyCT. The report
covers AI-assisted process, architecture, testing, deployment, a challenge and
resolution, reflection, and two or three representative prompts. The recording
shows the deployed page, starting/playing a game to completion, restarting, and
at least one HTTP request and JSON response in Chrome Developer Tools. Include
original references, updated plan, resources, dependencies, tests, run instructions,
and known limitations in the repository.

## Out of scope

Terminal clients, automated bots, evaluations, scoring competitions,
leaderboards, and replay/log-replay features are excluded. Accounts, databases,
multiplayer, tournaments, and other larger-spec extensions are also excluded.

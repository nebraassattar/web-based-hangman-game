# Phase 4 verification — October 29, 2026

## Automated checks

Environment: Python 3.11.5, Flask 3.1.3, project `.venv`.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
node --check static/app.js
git diff --check
```

Result: 29 tests pass; dependency, JavaScript syntax, and whitespace checks pass.
The tests include engine rules, all resource files, complete API wins/losses,
restart, invalid JSON/fields/difficulty/letters, duplicates, unknown IDs,
post-game rejection, separate games, and active-answer omission. A new regression
test sends concurrent duplicate guesses through separate Flask clients: exactly
one succeeds, the other returns 400, and only one life is spent.

## Live Chrome verification

- Started games on Easy, Medium, and Hard; difficulty labels match the response.
- Started with Enter, guessed using keyboard and letter buttons, and observed
  pattern, lives, history, and SVG changes.
- Repeated Z and pressed 1: history stayed at Z and no additional life was spent.
- Won MONKEY using keyboard guesses; the final answer appeared and focus moved
  to New game. Remaining letter controls were disabled.
- Restarted without navigation and lost RAINBOW after Z, X, Q, V, J, D:
  six parts, zero chances, final answer displayed, and guesses disabled.
- Stopped the local server during a game, then guessed: an error alert appeared,
  the old pattern was cleared, guesses were disabled, and Start game was focused.
- Restarted the server while a second tab retained an old game. Its next guess
  received 404; the client displayed “This game is no longer available. Start
  a new game.” Creating a fresh game restored normal play.
- Inspected desktop at 1280×900 and mobile at 320×780. Mobile reflow is stacked;
  measured document width equalled the available 305px viewport (scrollbar
  excluded), with no horizontal overflow. Temporary viewport changes were reset.
- Pending controls are disabled during requests; no client-side word selection
  or independent outcome calculation exists. Failure recovery GETs authoritative
  state before permitting further guesses.

## Accessibility checks and fixes

Fixed focus loss caused by disabling the clicked button during a request.
After starting or guessing, focus moves to an available letter; when the game
ends or cannot be recovered, focus moves to the new-game button. Visible focus
outlines remain available for Tab navigation. Used-letter status has text labels
and is not conveyed by color alone. Difficulty has an associated label, the
page has a main landmark and heading, and the drawing has a text description.
Outcome updates use `role=status`, `aria-live=polite`, and `aria-atomic=true`;
failure messages use `role=alert`. These semantics were inspected in the browser.

Darkened disabled-letter text. Calculated sRGB contrast ratios for CSS colors:
body 12.47:1; muted text on card 5.00:1; primary button 6.79:1;
disabled letters 4.93:1; correct letters 7.08:1; incorrect letters 4.68:1;
focus outline against card 3.67:1. Text samples meet 4.5:1 and the focus outline
meets 3:1. This is a targeted check, not a full WCAG certification.

## Chrome Developer Tools evidence

Opened the Network panel, selected Fetch/XHR, created a game, and clicked E.
The guess appeared as a fetch request initiated by `static/app.js`. Status was
200 OK, and the Payload tab showed `{"letter":"e"}`. The Response tab showed:

```json
{
  "difficulty": "easy",
  "game_id": "aa3cbc6d5aee4746b8aba8c8153cce89",
  "guessed_letters": ["e"],
  "incorrect_letters": [],
  "pattern": "_ _ _ _ e",
  "remaining_guesses": 6,
  "status": "playing"
}
```

There was no `word` field. The page revealed E and disabled its letter button.
The game ID is a disposable local test identifier; restarting clears it.

To repeat for the demonstration:

1. Start Flask and open the application in Chrome.
2. Open Developer Tools (F12), choose Network, then Fetch/XHR.
3. Start a game and guess a letter; select the `guess` request.
4. Show its Headers (POST and status), Payload (one letter), and Response
   (updated safe state). Confirm no active answer, and point out the page update.

Explanation: a click/keydown calls JavaScript's guess handler; `fetch()` sends
JSON to Flask; Flask validates the body and finds the game; the engine updates
rules/state; Flask returns a safe JSON snapshot; JavaScript renders it. The
server alone decides correctness, remaining lives, and the outcome.

## Limits and remaining verification

No screen reader was run, so spoken announcement behavior is not claimed.
Actual touch devices, other browser engines, delayed-response/timeout fault
injection, and a full accessibility audit have not been tested. Error recovery
was exercised through a real server outage and restart. Chrome showed
`Baobab.Cursor.getters: invalid path` errors from a bundled script outside this
repository; these were observed separately from Hangman API behavior.
Chrome's automatic `/.well-known/appspecific/com.chrome.devtools.json` probe
returns 404 because no workspace-discovery endpoint is configured.

Known product limits remain: five words per difficulty, no reload restoration,
no game expiry, process-local storage, and optional external fonts with fallbacks.
Public HTTPS deployment and deployed-browser checks remain Phase 5 work.

# Render deployment

Public application: https://web-based-hangman-game.onrender.com

Dashboard: https://dashboard.render.com/web/srv-dbhcgfpsrm7s73ff6mdg

## Configuration

The root `render.yaml` defines a Python web service on the free instance plan,
building from `main`. The build installs dependencies and runs the Python tests;
a failed test prevents that build from proceeding. `.python-version` requests
the latest available Python 3.11 patch. Flask is pinned to the locally verified
release. Gunicorn is installed on Linux, not native Windows.

Build command:

```sh
pip install -r requirements.txt && python -m unittest discover -s tests -v
```

Start command:

```sh
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --access-logfile - --error-logfile - server:app
```

`server:app` imports the Flask application from `server.py`; it does not run
Flask's development server. Render supplies PORT. The process listens on all
interfaces. One worker keeps all games in a shared process; four threads can
handle requests, with the application's lock protecting game operations.
Debug mode is off. The Blueprint sets `/` as its health-check path; the service
created through the Render integration currently uses Render's default port
health check (the integration does not expose the HTTP health-check setting).
The public `/` page was also verified over HTTPS. No credentials or environment
secrets are required for this application.

## Create the service

Use the GitHub repository `nebraassattar/web-based-hangman-game`, branch `main`.
Create a Render Blueprint from this repository to use `render.yaml`, or create
a Python Web Service with the build/start commands above. Select Free and
confirm the final configuration before deploying. This app does not require a
database or paid disk. Record the actual assigned HTTPS URL only once returned
by Render; do not infer it from the service name.

## Verification after deployment

Run the repeatable HTTP check (creates disposable games on the supplied server):

```powershell
.\.venv\Scripts\python.exe tests/smoke_deployment.py https://YOUR-ACTUAL-SERVICE.onrender.com
```

The URL above is a placeholder, not a deployed address. The check validates UI
assets, all difficulties, full game completion, active-answer omission, invalid
guesses, post-game rejection, unknown IDs, and a fresh game after completion.
Still perform the browser checks below; HTTP checks alone do not verify rendering.

- Confirm the build/test log succeeds and Gunicorn starts with one worker.
- Open the assigned public HTTPS URL with the local server stopped.
- Start Easy, Medium, and Hard games and inspect active JSON for answer omission.
- Verify POST-create returns 201, GET-state returns 200, and POST-guess returns 200.
- Play a complete win or loss, verify final answer disclosure, then restart.
- Inspect at least one public guess request/response in Chrome Developer Tools.
- Record the URL, deployed commit, verification date, and any remaining limits.

## Availability and limitations

Games are memory-only: restarts, deploys, and idle shutdown erase them. Keep one
worker and one service instance; multiple processes do not share the game store.
No automatic game expiry exists, so memory grows with created games.

Render's free services spin down after 15 minutes of inactivity and may take
about a minute to wake. Open the site before recording or grading and start a
fresh game after waking. Free usage limits may also affect availability. Recheck
the URL near submission and during the grading period. Do not claim continuous
availability without monitoring it. No paid service has been authorized.

## Sources

- https://render.com/docs/deploy-flask
- https://render.com/docs/blueprint-spec
- https://render.com/docs/python-version
- https://render.com/docs/free

## Deployment record

October 29, 2026: preparation verified. On Windows/Python 3.11.5, dependency
installation passed (Gunicorn correctly skipped), and all 29 tests passed.
In a fresh Ubuntu/Python 3.12.3 virtual environment, Flask 3.1.3 and Gunicorn
23.0.0 installed successfully; all 29 tests and `pip check` passed. Started
Gunicorn with one worker/four threads and passed the repeatable HTTP smoke check
for the page, assets, all three difficulties, and all required API endpoints.
The test server was shut down afterward. This verifies Linux behavior on the
available local Python; Render is configured to use the 3.11 series.

For a similar Linux check after installing dependencies:

```sh
python tests/smoke_deployment.py --local-gunicorn
```

Confirmed `.env` and the local `.venv` are ignored. No application credentials
are needed or included in deployment files. GitHub's history remains intact.

The student connected Render and explicitly selected “My Workspace” and Free.
Created the service through the connected Render integration rather than a
Blueprint import; its commands match the configuration above. Region is
Virginia; one free instance; branch `main`. The API displays automatic deploys
enabled, but public-Git-URL services require manual deploys (see final verification).

- Service: `srv-dbhcgfpsrm7s73ff6mdg`.
- Initial deployment: `dep-dbhcgg9srm7s73ff6n90`.
- Application commit: `3ad546fb3df7fab00bbb4ced4924a4725b201638`.
- Initial live time: October 29, 2026, about 12:15 a.m. America/New_York.
- Render runtime: Python 3.11.18; build passed all 29 tests.
- Runtime log confirmed Gunicorn bound to `0.0.0.0:10000` with a single
  gthread worker; page requests returned 200.

Public verification command passed against the actual HTTPS URL. It checked
the page/assets, all difficulties, POST-create/GET-state/POST-guess, malformed
guesses, answer omission during play, complete games, post-game rejection,
unknown IDs, and fresh-game creation. No local server was running.

In Chrome on the public URL, played Easy to a six-miss loss (RAINBOW), verified
the completed drawing and final answer, then started Medium and Hard without
reloading. These checks establish current accessibility and playability, not
future uptime. Repeat the public DevTools demonstration in Phase 6 as part of
the recording; Phase 4's detailed Network inspection was on localhost.

The documentation/region update was pushed as `7182e41`, but no automatic
deployment followed. Final review resolved the cause: this service uses a public
Git repository URL. Render's official deployment documentation states that
auto-deploy requires a connected Git provider; public-Git-URL services must be
deployed manually. The API's autoDeploy=yes does not override this constraint.

For future changes: push to main, use Manual Deploy > Deploy latest commit on
the service dashboard (or trigger a deploy through the connected Render tool),
wait for the specific deploy to be live, and repeat the HTTPS smoke check. Do
not trigger duplicate deploys when a connected-provider auto-deploy is already
running. Connecting GitHub properly is an optional follow-up, not required for
the currently working assignment.

Final review re-ran all 29 unit/API tests, JavaScript syntax and dependency checks,
and the public HTTP smoke suite. A fresh Chrome game was won as TIGER using
keyboard input, with correct pattern updates, final disclosure, and disabled
post-game controls. The final source push is followed by an explicit latest-commit
deploy because this service cannot automatically deploy from its public Git URL.

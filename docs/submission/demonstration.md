# Demonstration script and submission checklist

Target length: about 2 minutes 40 seconds. Record your own screen and narration.
The recording is not yet created. Use the deployed site, not localhost.

Application: https://web-based-hangman-game.onrender.com

Repository: https://github.com/nebraassattar/web-based-hangman-game

## Before recording

- Open the public URL early so a free instance has time to wake.
- Close unrelated tabs and hide personal account information/notifications.
- Open Chrome Developer Tools (F12), choose Network, then Fetch/XHR.
- Arrange the page and Network panel so the controls and response are readable.
- Test your screen recorder and microphone; avoid recording passwords or tokens.
- Keep the local Flask server stopped to demonstrate cloud operation.

## Suggested sequence

**0:00-0:20 | Introduce the deployed application.** Show the public HTTPS URL.
Say: "This is my Hangman application, built with Python and Flask on the server
and HTML, CSS, and JavaScript in the browser. It is hosted on Render."

**0:20-0:40 | Start a game.** Choose Easy and click Start game. Point out the
masked word, six chances, drawing, and letter controls. Say: "The server chooses
the word. The browser receives a masked pattern, not the answer."

**0:40-1:20 | Show the HTTP/JSON sequence.** Type Z on the keyboard. Select the
`guess` request in Network. Show Headers (POST and 200), Payload
(`{"letter":"z"}`), and Response. Point out the updated pattern, guessed
letters, remaining_guesses, status=playing, and absence of `word`.
Say: "JavaScript sends the letter using fetch. Flask validates it and asks the
game engine to update the state. The server returns JSON, and JavaScript updates
the page from that response."

**1:20-2:05 | Complete the game.** Click E to show another guess; it may be correct
or incorrect. Continue with unused letters X, Q, V, J, D until the game ends;
stop clicking as soon as it does. Z, X, Q, V, J, and D are absent from all five
current Easy words, so they can be used to demonstrate a loss. E may spend an
additional life; do not assume all six later buttons remain enabled.
Point out the drawing progression, final outcome, answer, and disabled letters.

**2:05-2:25 | Restart.** Choose Medium or Hard and click New game. Show a new masked
word, empty history, six chances, and reset drawing without refreshing the page.

**2:25-2:40 | Explain one design choice.** Say: "Game rules live in a separate
Python engine, so they can be unit tested. The server controls the state. I use
one Gunicorn worker because games are stored in memory; restarting loses them."

## Report review

- Read the two-page PDF and editable Markdown source.
- Confirm the process/challenge descriptions match what you can explain.
- The supplied personal reflection is included. Confirm its wording and regenerate
  the PDF if making further changes.
- Confirm the two URLs, tests, and known limitations are accurate.
- Be able to explain validation, six-miss loss, state serialization, and fetch.

## HuskyCT hand-in

- [ ] Give the report a final review before submitting; verify PDF pages after any further edits.
- [ ] Record the 2-3 minute demonstration with your narration.
- [ ] Review video playback for legible HTTP/JSON details, sound, and a full game/restart.
- [ ] Reopen the public application shortly before submitting and during grading.
- [ ] Submit the GitHub URL, deployed HTTPS URL, PDF report, and video/link as instructed.
- [ ] Confirm uploaded files/links open and retain submission confirmation.

The agent has prepared the report and script; no video or HuskyCT submission is
claimed. Free hosting can sleep and usage limits can affect future availability.

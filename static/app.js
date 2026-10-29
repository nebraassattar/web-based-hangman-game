/* Presentation and HTTP only: Flask owns the word, rules, and outcome. */
"use strict";

const difficulty = document.querySelector("#difficulty");
const newGame = document.querySelector("#new-game");
const keyboard = document.querySelector("#keyboard");
const message = document.querySelector("#message");
const errorMessage = document.querySelector("#error");
const slots = document.querySelector("#word-slots");
const keys = [];
let state = null;
let pending = false;

for (const row of ["qwertyuiop", "asdfghjkl", "zxcvbnm"]) {
  const container = document.createElement("div");
  container.className = "key-row";
  for (const letter of row) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "letter-key";
    button.textContent = letter.toUpperCase();
    button.dataset.letter = letter;
    button.disabled = true;
    button.setAttribute("aria-label", `Guess ${letter.toUpperCase()}`);
    button.addEventListener("click", () => guess(letter));
    container.append(button);
    keys.push(button);
  }
  keyboard.append(container);
}

function updateControls() {
  newGame.disabled = pending;
  difficulty.disabled = pending;
  newGame.firstChild.textContent = pending ? "One moment… " : state ? "New game " : "Start game ";
  keyboard.setAttribute("aria-busy", String(pending));
  for (const key of keys) {
    const letter = key.dataset.letter;
    const used = state?.guessed_letters.includes(letter);
    const incorrect = state?.incorrect_letters.includes(letter);
    key.disabled = pending || !state || state.status !== "playing" || used;
    key.classList.toggle("correct", Boolean(used && !incorrect));
    key.classList.toggle("incorrect", Boolean(incorrect));
    key.setAttribute("aria-label", used ? `${letter.toUpperCase()}, ${incorrect ? "incorrect" : "correct"}` : `Guess ${letter.toUpperCase()}`);
  }
}

function render() {
  const letters = state.pattern.split(" ");
  slots.replaceChildren();
  for (const letter of letters) {
    const slot = document.createElement("span");
    slot.className = "letter-slot";
    slot.textContent = letter === "_" ? "" : letter;
    slot.setAttribute("aria-hidden", "true");
    slots.append(slot);
  }
  slots.setAttribute("aria-label", `Word: ${letters.map(letter => letter === "_" ? "blank" : letter).join(", ")}`);
  document.querySelector("#letter-count").textContent = `${letters.length} letters`;
  document.querySelector("#word-label").textContent = `${state.difficulty.toUpperCase()} · YOUR WORD`;
  document.querySelector("#remaining").textContent = state.remaining_guesses;
  document.querySelector("#guessed").textContent = state.guessed_letters.length ? state.guessed_letters.join(" · ").toUpperCase() : "None yet — a clean slate.";
  document.querySelectorAll("[data-part]").forEach((part, index) => part.toggleAttribute("hidden", index >= state.incorrect_letters.length));
  document.querySelectorAll("#life-dots i").forEach((dot, index) => dot.classList.toggle("spent", index >= state.remaining_guesses));
  document.querySelector("#drawing-description").textContent = `${state.incorrect_letters.length} incorrect guesses. ${state.remaining_guesses} chances remaining.`;
  document.querySelector("#round-label").textContent = state.status === "playing" ? "A WORK IN PROGRESS" : "UNTIL THE NEXT WORD";
  message.className = `message ${state.status}`;
  if (state.status === "won") {
    message.textContent = `Nicely done! The word was ${state.word.toUpperCase()}. Ready for another?`;
  } else if (state.status === "lost") {
    message.textContent = `The word was ${state.word.toUpperCase()}. A fresh word is a fresh start.`;
  } else {
    message.textContent = `${state.remaining_guesses} chances left. ${state.pattern}. Pick your next letter.`;
  }
  updateControls();
}

async function api(path, body) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch(path, {
      method: body === undefined ? "GET" : "POST",
      headers: body === undefined ? {} : { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
      cache: "no-store",
    });
    const result = await response.json();
    if (!response.ok) {
      const error = new Error(result.error?.message || "The request could not be completed.");
      error.status = response.status;
      throw error;
    }
    return result;
  } finally {
    clearTimeout(timeout);
  }
}

async function perform(action) {
  if (pending) return;
  const previousFocus = document.activeElement;
  pending = true;
  errorMessage.hidden = true;
  updateControls();
  try {
    state = await action();
    render();
  } catch (error) {
    let detail = error.status ? error.message : "Could not reach the game server. Check your connection, then try again.";
    // A guess may have reached Flask even when its response was lost. Retrieve
    // authoritative state before enabling another attempt; never guess locally.
    if (state) {
      try {
        state = await api(`/api/games/${state.game_id}`);
        render();
      } catch (recoveryError) {
        state = null;
        slots.replaceChildren();
        slots.setAttribute("aria-label", "Game unavailable. Start a new game.");
        document.querySelector("#word-label").textContent = "GAME UNAVAILABLE";
        document.querySelector("#letter-count").textContent = "—";
        message.className = "message";
        detail = recoveryError.status === 404 ? "This game is no longer available. Start a new game." : "Connection lost. Start a new game when the server is available.";
        message.textContent = "Start a new game to continue.";
      }
    }
    errorMessage.textContent = detail;
    errorMessage.hidden = false;
  } finally {
    pending = false;
    updateControls();
    // Disabled buttons lose focus in browsers. Keep keyboard navigation near
    // the action instead of sending the next Tab back to the page header.
    if (previousFocus === newGame || keys.includes(previousFocus)) {
      const nextKey = keys.find(key => !key.disabled);
      const target = state?.status === "playing" && nextKey ? nextKey : newGame;
      target.focus({ preventScroll: true });
    }
  }
}

function guess(letter) {
  if (!state || pending || state.status !== "playing" || state.guessed_letters.includes(letter)) return;
  return perform(() => api(`/api/games/${state.game_id}/guess`, { letter }));
}

newGame.addEventListener("click", () => perform(() => api("/api/games", { difficulty: difficulty.value })));
document.addEventListener("keydown", event => {
  if (event.ctrlKey || event.altKey || event.metaKey || event.repeat || event.isComposing) return;
  if (event.target.closest("input, select, textarea, [contenteditable]")) return;
  if (/^[a-zA-Z]$/.test(event.key)) {
    event.preventDefault();
    guess(event.key.toLowerCase());
  }
});

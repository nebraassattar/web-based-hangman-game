"""Flask JSON API. Game rules remain in the independent engine."""

from threading import Lock
from uuid import uuid4

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest, HTTPException

from game import GameFinishedError, HangmanGame, InvalidGuessError
from word_manager import WordManager


def create_app(word_manager=None):
    """Create isolated application state; tests can supply a word manager."""
    app = Flask(__name__)
    manager = word_manager if word_manager is not None else WordManager()
    games = {}
    # Serialize game operations so concurrent requests cannot accept a duplicate
    # guess or read a half-updated snapshot. Storage still requires one process.
    lock = Lock()

    @app.get("/")
    def index():
        return render_template("index.html")

    def error(code, message, status):
        return jsonify(error={"code": code, "message": message}), status

    def read_body(field):
        if not request.is_json:
            return None, error("unsupported_media_type", "Use a JSON request body.", 415)
        try:
            body = request.get_json()
        except BadRequest:
            return None, error("invalid_request", "Request body must be valid JSON.", 400)
        if not isinstance(body, dict) or set(body) != {field}:
            return None, error("invalid_request", f"Provide exactly the '{field}' field.", 400)
        return body[field], None

    def public_state(game_id):
        difficulty, game = games[game_id]
        return {"game_id": game_id, "difficulty": difficulty, **game.to_state()}

    @app.post("/api/games")
    def create_game():
        difficulty, failure = read_body("difficulty")
        if failure is not None:
            return failure
        try:
            word = manager.choose_word(difficulty)
        except ValueError:
            return error("invalid_difficulty", "Difficulty must be easy, medium, or hard.", 400)
        with lock:
            game_id = uuid4().hex
            games[game_id] = (difficulty, HangmanGame(word))
            return jsonify(public_state(game_id)), 201

    @app.get("/api/games/<game_id>")
    def get_game(game_id):
        with lock:
            if game_id not in games:
                return error("game_not_found", "Game not found.", 404)
            return jsonify(public_state(game_id))

    @app.post("/api/games/<game_id>/guess")
    def guess(game_id):
        with lock:
            if game_id not in games:
                return error("game_not_found", "Game not found.", 404)
            letter, failure = read_body("letter")
            if failure is not None:
                return failure
            try:
                games[game_id][1].guess(letter)
            except GameFinishedError as exc:
                return error("game_finished", str(exc), 409)
            except InvalidGuessError as exc:
                return error("invalid_guess", str(exc), 400)
            return jsonify(public_state(game_id))

    @app.errorhandler(HTTPException)
    def http_error(exc):
        # Keep routing errors JSON too, without dropping headers such as Allow.
        response = exc.get_response()
        response.data = app.json.dumps({"error": {
            "code": exc.name.lower().replace(" ", "_"),
            "message": exc.description,
        }})
        response.content_type = "application/json"
        return response

    @app.after_request
    def prevent_state_caching(response):
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    return app


app = create_app()


if __name__ == "__main__":
    app.run()

"""API contract tests with fixed test-only words and no running HTTP server."""

import unittest

from server import create_app


class TestWords:
    def choose_word(self, difficulty):
        if not isinstance(difficulty, str) or difficulty not in ("easy", "medium", "hard"):
            raise ValueError("Invalid difficulty")
        return "apple"


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestWords())
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def start(self, difficulty="easy"):
        response = self.client.post("/api/games", json={"difficulty": difficulty})
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("word", response.json)
        return response.json

    def submit(self, game_id, letter):
        return self.client.post(f"/api/games/{game_id}/guess", json={"letter": letter})

    def assert_error(self, response, status):
        self.assertEqual(response.status_code, status)
        self.assertEqual(set(response.json), {"error"})
        self.assertEqual(set(response.json["error"]), {"code", "message"})

    def test_create_and_get_all_difficulties(self):
        ids = set()
        for difficulty in ("easy", "medium", "hard"):
            state = self.start(difficulty)
            self.assertEqual(state["difficulty"], difficulty)
            self.assertEqual(state["status"], "playing")
            self.assertEqual(state["remaining_guesses"], 6)
            self.assertEqual(state["pattern"], "_ _ _ _ _")
            self.assertEqual(set(state), {"game_id", "difficulty", "pattern", "status",
                                          "guessed_letters", "incorrect_letters", "remaining_guesses"})
            ids.add(state["game_id"])
            response = self.client.get(f"/api/games/{state['game_id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, state)
            self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(len(ids), 3)

    def test_correct_incorrect_duplicate_and_invalid_guesses(self):
        game_id = self.start()["game_id"]
        state = self.submit(game_id, "P").json
        self.assertEqual(state["pattern"], "_ p p _ _")
        self.assertEqual(state["remaining_guesses"], 6)
        response = self.submit(game_id, "z")
        self.assertEqual(response.status_code, 200)
        state = response.json
        self.assertEqual(state["incorrect_letters"], ["z"])
        self.assertEqual(state["remaining_guesses"], 5)
        self.assertNotIn("word", state)
        for letter in ("p", "Z", "", "ab", "é", " ", 1, None, [], {}):
            with self.subTest(letter=letter):
                self.assert_error(self.submit(game_id, letter), 400)
                self.assertEqual(self.client.get(f"/api/games/{game_id}").json, state)

    def test_win_and_restart(self):
        game_id = self.start()["game_id"]
        for letter in "aple":
            response = self.submit(game_id, letter)
            self.assertEqual(response.status_code, 200)
            if letter != "e":
                self.assertNotIn("word", response.json)
        final = response.json
        self.assertEqual(final["status"], "won")
        self.assertEqual(final["word"], "apple")
        self.assertEqual(self.client.get(f"/api/games/{game_id}").json, final)
        self.assert_error(self.submit(game_id, "z"), 409)
        self.assertEqual(self.client.get(f"/api/games/{game_id}").json, final)
        new = self.start()
        self.assertNotEqual(new["game_id"], game_id)
        self.assertEqual(new["guessed_letters"], [])

    def test_loss_after_exactly_six_misses(self):
        game_id = self.start()["game_id"]
        for index, letter in enumerate("bcdfgh", start=1):
            response = self.submit(game_id, letter)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["remaining_guesses"], 6 - index)
            self.assertEqual("word" in response.json, index == 6)
        final = response.json
        self.assertEqual(final["status"], "lost")
        self.assertEqual(final["word"], "apple")
        self.assert_error(self.submit(game_id, "a"), 409)
        self.assertEqual(self.client.get(f"/api/games/{game_id}").json, final)

    def test_game_and_application_isolation(self):
        first, second = self.start(), self.start()
        self.submit(first["game_id"], "a")
        self.assertEqual(self.client.get(f"/api/games/{second['game_id']}").json, second)
        other = create_app(TestWords()).test_client()
        self.assert_error(other.get(f"/api/games/{first['game_id']}"), 404)

    def test_invalid_create_bodies(self):
        for body in ({}, {"difficulty": "expert"}, {"difficulty": "Easy"},
                     {"difficulty": None}, {"difficulty": []}, {"difficulty": 1},
                     {"difficulty": "easy", "word": "chosen"}, [], "easy", 1):
            with self.subTest(body=body):
                self.assert_error(self.client.post("/api/games", json=body), 400)

    def test_malformed_non_json_and_invalid_guess_bodies_leave_state_unchanged(self):
        state = self.start()
        path = f"/api/games/{state['game_id']}/guess"
        for endpoint in ("/api/games", path):
            for raw in ("{", "null", "", "[]"):
                with self.subTest(endpoint=endpoint, raw=raw):
                    self.assert_error(self.client.post(endpoint, data=raw, content_type="application/json"), 400)
            self.assert_error(self.client.post(endpoint, data="letter=a"), 415)
            self.assert_error(self.client.post(endpoint, data="{}", content_type="text/plain"), 415)
        for body in ({}, {"letter": "a", "word": "apple"}, {"difficulty": "easy"}):
            self.assert_error(self.client.post(path, json=body), 400)
        self.assertEqual(self.client.get(f"/api/games/{state['game_id']}").json, state)

    def test_unknown_game_route_and_method_errors_are_json(self):
        self.assert_error(self.client.get("/api/games/missing"), 404)
        self.assert_error(self.submit("missing", "a"), 404)
        self.assert_error(self.client.get("/api/not-a-route"), 404)
        response = self.client.delete("/api/games")
        self.assert_error(response, 405)
        self.assertIn("POST", response.headers["Allow"])

    def test_real_word_manager_supports_all_difficulties(self):
        client = create_app().test_client()
        for difficulty in ("easy", "medium", "hard"):
            response = client.post("/api/games", json={"difficulty": difficulty})
            self.assertEqual(response.status_code, 201)
            self.assertNotIn("word", response.json)

    def test_browser_page_and_required_assets_are_served(self):
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "text/html")
            self.assertIn(b'lang="en"', response.data)
        for path, content_type in (("/static/app.js", "javascript"),
                                   ("/static/style.css", "text/css")):
            with self.subTest(path=path), self.client.get(path) as response:
                self.assertEqual(response.status_code, 200)
                self.assertIn(content_type, response.content_type)

from django.test import TestCase, Client


class CreateViewTestCase(TestCase):
    c = Client()

    def test_bad_game_opts(self):
        # Passing NaN to any of the game options fields should give an error
        opts = {
            "Width":      "foo",
            "Height":     "bar",
            "Food":       "baz",
            "Snake.Name": "Snekky Snek",
            "Snake.URL":  "http://localhost"
        }
        resp = self.c.post("/create/", opts)

        assert "error" in resp.json().keys()

    def test_invalid_snake_url(self):
        # Passing invalid snake URL should give error
        opts = {
            "Width":      "10",
            "Height":     "15",
            "Food":       "5",
            "Snake.Name": "Snekky Snek",
            "Snake.URL":  "INVALIDURL"
        }
        resp = self.c.post("/create/", opts)

        assert "error" in resp.json().keys()

    def test_no_snake_name(self):
        # Passing URL without name should give error
        opts = {
            "Width": "10",
            "Height": "15",
            "Food": "5",
            "Snake.URL": "http://localhost"
        }
        resp = self.c.post("/create/", opts)

        assert "error" in resp.json().keys()

    def test_no_snake_url(self):
        # Passing URL without name should give error
        opts = {
            "Width": "10",
            "Height": "15",
            "Food": "5",
            "Snake.Name": "Snekky Snek"
        }
        resp = self.c.post("/create/", opts)

        assert "error" in resp.json().keys()

    def test_no_snakes(self):
        # Passing game options with no snakes should give error
        opts = {
            "Width": "10",
            "Height": "15",
            "Food": "5"
        }
        resp = self.c.post("/create/", opts)

        assert "error" in resp.json().keys()

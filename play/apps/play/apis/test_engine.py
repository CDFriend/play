import subprocess
import os
from django.test import TestCase
from django.core.validators import ValidationError

from .engine import *

ENGINE_TEST_PORT = 50000


class EngineTestCase(TestCase):

    def setUp(self):
        gopath = os.getenv("GOPATH")
        try:
            self._engine_url = "http://localhost:%d" % ENGINE_TEST_PORT
            self._engine = subprocess.Popen(["%s/bin/engine" % gopath, "server",
                                             "-l", ":%d" % ENGINE_TEST_PORT],
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            self.skipTest("Could not find engine executable in GOPATH. "
                          "Is engine installed?")

    def tearDown(self):
        self._engine.terminate()

    def test_create_game(self):
        req = CreateRequest()
        resp = create_game(req, engine_url=self._engine_url)
        assert type(resp.id) is str and len(resp.id) > 0

    def test_createrequest_valid(self):
        req = CreateRequest(width=15, height=12, food=5, snakes=[SnakeOptions()])

        assert req.width == 15
        assert req.height == 12
        assert req.food == 5
        assert len(req.snakes) == 1

    def test_createrequest_invalidopts(self):
        with self.assertRaises(ValueError):
            CreateRequest(width="this", height="is", food="wrong")

    def test_snakeoptions_valid(self):
        opts = SnakeOptions(name="Snekky Snek", id="testid", url="http://localhost:8000")

        assert opts.name == "Snekky Snek"
        assert opts.id == "testid"
        assert opts.url == "http://localhost:8000"

    def test_snakeoptions_invalid_url(self):
        with self.assertRaises(ValidationError):
            SnakeOptions(url="OHNOBADURL")

    def test_createresponse_valid(self):
        resp = CreateResponse(id="testtest")
        assert resp.id == "testtest"

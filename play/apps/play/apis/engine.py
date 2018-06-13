"""
Functions for interfacing with the Battlesnake engine API.
For more information, see API spec here:
    https://github.com/battlesnakeio/docs/blob/master/apis/engine/spec
"""

__engine_api_version__ = "0.0.1"

import requests
from requests.structures import CaseInsensitiveDict
from django.core.validators import URLValidator
from django.conf import settings

val_ = URLValidator()


class CreateRequest:
    def __init__(self, **kwargs):
        self.width  = int(kwargs.get("width", 20))
        self.height = int(kwargs.get("height", 20))
        self.food   = int(kwargs.get("food", 20))

        self.snakes = kwargs.get("snakes", [SnakeOptions()])

        assert type(self.snakes) == list and \
            all(type(s) is SnakeOptions for s in self.snakes), \
            "CreateRequest.snakes must be list of SnakeOptions"
        assert len(self.snakes) > 0, "CreateRequest must have at least one snake"

    def todict(self):
        dict = self.__dict__
        dict["snakes"] = [s.__dict__ for s in self.snakes]
        return dict


class CreateResponse:
    def __init__(self, **kwargs):
        self.id = str(kwargs.get("id", ""))


class SnakeOptions:
    def __init__(self, **kwargs):
        self.name = str(kwargs.get("name", ""))
        self.url  = str(kwargs.get("url", "http://localhost"))
        self.id   = str(kwargs.get("id", ""))

        # Check snake URL is valid
        val_(self.url)


def create_game(create_request, engine_url=settings.ENGINE_URL):
    """Creates a new game on the engine.
    Issues a POST to <engine_url>/games (blocking).
    """
    req_json = create_request.todict()
    resp = requests.post(engine_url + "/games", json=req_json)
    resp_json = CaseInsensitiveDict(resp.json())
    return CreateResponse(id=resp_json["ID"])

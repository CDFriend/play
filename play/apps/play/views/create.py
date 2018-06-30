from django.http import JsonResponse
from django.shortcuts import render

from ..apis.engine import *


def create(request):
    if request.POST:
        req = request.POST

        # TODO: handle validation errors
        snakes = []
        for name, url in zip(req.getlist("Snake.Name"), req.getlist("Snake.URL")):
            if name and url:
                snakes.append(SnakeOptions(name=name, url=url))

        create_req = CreateRequest(width=req.get("Width"),
                                   height=req.get("Height"),
                                   food=req.get("Food"),
                                   snakes=snakes)

        game = create_game(create_req)
        href = "%s/games/%s" % (settings.ENGINE_URL, game.id)

        return JsonResponse({"id": game.id, "href": href})

    return render(request, 'create.html')

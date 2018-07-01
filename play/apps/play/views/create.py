from django.http import JsonResponse
from django.shortcuts import render

from ..apis.engine import *


def create(request):
    """
    Create Game View

    Creates a new game in the engine on POST.

    ~~~ Returns ~~~
    On success:
        { "id" : (GAME ID), "href": (LINK TO GAME) }
    On error:
        { "error" : (ERROR MESSAGE) }
    """
    if request.POST:
        try:
            create_req = _extract_create_request(request.POST)

            game = create_game(create_req)
            href = "%s/games/%s" % (settings.ENGINE_URL, game.id)

            return JsonResponse({"id": game.id, "href": href})

        except Exception as e:
            return JsonResponse({"error": e.message}, status=400)

    return render(request, 'create.html')


def _extract_create_request(req_data):
    snakes = []
    for name, url in zip(req_data.getlist("Snake.Name"), req_data.getlist("Snake.URL")):
        if name and url:
            snakes.append(SnakeOptions(name=name, url=url))

    return CreateRequest(width=req_data.get("Width"),
                         height=req_data.get("Height"),
                         food=req_data.get("Food"),
                         snakes=snakes)

from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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

        except ValidationError as e:
            return JsonResponse({"error": e.messages}, status=400)

    return render(request, 'create.html')


def _extract_create_request(req_data):
    i = 0
    snakes = []
    for name, url in zip(req_data.getlist("Snake.Name"), req_data.getlist("Snake.URL")):
        i += 1
        if name and url:
            # Name and URL specified
            try:
                snakes.append(SnakeOptions(name=name, url=url))
            except ValidationError:
                raise ValidationError(_("Invalid snake URL '%(url)s'"),
                                      params={"url": url},
                                      )

        elif (name and not url) or (url and not name):
            # Name XOR url specified - error!
            raise ValidationError(_("Name or URL not specified for snake %(snake_num)d"),
                                  params={"snake_num": i})

        else:
            # Neither specified - ignore
            pass

    try:
        req = CreateRequest(width=req_data.get("Width"),
                            height=req_data.get("Height"),
                            food=req_data.get("Food"),
                            snakes=snakes)
        return req
    except ValueError:
        raise ValidationError(_("Provided game options value is NaN"))

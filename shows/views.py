import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .config import shows_url, actors_url, actors_ending_url

# Create your views here.

def execute_show_search():
    """
    Sends HTTP request GET to http://api.tvmaze.com/schedule/web?date=2020-01-07
    to obtain list of serials.

    Returns:
        A response from request GET
    """

    url = shows_url

    return requests.get(url=url, timeout=5)


def execute_actors_search(title_id):
    """
    Sends HTTP request GET to http://api.tvmaze.com/shows/{title_id}/cast
    to obtain list of actors from show with id = title_id

    Args:
        title_id (str): show's id

    Returns:
        A response from request GET
    """

    url = actors_url + title_id + actors_ending_url

    return requests.get(url=url, timeout=5)


@api_view(['GET'])
def search_show(request):
    """
    Step 1. Run execute_show_search
    Step 2. check the result, if success continue,
            else break and return info about error
    Step 3. prepare list of shows
    Step 4. render html with list of shows

    Args:
        request: request

    Returns:
        render html with list of shows,
        or Response (dict): info about error.
    """

    result = {
        "status": None,
        "message": None,
    }

    # Step 1. Run execute_show_search
    shows = execute_show_search()

    result["message"] = "There was a problem with send request"
    result["status"] = shows.status_code

    # Step 2. check the result, if success continue, else break
    try:
        if shows.status_code in [200, 201, 202]:
            shows = shows.json()
            length = len(shows)
            list_of_shows = []

            # Step 3. prepare list of shows
            for show in shows:
                show_id = show["_embedded"]["show"]["id"]
                show_title = show["_embedded"]["show"]["name"]
                list_of_shows.append({"id": show_id, "title": show_title})

            # Step 4. render html with list of shows
            return render(request, "shows/index.html", {
                "shows": list_of_shows
            })
    except:
        return Response(result)


@api_view(['GET'])
def search_actor_from_show(request, title_id):
    """
    Step 1. Run execute_actor_search
    Step 2. check the result, if success continue,
            else break and return info about error
    Step 3. prepare list of actors
    Step 4. render html with list of actors

    Args:
        request: request

    Returns:
        render html with list of shows,
        or Response (dict): info about error.
    """

    result = {
        "status": None,
        "message": None,
    }

    # Step 1. Run execute_actor_search
    actors = execute_actors_search(title_id=title_id)

    result["message"] = "There was a problem with send request"
    result["status"] = actors.status_code

    # Step 2. check the result, if success continue, else break
    try:
        if actors.status_code in [200, 201, 202]:
            actors = actors.json()
            list_of_authors = []

            # Step 3. prepare list of actors
            for actor in actors:
                actor_id = actor["person"]["id"]
                actor_name = actor["person"]["name"]
                list_of_authors.append({"id": actor_id, "name": actor_name})

            # Step 4. render html with list of actors
            return render(request, "actors/index.html", {
                "actors": list_of_authors
            })
    except:
        return Response(result)
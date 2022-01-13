import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def wiki_search(title):
    """Get title info from Wikimedia API"""

    # Contact API
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&generator=prefixsearch&gpssearch={urllib.parse.quote_plus(title)}&gpslimit=3&pilicense=any&prop=pageimages|pageterms&piprop=original&pilimit=3&redirects=&wbptterms=description"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse JSON data
    response = response.json()
    # print(response)

    response = response['query']['pages']
    search_response = []
    for search_details in response.values():
        # remove 'ns' key
        search_details.pop('ns') if 'ns' in search_details else None
        # Create 'description' key from 'terms'  and remove 'terms' key
        search_details['description'] = search_details['terms']['description'].pop() if 'terms' in search_details else None
        search_details.pop('terms') if 'terms' in search_details else None
        search_response.append(search_details)

    # print(search_response)

    # return sorted search response by index
    return sorted(search_response, key=lambda x: x['index'])
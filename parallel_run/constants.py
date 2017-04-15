"""
Module to hold the static definitions.
"""


URLS = {
    "google": (
        "https://www.googleapis.com/customsearch/v1?key={key}"
        "&cx=017576662512468239146:omuauf_lfve&q={q}&limit=1"
    ),
    "duckduckgo": "http://api.duckduckgo.com/?format=json&q={q}",
    "twitter": (
        "https://api.twitter.com/1.1/search/tweets.json?q={q}&"
        "count={limit}&type=recent"
    ),
    None: None
}

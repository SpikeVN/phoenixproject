import json

import requests


def serialize_session(session: requests.Session):
    attrs = [
        "headers",
        "cookies",
        "auth",
        "proxies",
        "hooks",
        "params",
        "timeout",
        "config",
        "verify",
    ]

    session_data = {}
    requests.session()
    for attr in attrs:
        session_data[attr] = getattr(session, attr)

    return json.dumps(session_data)


def deserialize_session(data):
    session_data = json.loads(data)

    if "auth" in session_data:
        session_data["auth"] = tuple(session_data["auth"])

    if "cookies" in session_data:
        session_data["cookies"] = dict(
            (key.encode(), val) for key, val in session_data["cookies"].items()
        )

    # noinspection PyArgumentList
    return requests.session(**session_data)

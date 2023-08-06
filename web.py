#!/usr/bin/env python3
import threading
import webbrowser

import bottle
import countMeDown


@bottle.route("/", method="GET")
def get_page():
    return bottle.template("form")


@bottle.route("/", method="POST")
def handle_post():
    request_args = bottle.request.forms
    if request_args.mode == "mode_duration":
        seconds = countMeDown.get_seconds_from_mixed_format(
            request_args.get("duration")
        )
    else:
        seconds = countMeDown.get_seconds_until_time(request_args.time)

    command = threading.Thread(
        target=countMeDown.count_me_down,
        args=(
            seconds,
            request_args.prefix,
            request_args.ending,
            int(request_args.step),
            "./time.txt",
            True,
        ),
    )
    command.start()

    return "yay"


if __name__ == "__main__":
    server = threading.Thread(
        target=bottle.run, kwargs={"host": "localhost", "port": 22222}
    )
    server.start()

    webbrowser.open("http://localhost:22222")

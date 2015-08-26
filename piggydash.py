#!/usr/bin/env python

from yaml import load
from os import path
from addict import Dict
import requests
import simple
import notifications

def parse_yaml():
    settings = None

    if not path.isfile("./secrets.yml"):
        raise Exception("Missing secrets.yml")
    else:
        with open("./secrets.yml", "rb") as f:
            settings = Dict(load(f))

    if (
        not settings.simple.username or
        not settings.simple.password or
        not settings.simple.goal_name or
        not settings.simple.transfer_amount
    ):
        raise Exception("Missing required secret keys/config, check secrets.example.yml for instructions")
    else:
        return settings


def main():
    settings = parse_yaml()

    session = requests.Session()
    session.headers.update({
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    })

    simple.login(settings.simple, session)
    csrf = simple.get_csrf(session)
    goal_id = simple.goal_lookup(session, csrf, settings.simple.goal_name)
    success = simple.transact(session, csrf, settings.simple.transfer_amount, goal_id)

    # Instapush notification is optional -- don't do this if the credentials are not present
    if settings.instapush.id and settings.instapush.secret and success:
        notifications.push_notify(settings.instapush, settings.simple.transfer_amount, settings.simple.goal_name)


if __name__ == "__main__":
    main()

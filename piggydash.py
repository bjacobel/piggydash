#!/usr/bin/env python

from yaml import load
from instapush import Instapush, App
from os import path
from addict import Dict

def parse_yaml():
    if not path.isfile("./secrets.yml"):
        raise Exception("Missing secrets.yml")
    else:
        with open("./secrets.yml", "rb") as f:
            return Dict(load(f))


def push_notify(instapush, amount, goal):
    # Requires creating an app in Instapush and putting its credentials in secrets.yml
    app = App(appid=instapush.id, secret=instapush.secret)

    events = app.list_event()

    if 'transfer' not in [event['title'] for event in events]:
        # transfer doesn't exist yet, we have to create it
        app.add_event(
            event_name = 'transfer',
            trackers   = ['amount', 'goal'],
            message    = '${amount} transferred to {goal}.'
        )

    app.notify(event_name = 'transfer', trackers = {
        'amount': amount,
        'goal': goal
    })


def main():
    settings = parse_yaml()

    amount = 5
    goal = "Rainy Day Fund"

    if settings.instapush.id and settings.instapush.secret:
        push_notify(settings.instapush, amount, goal)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from yaml import load
from os import path
from addict import Dict
from bs4 import BeautifulSoup
import instapush
import requests
import re
import urllib


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


def login(simple, session):
    login_page = session.get("https://bank.simple.com/signin")
    login_content = login_page.content

    csrf = BeautifulSoup(login_content, 'html.parser').find('input', {"name": "_csrf"})['value']

    response = session.post(
        "https://bank.simple.com/signin",
        data = {
            "username": simple.username,
            "password": simple.password,
            "_csrf": csrf
        },
        headers = {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )

    if not response.ok:
        raise Exception("Something happened with Simple authentication.")


def get_csrf(session):
    goals_page = session.get("https://bank.simple.com/goals")

    return BeautifulSoup(goals_page.content, 'html.parser').find('meta', {"name":"_csrf"})['content']


def goal_lookup(session, csrf, goal_name):
    response = session.get(
        url = "https://bank.simple.com/goals/data",
        headers = {
            "X-Request": "JSON",
            "X-CSRF-Token": csrf
        }
    )

    for goal in response.json():
        if goal['name'] == goal_name and not goal['archived']:
            return goal['id']

    raise Exception("No goal matching specified name found")


def transact(session, csrf, dollars, goal_id):
    response = session.post(
        url = "https://bank.simple.com/goals/{}/transactions".format(goal_id),
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        data = {
            "amount": int(dollars * 10000),
            "_csrf": csrf,
        }
    )

    return response.ok


def push_notify(settings, amount, goal):
    # Requires creating an app in Instapush and putting its credentials in secrets.yml
    app = instapush.App(
        appid = settings.id,
        secret = settings.secret
    )

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

    session = requests.Session()
    session.headers.update({
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    })

    login(settings.simple, session)
    csrf = get_csrf(session)
    goal_id = goal_lookup(session, csrf, settings.simple.goal_name)
    success = transact(session, csrf, settings.simple.transfer_amount, goal_id)

    # Instapush notification is optional -- don't do this if the credentials are not present
    if settings.instapush.id and settings.instapush.secret and success:
        push_notify(settings.instapush, settings.simple.transfer_amount, settings.simple.goal_name)


if __name__ == "__main__":
    main()

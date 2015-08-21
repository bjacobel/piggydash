#!/usr/bin/env python

from yaml import load
from os import path
from addict import Dict
from bs4 import BeautifulSoup
import instapush
import requests
import re

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"

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
        not settings.simple.goal
    ):
        raise Exception("Missing required secret keys, check secrets.example.yml for instructions")
    else:
        return settings


def login(simple):
    login_page = requests.get("https://bank.simple.com/signin")
    login_content = login_page.content
    login_session_cookie = re.search(r"_simple_session=([a-z0-9]+);", login_page.headers['Set-Cookie']).group(1)

    csrf = BeautifulSoup(login_content, 'html.parser').find_all('input')[-1]['value']

    response = requests.post(
        "https://bank.simple.com/signin",
        data = {
            "username": simple.username,
            "password": simple.password,
            "_csrf": csrf
        },
        headers = {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": user_agent,
            "Cookie": "_simple_session={}".format(login_session_cookie),
        }
    )

    if not response.ok:
        raise Exception("Something happened with Simple authentication.")

    return login_session_cookie


def transact(simple, session, dollars):
    goals_page = requests.get("https://bank.simple.com/goals", headers = {
        "Cookie": "_simple_session={}".format(session),
        "User-Agent": user_agent
    })

    csrf = BeautifulSoup(goals_page.content, 'html.parser').find_all('input')[-1]['value']

    response = requests.post(
        "https://bank.simple.com/goals/{}/transactions".format(simple.goal),
        data = {
            "amount": int(dollars * 10000),
            "_csrf": csrf
        },
        headers = {
            "User-Agent": user_agent,
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "_simple_session={}".format(session),
            "X-Requested-With": "XMLHttpRequest"
        }
    )

    import ipdb; ipdb.set_trace()


def push_notify(instapush, amount, goal):
    # Requires creating an app in Instapush and putting its credentials in secrets.yml
    app = instapush.App(appid=instapush.id, secret=instapush.secret)

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

    session_cookie = login(settings.simple)
    transact(settings.simple, session_cookie, 0.01)

    # Instapush notification is optional -- don't do this if the credentials are not present
    # if settings.instapush.id and settings.instapush.secret:
    #     push_notify(settings.instapush, amount, goal)


if __name__ == "__main__":
    main()

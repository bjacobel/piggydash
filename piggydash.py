#!/usr/bin/env python

from yaml import load
from os import path
from addict import Dict
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

    sp = simple.Simple(settings.simple)

    sp.login()
    sp.goal_lookup()

    success = sp.transact()

    # IFTTT maker notification is optional -- don't do this if the credentials are not present
    if settings.ifttt.key and success:
        notifications.push_notify(settings.ifttt.key, settings.simple.transfer_amount, settings.simple.goal_name)


if __name__ == "__main__":
    main()

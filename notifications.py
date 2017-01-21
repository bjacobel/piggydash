import requests

def push_notify(key, amount, goal):
    requests.post(
        "https://maker.ifttt.com/trigger/piggydash/with/key/{key}".format(key=key),
        json={
            "value1": "%.2f" % amount,
            "value2": goal
        }
    )

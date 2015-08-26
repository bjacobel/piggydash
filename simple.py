from bs4 import BeautifulSoup
import requests

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

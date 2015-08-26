from bs4 import BeautifulSoup
import requests

class Simple:
    def __init__(self, simple_settings):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) " +
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
        })

        self.username = simple_settings.username
        self.password = simple_settings.password
        self.goal_name = simple_settings.goal_name
        self.transfer_amount = simple_settings.transfer_amount


    def login(self):
        login_page = self.session.get("https://bank.simple.com/signin")
        login_content = login_page.content

        login_csrf = BeautifulSoup(login_content, 'html.parser').find('input', {"name": "_csrf"})['value']

        response = self.session.post(
            "https://bank.simple.com/signin",
            data = {
                "username": self.username,
                "password": self.password,
                "_csrf": login_csrf
            },
            headers = {
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
        )

        if not response.ok:
            raise Exception("Something happened with Simple authentication.")


    def get_csrf(self):
        try:
            self.csrf
            return
        except AttributeError:
            goals_page = self.session.get("https://bank.simple.com/goals")

            self.csrf =  BeautifulSoup(goals_page.content, 'html.parser').find('meta', {"name":"_csrf"})['content']


    def goal_lookup(self):
        self.get_csrf()

        response = self.session.get(
            url = "https://bank.simple.com/goals/data",
            headers = {
                "X-Request": "JSON",
                "X-CSRF-Token": self.csrf
            }
        )

        for goal in response.json():
            if goal['name'] == self.goal_name and not goal['archived']:
                self.goal_id = goal['id']
                return

        raise Exception("No goal matching specified name found")


    def transact(self):
        self.get_csrf()

        response = self.session.post(
            url = "https://bank.simple.com/goals/{}/transactions".format(self.goal_id),
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data = {
                "amount": int(self.transfer_amount * 10000),
                "_csrf": self.csrf,
            }
        )

        return response.ok

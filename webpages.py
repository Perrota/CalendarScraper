import requests
from bs4 import BeautifulSoup


class Page():

    def __init__(self, url):
        self.url = url

    def request_and_parse(self) -> BeautifulSoup:
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

import datetime
import json

from webpages import Page


class PromiedosWebPage(Page):

    BASE_URL = 'https://promiedos.com.ar/games/'

    def __init__(self):
        super().__init__(self.BASE_URL)

    def get_matches(self, date: str) -> list['Match']:
        self.url = self.BASE_URL + date
        soup = self.request_and_parse()
        if soup is None:
            raise RuntimeError("Failed to fetch or parse Promiedos webpage.")
        
        raw_data = soup.select_one("#__NEXT_DATA__")
        if raw_data is None:
            raise RuntimeError("Could not find embedded JSON data in page.")
        
        data = json.loads(raw_data.text)
        leagues = data['props']['pageProps']['data']['leagues']

        return [
            Match(
                league['name'],
                game['teams'][0]['short_name'],
                game['teams'][1]['short_name'],
                date,
                game['start_time'][-5:]
            )
            for league in leagues
            for game in league['games']
        ]

class Match():

    def __init__(self, liga: str, local: str, visitante: str, date: str, time: str) -> None:
        self.liga = liga
        self.local = local
        self.visitante = visitante
        self.date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
        self.time = datetime.datetime.strptime(time, '%H:%M').time()
        self.description = self.local + ' vs ' + self.visitante

    def __repr__(self) -> str:
        return (
            f"Match({self.liga!r}, {self.local!r} vs {self.visitante!r}, "
            f"{self.date} at {self.time})"
        )

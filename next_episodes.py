import datetime
import logging
from typing import cast

from bs4 import Tag

from webpages import Page


class NextEpisodeDotNet(Page):

    def __init__(self, logging_level: int = 0) -> None:
        super().__init__('https://next-episode.net')
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)

    def get_episodes(self) -> list['Episode']:
        soup = self.request_and_parse()

        inner_calendar = soup.select_one('td #innercalendar')
        if not inner_calendar:
            raise RuntimeError("Did not find inner calendar in NextEpisode.net")

        span_calendar = inner_calendar.span
        if not span_calendar is not None:
            raise RuntimeError("Did not find the div containing shows in NextEpisode.net")

        div_shows = span_calendar.find_all('div', recursive=False)
        div_shows = [tag for tag in div_shows if isinstance(tag, Tag)]

        # Extract show times
        time_strings = [tag.div.text for tag in div_shows if tag.div]
        show_times = [
            datetime.datetime.combine(
                datetime.date.today(),
                datetime.datetime.strptime(t, "%I:%M%p").time()
            ) + datetime.timedelta(hours=2)
            for t in time_strings
        ]
        show_times = [
            t if t >= datetime.datetime.now()
            else t + datetime.timedelta(days=1)
            for t in show_times
        ]

        # Extract titles and episode numbers
        show_titles = [cast(Tag, tag.select_one('a')).text for tag in div_shows if tag.select_one('a')]
        episode_numbers = [
            tag.select('div')[2].text
            for tag in div_shows
            if len(tag.select('div')) > 2
        ]

        return [
            Episode(show, episode, time)
            for show, episode, time in zip(show_titles, episode_numbers, show_times)
        ]

class Episode():

    def __init__(self, show, episode_n, start_time) -> None:
        self.show = show
        self.episode_n = episode_n
        self.start_time = start_time

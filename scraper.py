import datetime
import json
import sys
from pathlib import Path

from events_db import Config, ConfigsTable
from next_episodes import NextEpisodeDotNet
from promiedos import PromiedosWebPage


def matches_title(episode_title: str, show_titles: list[str]) -> bool:
    return any(
        show.strip() in episode_title or show.strip().title() in episode_title
        for show in show_titles
    )


def load_config(file_name: str = 'config.json') -> dict:
    path = Path(__file__).parent / file_name
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def get_upcoming_dates(days: int = 2) -> list[str]:
    today = datetime.date.today()
    return [
        (today + datetime.timedelta(days=i)).strftime('%d-%m-%Y')
        for i in range(days)
    ]


def main() -> None:
    config = load_config()
    shows = config.get('shows', [])
    teams = config.get('teams', [])

    table_configs = ConfigsTable()

    # Get and filter matches
    promiedos = PromiedosWebPage()
    upcoming_matches = []
    for day in get_upcoming_dates():
        upcoming_matches.extend(promiedos.get_matches(day))
    
    vip_matches = [
        match for match in upcoming_matches
        if match.home in teams or match.away in teams
    ]
    for match in vip_matches:
        table_configs.upload_config(Config.from_match(match))

    # Get and filter episodes
    episodes = NextEpisodeDotNet().get_episodes()
    vip_episodes = [
        episode
        for episode in episodes
        if matches_title(episode.show, shows)
    ]
    for episode in vip_episodes:
        table_configs.upload_config(Config.from_episode(episode))

    sys.exit(0)


if __name__ == "__main__":
    main()

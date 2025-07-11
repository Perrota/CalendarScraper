from datetime import datetime

from sqlalchemy import engine, text

from next_episodes import Episode
from promiedos import Match


class ConfigsTable():

    def __init__(self) -> None:
        self.engine = engine.create_engine('mssql+pyodbc://.\\SQLEXPRESS01/Agenda?driver=ODBC+Driver+17+for+SQL+Server')

    def upload_config(self, config):
        with self.engine.connect() as connection:
            query = text("EXEC usp_SaveNewConfig :param1, :param2, :param3, :param4, :param5")
            connection.execute(query, {
                    "param1": config.starting_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "param2": config.description,
                    "param3": int(config.repeat),
                    "param4": config.per,
                    "param5": config.unit
                }
            )
            connection.commit()

class Config():

    def __init__(self, starting_datetime: datetime, description: str , repeat: bool = False, per = None, unit = None) -> None:
        self.starting_datetime = starting_datetime
        self.description = description
        self.repeat = repeat
        self.database_id = None
        self.per = per
        self.unit = unit
    
    @staticmethod
    def from_episode(epidose: Episode):
        return Config(
            starting_datetime = epidose.start_time,
            description = epidose.show + ' ' + epidose.episode_n,
            repeat = False
        )
    
    @staticmethod
    def from_match(match: Match):
        return Config(
            starting_datetime = datetime.combine(match.date, match.time),
            description = match.local + ' vs ' + match.visitante,
            repeat = False
        )
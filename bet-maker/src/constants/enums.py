from enum import Enum


class EventStatus(str, Enum):
    NEW = "new"
    FIRST_TEAM_WON = "first_team_won"
    SECOND_TEAM_WON = "second_team_won"

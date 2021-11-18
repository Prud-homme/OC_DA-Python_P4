from __future__ import annotations

from typing import TypedDict, Union

from .match import Match
from .player import Player
from .tournament import Tournament
from .turn import Turn


class SerializedPlayer(TypedDict):
    firstname: str
    lastname: str
    birthdate: str
    gender: str
    ranking: int


class SerializedPartialPlayer(TypedDict):
    firstname: str
    lastname: str
    birthdate: str
    gender: str


class SerializedMatch(TypedDict):
    match: tuple[
        list[Union[SerializedPlayer, float], list[Union[SerializedPlayer, float]]]
    ]


class SerializedTurn(TypedDict):
    name: str
    start_date: str
    end_date: str
    matches: list[Match]


class SerializedPartialTournament(TypedDict):
    name: str
    location: str
    date: str
    description: str
    time_control: str
    turns_number: int
    players_number: int


class SerializedTournament(TypedDict):
    name: str
    location: str
    date: str
    description: str
    time_control: str
    turns_number: int
    players_number: int
    turns: list[Turn]
    players: list[Player]

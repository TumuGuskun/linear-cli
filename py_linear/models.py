from dataclasses import dataclass
from uuid import UUID


@dataclass
class Team:
    id: UUID
    name: str


@dataclass
class User:
    id: UUID | None
    name: str = "Unassigned"
    displayName: str = "Unassigned"


@dataclass
class State:
    name: str


@dataclass
class Issue:
    id: str
    assignee: User
    description: str
    identifier: str
    state: State
    team: Team
    title: str
    url: str

    def __post_init__(self):
        if self.assignee and isinstance(self.assignee, dict):
            self.assignee = User(**self.assignee)
        else:
            self.assignee = User(None)
        if self.state and isinstance(self.state, dict):
            self.state = State(**self.state)
        if self.team and isinstance(self.team, dict):
            self.team = Team(**self.team)

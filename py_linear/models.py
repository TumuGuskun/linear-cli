from dataclasses import dataclass


@dataclass
class Team:
    id: str
    name: str


@dataclass
class User:
    name: str


@dataclass
class Issue:
    assignee: User
    title: str
    branchName: str
    description: str
    id: str
    identifier: str

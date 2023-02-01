import requests
from pprint import pprint
from typing import Any
from dotenv import dotenv_values

from py_linear.queries import (
    create_issue_gql,
    get_team_id_gql,
    get_viewer_gql,
    issue_by_identifier_gql,
    issues_matching_text_gql,
    update_assignee_gql,
    viewer_issues_gql,
)
from py_linear.models import Issue, User


class Linear:
    def __init__(self, base_url: str, token: str, debug: bool = False) -> None:
        self.debug = debug
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Authorization": f"{token}"}

    def linear_post(self, gql_query: str) -> dict[str, Any]:
        response = requests.post(
            url=self.base_url, headers=self.headers, json={"query": gql_query}
        )
        if self.debug:
            pprint(gql_query)
            pprint(response.json())
        return response.json().get("data")

    def get_my_issues(self) -> list[Issue]:
        result = self.linear_post(gql_query=viewer_issues_gql())

        issues = []
        if result:
            issues.extend(
                [
                    Issue(**issue)
                    for issue in result["viewer"]["assignedIssues"]["nodes"]
                ]
            )
        return issues

    def get_issue_by_identifier(self, issue_identifier: str) -> Issue | None:
        result = self.linear_post(
            gql_query=issue_by_identifier_gql(identifier=issue_identifier)
        )

        issue = None
        if result:
            issue = Issue(**result["issue"])
        return issue

    def get_issue_by_text(self, text: str) -> list[Issue]:
        result = self.linear_post(gql_query=issues_matching_text_gql(text=text))

        issues = []
        if result:
            issues.extend([Issue(**issue) for issue in result["issues"]["nodes"]])
        return issues

    def create_issue(self, title: str, description: str, team_name: str) -> Issue:
        result = self.linear_post(gql_query=get_team_id_gql(team_name=team_name))
        team_id = result["teams"]["nodes"][0]["id"]

        mutation = create_issue_gql(
            title=title, description=description, team_id=team_id
        )

        result = self.linear_post(gql_query=mutation)
        return Issue(**result["issueCreate"]["issue"])

    def assign_issue(self, issue_id: str, user_id: str) -> None:
        self.linear_post(
            gql_query=update_assignee_gql(issue_id=issue_id, user_id=user_id)
        )

    def get_curr_user(self) -> User:
        result = self.linear_post(gql_query=get_viewer_gql())
        return User(**result["viewer"])


if __name__ == "__main__":
    env_vars = dotenv_values()
    linear = Linear(
        base_url=str(env_vars.get("LINEAR_URL")),
        token=str(env_vars["LINEAR_TOKEN"]),
        debug=True,
    )

    linear.create_issue("test 2", "n/a", "infra")

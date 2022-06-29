from dotenv import dotenv_values
from gql_query_builder import GqlQuery
from pprint import pprint
import requests

from py_linear.queries import team_gql
from py_linear.models import Issue


class Linear:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{token}'
        }

    def get_my_issues(self) -> list[Issue]:
        nodes = GqlQuery().fields(
            [team_gql(), 'title', 'description', 'id', 'identifier'], name='nodes').generate()
        assigned_issues = GqlQuery().fields(
            [nodes], name='assignedIssues').generate()
        query = GqlQuery().query('viewer').fields(
            [assigned_issues]).operation().generate()
        print(query)
        response = requests.get(
            url=self.base_url, headers=self.headers, params={'query': query})
        return response.json()


if __name__ == '__main__':
    env_vars = dotenv_values()
    linear = Linear(base_url=env_vars['LINEAR_URL'],
                    token=env_vars['LINEAR_TOKEN'])
    pprint(linear.get_my_issues())

from uuid import UUID
from gql_query_builder import GqlQuery


def issue_fields() -> list[str]:
    return [
        team_gql(),
        "title",
        "description",
        "id",
        "identifier",
        state_gql(),
        assignee_gql(),
        "url",
    ]


def issue_gql() -> str:
    return GqlQuery().fields(issue_fields()).query("issue").generate()


def team_gql() -> str:
    return GqlQuery().fields(["name", "id"]).query("team").generate()


def state_gql() -> str:
    return GqlQuery().fields(["name"]).query("state").generate()


def user_fields() -> list[str]:
    return ["name", "id", "displayName"]


def assignee_gql() -> str:
    return GqlQuery().fields(user_fields()).query("assignee").generate()


def user_issues_gql() -> str:
    return (
        GqlQuery()
        .fields([nodes_gql(issue_fields())])
        .query(
            "assignedIssues",
            input={
                "filter": '{ and: [ { state: { name: { neq: "Done" } } }, { state: { name: { neq: "Canceled" } } } ]}'
            },
        )
        .generate()
    )


def nodes_gql(fields: list[str]) -> str:
    return GqlQuery().fields(fields).query("nodes").generate()


def issue_by_identifier_gql(identifier: str) -> str:
    return (
        GqlQuery()
        .fields(issue_fields())
        .query("issue", input={"id": f'"{identifier}"'})
        .operation()
        .generate()
    )


def viewer_issues_gql() -> str:
    return GqlQuery().fields([user_issues_gql()]).query("viewer").operation().generate()


def issues_matching_text_gql(text: str) -> str:
    return (
        GqlQuery()
        .fields([nodes_gql(issue_fields())])
        .query(
            "issues",
            input={
                "filter": f'{{ or: [ {{ title : {{ containsIgnoreCase: "{text}" }} }}, {{ description : {{ containsIgnoreCase: "{text}" }} }} ] }}'
            },
        )
        .operation()
        .generate()
    )


def get_team_id_gql(team_name: str) -> str:
    return (
        GqlQuery()
        .fields([nodes_gql(["id"])])
        .query(
            "teams", input={"filter": f'{{ name: {{ eqIgnoreCase: "{team_name}" }} }}'}
        )
        .operation()
        .generate()
    )


def create_issue_gql(title: str, description: str, team_id: UUID) -> str:
    return (
        GqlQuery()
        .fields(["success", issue_gql()])
        .query(
            "issueCreate",
            input={
                "input": f'{{ title: "{title}", description: "{description}", teamId: "{team_id}" }}'
            },
        )
        .operation("mutation", name="IssueCreate")
        .generate()
    )


def update_assignee_gql(issue_id: str, user_id: str) -> str:
    return (
        GqlQuery()
        .fields([issue_gql()])
        .query(
            "issueUpdate",
            input={"id": f'"{issue_id}"', "input": f'{{ assigneeId: "{user_id}" }}'},
        )
        .operation("mutation", name="IssueUpdate")
        .generate()
    )


def get_viewer_gql() -> str:
    return GqlQuery().fields(user_fields()).query("viewer").operation().generate()

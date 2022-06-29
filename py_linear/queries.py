from gql_query_builder import GqlQuery
# def node_gql(


def team_gql():
    return GqlQuery().fields(['name', 'id'], name='team').generate()

import graphene
import movies.schema
import account.schema
import graphql_jwt

class Query(movies.schema.Query, account.schema.Query, graphene.ObjectType):
	pass

class StarWarsMutations(movies.schema.Mutations, account.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=StarWarsMutations)

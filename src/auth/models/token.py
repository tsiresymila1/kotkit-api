from nestipy.graphql.strawberry import ObjectType


@ObjectType()
class TokenResponse:
    token: str

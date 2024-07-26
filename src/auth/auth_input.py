from nestipy.graphql.strawberry import Input


@Input()
class LoginInput:
    username: str
    password: str


@Input()
class RegisterInput:
    username: str
    password: str
    email: str
    name: str

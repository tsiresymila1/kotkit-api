from nestipy.graphql.strawberry import Input
from strawberry.file_uploads import Upload


@Input()
class CreateVideoInput:
    title: str
    description: str
    video: Upload

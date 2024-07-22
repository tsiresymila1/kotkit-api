import os.path

import uvicorn
from nestipy.core import NestipyFactory
from nestipy.openapi import DocumentBuilder, SwaggerModule

from app_module import AppModule

app = NestipyFactory.create(AppModule)

app.use_static_assets(os.path.join(os.getcwd(), "assets"), "/assets")

document = (
    DocumentBuilder().set_title("KOTKIT").set_description("Video streaming alternative tiktok")
    .add_bearer_auth()
    .build()
)
SwaggerModule.setup('api', app, document)

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)

import uvicorn
from fastapi import FastAPI

from app.api import router
from config import config

tags_metadata = [
    config.service.tags_metadata_transaction,  # type: ignore
    config.service.tags_metadata_health,  # type: ignore
]  # type: ignore
app = FastAPI(
    title=config.service.title,  # type: ignore
    description=config.service.description,  # type: ignore
    tags_metadata=tags_metadata,
    debug=config.service.debug,  # type: ignore
)  # type: ignore

app.include_router(
    router,
    prefix='/api',
)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432

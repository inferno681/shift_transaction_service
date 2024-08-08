from fastapi import APIRouter

from app.api.endpoints import router_healthz, router_transaction
from config import config

router = APIRouter()

router.include_router(
    router_transaction,
    tags=[config.service.tags_metadata_transaction['name']],  # type: ignore
)
router.include_router(
    router_healthz,
    tags=[config.service.tags_metadata_health['name']],  # type: ignore
)

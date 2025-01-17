from fastapi import APIRouter

import fastapi_logging
from models.responses import AccountIdsListResponse
from services.data import DataService

logger = fastapi_logging.get_logger(__name__)

router = APIRouter()
data_service = DataService()


@router.get(
    "/account_ids",
    response_model=AccountIdsListResponse,
    summary="Получить список всех account_id игроков",
)
async def get_account_ids():
    logger.info("GET request /api/v1/data/account_ids")
    account_ids = data_service.get_account_ids()
    logger.info(f"Loaded account IDs: {len(account_ids)}")
    return AccountIdsListResponse(account_ids=account_ids)

from fastapi import APIRouter

from src.api.routes.bundle import bundle_router
from src.api.routes.household import household_router
from src.api.routes.product import product_router
from src.api.routes.routes import api_authentication
from src.api.routes.start import start_router
from src.api.routes.token import api_backend_router

api_router = APIRouter()
# api_router.include_router(household_router)
# api_router.include_router(product_router)
# api_router.include_router(api_authentication)
# api_router.include_router(start_router)
api_router.include_router(api_backend_router)



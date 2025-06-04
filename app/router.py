from fastapi import APIRouter

from app.api.auth.auth_api import router as auth_router
from app.api.products.product_api import router as product_router


route = APIRouter()

route.include_router(auth_router, prefix=("/auth"), tags=["AUTH"])
route.include_router(product_router, prefix=("/product"), tags=["PRODUCT"])
# route.include_router(comparison_router, prefix=("/comparison"), tags=["COMPARISON"])
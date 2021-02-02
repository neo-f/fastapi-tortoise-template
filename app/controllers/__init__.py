from fastapi import APIRouter
from app.controllers import demo

router = APIRouter()
router.include_router(demo.router)

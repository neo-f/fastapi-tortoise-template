from fastapi import APIRouter
from app.controllers import demo

router = APIRouter()
router.include(demo.router)

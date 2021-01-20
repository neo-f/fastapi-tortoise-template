from fastapi import APIRouter, Depends

from app import schemas
from app.models import Demo
from app.utils.paginator import Pagination, PaginationResult

router = APIRouter()


@router.get("/demo", response_model=PaginationResult[schemas.DemoDetail], tags=["Animal"])
async def list_demos(p: Pagination = Depends(Pagination)):
    queryset = Demo.all()
    return await p.apply(queryset, schemas.DemoDetail)

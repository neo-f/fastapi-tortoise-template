import asyncio
from typing import Generic, List, Type, TypeVar

from fastapi import Query
from pydantic.generics import GenericModel
from tortoise.queryset import QuerySet

from app.core.config import settings
from app.schemas import Schema

DataT = TypeVar("DataT")


class PaginationResult(GenericModel, Generic[DataT]):
    count: int
    results: List[DataT]


class Pagination:
    def __init__(
        self,
        limit: int = Query(default=settings.default_limit, ge=1, le=settings.max_limit),
        offset: int = Query(default=0, ge=0),
    ):
        self.limit = limit
        self.offset = offset

    async def apply(self, qs: QuerySet, schema: Type[Schema]):
        count, results = await asyncio.gather(qs.count(), qs.limit(self.limit).offset(self.offset))
        return PaginationResult(count=count, results=[schema.from_orm(obj) for obj in results])

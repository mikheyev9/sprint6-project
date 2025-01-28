from fastapi import Request
from elasticsearch import AsyncElasticsearch


async def get_elastic(request: Request) -> AsyncElasticsearch:
    return request.app.state.elastic

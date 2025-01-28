from fastapi import Depends
from elasticsearch import AsyncElasticsearch

from db.elastic import get_elastic
from services.base_service import BaseService


def service_for(service_name: str):
    """Возвращает FastAPI-зависимость, создающую нужный сервис."""
    
    def service_provider(elastic: AsyncElasticsearch = Depends(get_elastic)) -> BaseService:
        return BaseService.get_instance(service_name, elastic)
    
    return service_provider



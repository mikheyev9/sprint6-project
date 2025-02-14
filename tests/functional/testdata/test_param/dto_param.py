from abc import ABC
from typing import Dict, Type

from pydantic import BaseModel, ConfigDict


class Builder(ABC):
    __subclasses: Dict[str, Type['Builder']] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__subclasses[cls.__name__.lower()] = cls

    @classmethod
    def get_subclasses(cls):
        return cls.__subclasses


class AbstractDTO(BaseModel, Builder):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )

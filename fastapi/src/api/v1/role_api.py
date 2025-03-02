from typing import Annotated, List
from uuid import UUID

from src.schemas.response_schema import ResponseSchema
from src.schemas.role_schema import RoleCreate, RoleGetFull, RoleUpdate
from src.services.role_service import RoleService, get_role_service

from fastapi import APIRouter, Depends, Path

router = APIRouter()


@router.get("/all", response_model=List[RoleGetFull], summary="Get all roles", description="Get all roles")
async def get_all_roles(role_service: RoleService = Depends(get_role_service)) -> List[RoleGetFull]:
    return await role_service.get_all()


@router.post("/", response_model=RoleGetFull, summary="Create new role", description="Create new role")
async def create_role(role_data: RoleCreate, role_service: RoleService = Depends(get_role_service)) -> RoleGetFull:
    return await role_service.create(role_data)


@router.patch(
    "/{role_id}", response_model=RoleGetFull, summary="Update existing role", description="Update existing role"
)
async def update_role(
    role_id: Annotated[
        UUID,
        Path(
            title="role id",
            description="Role id for the item to search in the database",
        ),
    ],
    data: RoleUpdate,
    role_service: RoleService = Depends(get_role_service),
) -> RoleGetFull:
    return await role_service.update(role_id, data)


@router.delete(
    "/{role_id}", response_model=ResponseSchema, summary="Delete existing role", description="Delete existing role"
)
async def delete_role(
    role_id: Annotated[
        UUID,
        Path(
            title="role id",
            description="Role id for the item to search in the database",
        ),
    ],
    role_service: RoleService = Depends(get_role_service),
) -> ResponseSchema:
    await role_service.delete(role_id)
    return ResponseSchema(detail="Role deleted successfully")

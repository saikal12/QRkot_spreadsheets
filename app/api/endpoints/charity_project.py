from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validation import (check_before_delete,
                                          check_full_amount,
                                          check_name_duplicate,
                                          check_project_closed,
                                          check_project_exists,
                                          get_objs_investing)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import donation_investing

router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_project(session: AsyncSession = Depends(get_async_session)):
    project = await charity_project_crud.get_multi(session)
    return project


@router.post('/', response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)])
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    project = await charity_project_crud.create(project, session, commit=False)
    sourses = await get_objs_investing(project, session)
    commit_changes = donation_investing(project, sourses)
    session.add(commit_changes)
    await session.commit()
    await session.refresh(commit_changes)
    return commit_changes


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    await check_before_delete(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    project = await check_project_exists(project_id, session)
    await check_project_closed(project.fully_invested)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(obj_in.full_amount, project)
    project = await charity_project_crud.update(project, obj_in, session)
    return project

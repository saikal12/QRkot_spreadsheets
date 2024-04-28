from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityproject(
        CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]):

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        project = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date, CharityProject.create_date,
                CharityProject.description
            ).where(CharityProject.fully_invested is True).order_by(
                func.extract('epoch', CharityProject.close_date) -
                func.extract('epoch', CharityProject.create_date)
            )
        )
        return project.all()


charity_project_crud = CRUDCharityproject(CharityProject)

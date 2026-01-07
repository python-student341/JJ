from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from backend.models.models import VacancyModel, UserModel, Role
from backend.schemas.vacancy_schema import CreateVacancySchema, EditVacancySchema
from backend.database.database import session_dep
from backend.dependencies import get_user_token


router = APIRouter()


@router.post('/vacancy/create_vacancy', tags=['Vacancy'])
async def create_vacancy(data: CreateVacancySchema, session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.tenant:
        raise HTTPException(status_code=403, detail='Only tenants can make vacancies')

    new_vacancy = VacancyModel(
        tenant_id = current_user.id,
        title = data.title,
        compensation = data.compensation,
        city = data.city
    )

    session.add(new_vacancy)
    await session.commit()

    return {'success': True, 'message': 'Vacancy was created', 'Vacancy': new_vacancy}


@router.get('/vacancy/get_all_my_vacancies', tags=['Vacancy'])
async def get_all_my_vacancies(session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    vacancy_query = await session.execute(select(VacancyModel).where(VacancyModel.tenant_id == user_id))
    all_vacancies = vacancy_query.scalars().all()

    return {'success': True, 'Your vacancies': all_vacancies}


@router.put('/resume/edit_vacancy/{vacancy_id}', tags=['Vacancy'])
async def edit_vacancy(vacancy_id: int, session: session_dep, data: EditVacancySchema = Depends(), user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.tenant:
        raise HTTPException(status_code=403, detail='Only applicant can edit resume')

    query_vacancy = await session.execute(select(VacancyModel).where(VacancyModel.id == vacancy_id))
    current_vacancy = query_vacancy.scalar_one_or_none()

    if not current_vacancy:
        raise HTTPException(status_code=404, detail='Vacancy not found')

    if current_user.id != current_vacancy.tenant_id:
        raise HTTPException(status_code=403, detail="It's not your resume")

    if data.new_title:
        current_vacancy.title = data.new_title

    if data.new_city:
        current_vacancy.city = data.new_city

    if data.new_compensation:
        current_vacancy.compensation = data.new_compensation

    await session.commit()
    await session.refresh(current_vacancy)

    return {'success': True, 'message': 'Vacancy was edited'}


@router.delete('/vacancy/delete_vacancy/{vacancy_id}', tags=['Vacancy'])
async def delete_vacancy(vacancy_id: int, session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.tenant:
        raise HTTPException(status_code=403, detail='Only tenants can delete vacancy')

    query_vacancy = await session.execute(select(VacancyModel).where(VacancyModel.id == vacancy_id))
    current_vacancy = query_vacancy.scalar_one_or_none()

    if not current_vacancy:
        raise HTTPException(status_code=404, detail='Vacancy not found')

    if current_vacancy.tenant_id != current_user.id:
        raise HTTPException(status_code=403, detail='This is not your vacancy')

    await session.delete(current_vacancy)
    await session.commit()

    return {'success': True, 'message': 'Vacancy was deleted'}
from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy import select

from backend.models.models import UserModel, ResumeModel, Role
from backend.database.hash import security
from backend.database.database import session_dep
from backend.schemas.resume_schema import CreateResumeSchema, EditResumeSchema
from backend.dependencies import get_user_token


router = APIRouter()


@router.post('/resume/create_resume', tags=['Resume'])
async def create_resume(data: CreateResumeSchema, session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.applicant:
        raise HTTPException(status_code=403, detail='Only applicant can make resumes')

    new_resume = ResumeModel(
        applicant_id = current_user.id,
        title = data.title,
        about = data.about,
        city = data.city,
        stack = data.stack
    )

    session.add(new_resume)
    await session.commit()

    return {'success': True, 'message': 'Resume was created'}


@router.get('/resume/get_all_my_resumes', tags=['Resume'])
async def get_all_resumes(session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    resume_query = await session.execute(select(ResumeModel).where(ResumeModel.applicant_id == user_id))
    all_resumes = resume_query.scalars().all()

    return {'success': True, 'Your resumes': all_resumes}


@router.put('/resume/edit_resume/{resume_id}', tags=['Resume'])
async def edit_resume(resume_id: int, session: session_dep, data: EditResumeSchema = Depends(), user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.applicant:
        raise HTTPException(status_code=403, detail='Only applicant can edit resume')

    query_resume = await session.execute(select(ResumeModel).where(ResumeModel.id == resume_id))
    current_resume = query_resume.scalar_one_or_none()

    if not current_resume:
        raise HTTPException(status_code=404, detail='Resume not found')

    if current_user.id != current_resume.applicant_id:
        raise HTTPException(status_code=403, detail="It's not your resume")

    if data.new_title:
        current_resume.title = data.new_title

    if data.new_about:
        current_resume.about = data.new_about

    if data.new_city:
        current_resume.city = data.new_city

    if data.new_stack:
        current_resume.stack = data.new_stack

    await session.commit()
    await session.refresh(current_resume)

    return {'success': True, 'message': 'Resume was edited'}


@router.delete('/resume/delete_resume/{resume_id}', tags=['Resume'])
async def delete_resume(resume_id: int, session: session_dep, user_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    if current_user.role != Role.applicant:
        raise HTTPException(status_code=403, detail='Only applicant can edit resumes')

    resume_query = await session.execute(select(ResumeModel).where(ResumeModel.id == resume_id))
    current_resume = resume_query.scalar_one_or_none()

    if not current_resume:
        raise HTTPException(status_code=404, detail='Resume not found')

    if current_user.id != current_resume.applicant_id:
        raise HTTPException(status_code=403, detail='This is not your resume')

    await session.delete(current_resume)
    await session.commit()

    return {'success': True, 'message': 'Resume was deleted'}
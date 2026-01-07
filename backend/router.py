from fastapi import APIRouter

from backend.api.user_api import router as user_router
from backend.api.vacancy_api import router as vacancy_router
from backend.api.resume_api import router as resume_router
from backend.api.response_api import router as response_router
from backend.api.search_api import router as search_router
from backend.api.admin_api import router as admin_router


main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(vacancy_router)
main_router.include_router(resume_router)
main_router.include_router(response_router)
main_router.include_router(search_router)
main_router.include_router(admin_router)
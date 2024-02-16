import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.book_handlers import router as book_router
from api.admin_handlers import router as admin_router
from api.login_handlers import router as login_router


app = FastAPI(title="GetBooks")

main_api_router = APIRouter()

main_api_router.include_router(book_router, prefix='/book', tags=['book'])
main_api_router.include_router(admin_router, prefix='/admin', tags=['admin'])
main_api_router.include_router(login_router, prefix='/login', tags=['login'])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
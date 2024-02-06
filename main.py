import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.book_handlers import router as book_router


app = FastAPI(title="GetBooks")

main_api_router = APIRouter()

main_api_router.include_router(book_router, prefix='/book', tags=['book'])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, APIRouter

from apps.transactions.routers import router as transactions_router
from apps.users.routes import router as users_router
from db.settings import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
api_router = APIRouter(prefix="/api")
api_router.include_router(transactions_router)
api_router.include_router(users_router)
app.include_router(api_router)

from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"], responses={404: {"description": "Not found"}})
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from db import get_db
from apps.users import schemas, crud
from apps.users.details import USER_DETAIL_404, EMAIL_EXISTS_400

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


@router.get("/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_DETAIL_404)
    return db_user

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_EXISTS_400)
    return crud.create_user(db, user=user)

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: UUID, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_DETAIL_404)
    crud.update_user(db, user_id=user_id, data=data)
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_DETAIL_404)
    crud.delete_user(db, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

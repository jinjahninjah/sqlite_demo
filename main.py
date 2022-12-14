from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from schema import SchemaUser
from services import (get_db,
                      create_database,
                      create_user,
                      read_users,
                      read_first,
                      update_user,
                      delete_user)

from typing import List, Dict

from table_models import User

create_database()

app = FastAPI(
    title="Sqlite Demo",
    version="0.0.0",
    docs_url="/"
)


@app.get("/version/")
def version_endpoint():
    return {app.version}


@app.post("/create/user/", response_model=SchemaUser)
def create_user_endpoint(user: SchemaUser, db: Session = Depends(get_db)):
    user_check = read_first(db=db, profile_id=user.profile_id)
    if user_check:
        raise HTTPException(
            status_code=403,
            detail=f"Duplicate Entry, User {User.profile_id} already exists"
        )
    else:
        return create_user(db=db, user=user)


@app.get("/read-users/", response_model=List[SchemaUser])
def read_users_endpoint(db: Session = Depends(get_db)):
    return read_users(db=db)


@app.patch("/update/user/{profile_id}")
def update_users_endpoint(
        profile_id: str,
        update_data: Dict,
        db: Session = Depends(get_db)
):
    return update_user(profile_id=profile_id, update_data=update_data, db=db)


@app.delete("/delete/user/{profile_id}")
def delete_user_endpoint(profile_id: str, db: Session = Depends(get_db)):
    return delete_user(db=db, profile_id=profile_id)

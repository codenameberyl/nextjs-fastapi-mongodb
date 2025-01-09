from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ....dependencies import get_database
from ....schemas.user import UserCreate, UserInDB
from ....services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/register")
async def register(user: UserCreate, db=Depends(get_database)):
    # Check if user exists
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Hash the password
    hashed_password = auth_service.get_password_hash(user.password)

    # Create a new user document using UserInDB
    user_in_db = UserInDB(
        username=user.username,
        email=user.email,
        password=hashed_password,
        created_at=datetime.utcnow(),
    )

    # Convert the Pydantic model to a dictionary for insertion into MongoDB
    user_data = user_in_db.dict(
        by_alias=True, exclude={"id"}
    )  # `by_alias=True` converts `_id` to `id` and exclude `id` during insert
    result = await db.users.insert_one(user_data)

    return {
        "id": str(result.inserted_id),
        "username": user.username,
        "email": user.email,
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)
):
    # Find the user by username or email
    user = await get_user_by_username_or_email(form_data.username, db)
    if not user or not auth_service.verify_password(
        form_data.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Update the last_login field in the database
    db.users.update_one(
        {"_id": user.id}, {"$set": {"last_login": datetime.utcnow()}}
    )

    access_token = auth_service.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


async def get_user_by_username_or_email(username_or_email: str, db):
    user_data = await db.users.find_one(
        {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
    )
    if user_data:
        if "_id" in user_data:
            user_data["id"] = str(user_data["_id"])  # Convert ObjectId to string
            del user_data["_id"]  # Remove original ObjectId field
        return UserInDB(**user_data)
    return None

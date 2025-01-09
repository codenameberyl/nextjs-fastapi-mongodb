from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from .config import settings

security = HTTPBearer()
motor_client = None


async def get_database():
    return motor_client[settings.DATABASE_NAME]


async def connect_to_mongo():
    global motor_client
    motor_client = AsyncIOMotorClient(settings.DATABASE_URL)


async def close_mongo_connection():
    global motor_client
    if motor_client:
        motor_client.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
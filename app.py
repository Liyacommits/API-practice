from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid 
from app_.database import init_db, get_session
from app_.models import User, UserCreate, UserRead, patientRecord, UserLogin
from app_.auth import hash_password, create_access_token, verify_password, get_current_user, get_core_session

async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/users", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(get_session)):
    users = await session.exec(select(User))
    return users.all()

@app.post("/register")
async def register_user(data: UserCreate, session: AsyncSession = Depends(get_core_session)):
    existing = await session.exec(select(User).where(User.email == data.email))
    if existing.first():
        raise HTTPException(400, "Email already taken")

    user = User(
        id = str(uuid.uuid4()),
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
        is_superuser=True if data.role.lower()=="doctor" else False
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "User created", "id": user.id}


@app.post("/login")
async def login_user(data: UserLogin, session: AsyncSession = Depends(get_core_session)):
    query = await session.exec(select(User).where(User.email == data.email))
    user = query.first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user
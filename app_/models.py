from sqlmodel import SQLModel, Field
import uuid

class User(SQLModel, table=True):
    id: str = Field(default=lambda: str(uuid.uuid4()), primary_key=True, index=True, nullable=False)
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    role : str
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    role: str

class UserRead(SQLModel):
    id: str
    name: str
    email: str
    role: str
    is_superuser: bool

class UserLogin(SQLModel):
    email: str
    password: str

class patientRecord(SQLModel, table=True):
    id: str = Field(default=lambda: str(uuid.uuid4()), primary_key=True, index=True, nullable=False)
    user_id: str = Field(foreign_key="user.id")
    medical_history: str
    medications: str

    
    

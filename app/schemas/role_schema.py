from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str]
    is_system_role: bool = False
    is_active: bool = True

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_system_role: Optional[bool] = None
    is_active: Optional[bool] = None

class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


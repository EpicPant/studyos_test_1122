from pydantic import BaseModel

class ModuleBase(BaseModel):
    name: str

class ModuleCreate(ModuleBase):
    sphere_id: int

    class Config:
        orm_mode = True

class ModuleFilter(BaseModel):
    sphere_id: int

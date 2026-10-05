from pydantic import BaseModel
from typing import Optional, Literal

class MasterdataCreate(BaseModel):
    name: str
    parentId: Optional[int] = None
    brandId: Optional[int] = None
    type: Literal[1, 2]
    status: Optional[bool] = True
    summary: Optional[str] = None
    description: Optional[str] = None

class MasterdataOut(MasterdataCreate):
    product_code: str
    id: int

    model_config = {
        "from_attributes": True
    }

class UpdateMasterdata(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    brand_id: Optional[int] = None
    status: Optional[bool] = None
    summary: Optional[str] = None
    description: Optional[str] = None

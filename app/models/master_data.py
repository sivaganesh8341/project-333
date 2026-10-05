from sqlalchemy import Column, Integer, Boolean, String
from app.database.base_class import Base


class MasterData(Base):
    __tablename__ = "masterdata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    product_code = Column(String(15), nullable=False, unique=True, index=True)
    parent_id = Column(Integer, nullable=True)
    brand_id = Column(Integer, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    type = Column(Integer, nullable=False)
    summary = Column(String(255), nullable=True)
    Description = Column(String(255), nullable=True)

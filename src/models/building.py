from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.orm import relationship

from database import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")

from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    cards = relationship("Card", back_populates="section", cascade="all, delete")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    commission = Column(Numeric(10, 2))
    promo_code = Column(String)
    discount_start = Column(Date)
    discount_end = Column(Date)

    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="cards")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

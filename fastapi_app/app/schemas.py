from datetime import date, datetime
from pydantic import BaseModel, model_validator, Field


# ---------- SECTIONS ----------
class SectionCreate(BaseModel):
    title: str = Field(..., min_length=1, strip_whitespace=True)


class SectionOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class SectionUpdate(BaseModel):
    title: str = Field(..., min_length=1, strip_whitespace=True)

# ---------- CARDS ----------
class CardCreate(BaseModel):
    title: str = Field(..., min_length=1, strip_whitespace=True)
    company_name: str = Field(..., min_length=1, strip_whitespace=True)
    commission: float
    promo_code: str | None = None
    discount_start: date
    discount_end: date
    section_id: int

    @model_validator(mode='after')
    def validate_dates(self):
        today = date.today()

        # Проверка: дата окончания не в прошлом
        if self.discount_end < today:
            raise ValueError("Дата окончания не может быть в прошлом")

        # Проверка: окончание >= начала
        if self.discount_end < self.discount_start:
            raise ValueError("Дата окончания не может быть раньше даты начала")

        return self

    @model_validator(mode='after')
    def validate_commission(self):
        if self.commission < 0:
            raise ValueError("Скидка не может быть отрицательной")
        return self


class CardUpdate(CardCreate):
    pass


class CardOut(CardCreate):
    id: int

    class Config:
        from_attributes = True
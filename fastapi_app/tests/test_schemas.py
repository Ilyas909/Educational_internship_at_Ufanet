# tests/test_schemas.py
import pytest
from datetime import date, timedelta
from app.schemas import CardCreate

def test_negative_commission():
    with pytest.raises(ValueError):
        CardCreate(
            title="Test",
            company_name="Test",
            commission=-1,
            promo_code=None,
            discount_start=date.today(),
            discount_end=date.today() + timedelta(days=1),
            section_id=1
        )


def test_end_date_before_start():
    with pytest.raises(ValueError):
        CardCreate(
            title="Test",
            company_name="Test",
            commission=5,
            promo_code=None,
            discount_start=date.today(),
            discount_end=date.today() - timedelta(days=1),
            section_id=1
        )


def test_end_date_before_start2():
    with pytest.raises(ValueError):
        CardCreate(
            title="Test",
            company_name="Test",
            commission=5,
            promo_code=None,
            discount_start=date.today() + timedelta(days=5),
            discount_end=date.today() + timedelta(days=1),
            section_id=1
        )
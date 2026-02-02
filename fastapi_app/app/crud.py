from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import schemas
from app.models import Section, Card


# ---------- SECTIONS ----------

async def get_sections(db: AsyncSession):
    result = await db.execute(select(Section))
    return result.scalars().all()


async def create_section(db: AsyncSession, title: str):
    section = Section(title=title)
    db.add(section)
    await db.commit()
    await db.refresh(section)
    return section


async def update_section(db: AsyncSession, section_id: int, title: str):
    section = await db.get(Section, section_id)
    if not section:
        return None

    section.title = title
    await db.commit()
    await db.refresh(section)
    return section



async def delete_section(db: AsyncSession, section_id: int):
    section = await db.get(Section, section_id)
    if section:
        await db.delete(section)
        await db.commit()


# ---------- CARDS ----------

async def get_cards_by_section(db: AsyncSession, section_id: int):
    result = await db.execute(
        select(Card).where(Card.section_id == section_id)
    )
    return result.scalars().all()


async def get_section_by_id(db: AsyncSession, section_id: int):
    return await db.get(Section, section_id)


async def create_card(db: AsyncSession, card_data: schemas.CardCreate):
    card = Card(
        title=card_data.title,
        company_name=card_data.company_name,
        commission=card_data.commission,
        promo_code=card_data.promo_code,
        discount_start=card_data.discount_start,
        discount_end=card_data.discount_end,
        section_id=card_data.section_id
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card


async def update_card(db: AsyncSession, card_id: int, card_data: schemas.CardUpdate):
    card = await db.get(Card, card_id)
    if not card:
        return None

    # Обновляем поля явно
    card.title = card_data.title
    card.company_name = card_data.company_name
    card.commission = card_data.commission
    card.promo_code = card_data.promo_code
    card.discount_start = card_data.discount_start
    card.discount_end = card_data.discount_end
    card.section_id = card_data.section_id

    await db.commit()
    await db.refresh(card)
    return card


async def delete_card(db: AsyncSession, card_id: int):
    card = await db.get(Card, card_id)
    if card:
        await db.delete(card)
        await db.commit()



async def get_card_by_id(db: AsyncSession, card_id: int):
    return await db.get(Card, card_id)

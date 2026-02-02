from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.get("/section/{section_id}", response_model=list[schemas.CardOut])
async def list_cards(section_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_cards_by_section(db, section_id)


@router.post("", response_model=schemas.CardOut)
async def add_card(data: schemas.CardCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли секция
    section_exists = await crud.get_section_by_id(db, data.section_id)
    if not section_exists:
        raise HTTPException(status_code=400, detail="Section not found")

    return await crud.create_card(db, data)


@router.put("/{card_id}", response_model=schemas.CardOut)
async def edit_card(
    card_id: int,
    data: schemas.CardUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_card(db, card_id, data)


@router.delete("/{card_id}")
async def remove_card(card_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_card(db, card_id)
    return {"status": "ok"}


@router.get("/{card_id}", response_model=schemas.CardOut)
async def get_card(card_id: int, db: AsyncSession = Depends(get_db)):
    card = await crud.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
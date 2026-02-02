from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app import crud
from app.schemas import SectionCreate, SectionOut, SectionUpdate

router = APIRouter(prefix="/api/sections", tags=["Sections"])


@router.get("", response_model=list[SectionOut])
async def get_sections(db: AsyncSession = Depends(get_db)):
    return await crud.get_sections(db)


@router.post("", response_model=SectionOut)
async def create_section(
    section: SectionCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_section(db, section.title)


@router.put("/{section_id}", response_model=SectionOut)
async def update_section(
    section_id: int,
    data: SectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    section = await crud.update_section(db, section_id, data.title)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.delete("/{section_id}")
async def delete_section(
    section_id: int,
    db: AsyncSession = Depends(get_db)
):
    await crud.delete_section(db, section_id)
    return {"status": "ok"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import api_sections, api_cards
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Partners Admin API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_sections.router)
app.include_router(api_cards.router)

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "sections.html",
        {"request": request}
    )


@app.get("/sections/{section_id}")
def section_cards_page(request: Request, section_id: int):
    return templates.TemplateResponse(
        "cards.html",
        {
            "request": request,
            "section_id": section_id
        }
    )


# Public routes
@app.get("/public")
def public_home(request: Request):
    return templates.TemplateResponse("public_sections.html", {"request": request})

@app.get("/public/sections/{section_id}")
def public_section_cards(request: Request, section_id: int):
    return templates.TemplateResponse("public_cards.html", {
        "request": request,
        "section_id": section_id
    })

@app.get("/public/cards/{card_id}")
def public_card_detail(request: Request, card_id: int):
    return templates.TemplateResponse("public_card_detail.html", {
        "request": request,
        "card_id": card_id
    })
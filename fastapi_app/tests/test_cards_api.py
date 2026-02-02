from datetime import date, timedelta
import pytest

@pytest.mark.asyncio
async def test_create_card(client, prepare_database):
    section = await client.post("/api/sections", json={"title": "Магазины"})
    section_id = section.json()["id"]

    payload = {
        "title": "Скидка 10%",
        "company_name": "DNS",
        "commission": 10,
        "promo_code": "DNS10",
        "discount_start": str(date.today()),
        "discount_end": str(date.today() + timedelta(days=10)),
        "section_id": section_id
    }

    res = await client.post("/api/cards", json=payload)
    assert res.status_code == 200
    assert res.json()["company_name"] == "DNS"


@pytest.mark.asyncio
async def test_create_card2(client, prepare_database):
    payload = {
        "title": "Скидка 10%",
        "company_name": "DNS",
        "commission": 10,
        "promo_code": "DNS10",
        "discount_start": str(date.today()),
        "discount_end": str(date.today() + timedelta(days=10)),
        "section_id": 99
    }

    res = await client.post("/api/cards", json=payload)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_get_cards_by_section(client, prepare_database):
    res = await client.get("/api/cards/section/1")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_update_card(client, prepare_database):
    section = await client.post("/api/sections", json={"title": "Аптеки"})
    section_id = section.json()["id"]

    create = await client.post("/api/cards", json={
        "title": "Скидка",
        "company_name": "36.6",
        "commission": 5,
        "promo_code": None,
        "discount_start": str(date.today()),
        "discount_end": str(date.today() + timedelta(days=5)),
        "section_id": section_id
    })

    card_id = create.json()["id"]

    res = await client.put(f"/api/cards/{card_id}", json={
        "title": "Скидка 7%",
        "company_name": "36.6",
        "commission": 7,
        "promo_code": "SALE",
        "discount_start": str(date.today()),
        "discount_end": str(date.today() + timedelta(days=7)),
        "section_id": section_id
    })

    assert res.status_code == 200
    assert res.json()["commission"] == 7


@pytest.mark.asyncio
async def test_delete_card(client, prepare_database):
    section = await client.post("/api/sections", json={"title": "Техника"})
    section_id = section.json()["id"]

    card = await client.post("/api/cards", json={
        "title": "SALE",
        "company_name": "MVideo",
        "commission": 15,
        "promo_code": None,
        "discount_start": str(date.today()),
        "discount_end": str(date.today() + timedelta(days=3)),
        "section_id": section_id
    })

    card_id = card.json()["id"]

    res = await client.delete(f"/api/cards/{card_id}")
    assert res.status_code == 200

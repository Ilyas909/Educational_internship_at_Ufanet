# tests/test_sections_api.py
import pytest

@pytest.mark.asyncio
async def test_create_section(client, prepare_database):
    res = await client.post("/api/sections", json={"title": "Еда"})
    assert res.status_code == 200
    assert res.json()["title"] == "Еда"


@pytest.mark.asyncio
async def test_get_sections(client, prepare_database):
    res = await client.get("/api/sections")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_update_section(client, prepare_database):
    create = await client.post("/api/sections", json={"title": "Старое"})
    section_id = create.json()["id"]

    res = await client.put(
        f"/api/sections/{section_id}",
        json={"title": "Новое"}
    )

    assert res.status_code == 200
    assert res.json()["title"] == "Новое"


@pytest.mark.asyncio
async def test_delete_section(client, prepare_database):
    create = await client.post("/api/sections", json={"title": "Удалить"})
    section_id = create.json()["id"]

    res = await client.delete(f"/api/sections/{section_id}")
    assert res.status_code == 200

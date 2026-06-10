import pytest
from httpx import AsyncClient


@pytest.fixture
async def usuario_id(client: AsyncClient) -> int:
    res = await client.post(
        "/api/usuarios/", json={"nombre": "T", "mail": "td@t.com", "password": "p"}
    )
    return res.json()["id"]


@pytest.fixture
async def objetivo_id(client: AsyncClient, usuario_id: int) -> int:
    res = await client.post(
        "/api/objetivos/", json={"nombre": "Objetivo", "usuario_id": usuario_id}
    )
    return res.json()["id"]


@pytest.mark.asyncio
async def test_crear_descripcion(client: AsyncClient, objetivo_id: int):
    response = await client.post(
        "/api/descripciones/",
        json={
            "feria": "Feria de Coleccionistas",
            "local": "Puesto 5",
            "moneda": "PESOS",
            "precio": 15000.0,
            "objetivo_id": objetivo_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["feria"] == "Feria de Coleccionistas"
    assert data["precio"] == 15000.0
    assert data["objetivo_id"] == objetivo_id


@pytest.mark.asyncio
async def test_listar_descripciones_de_objetivo(client: AsyncClient, objetivo_id: int):
    await client.post(
        "/api/descripciones/",
        json={
            "feria": "F1",
            "local": "L1",
            "moneda": "PESOS",
            "precio": 100,
            "objetivo_id": objetivo_id,
        },
    )
    await client.post(
        "/api/descripciones/",
        json={
            "feria": "F2",
            "local": "L2",
            "moneda": "DOLARES",
            "precio": 50,
            "objetivo_id": objetivo_id,
        },
    )
    response = await client.get(f"/api/objetivos/{objetivo_id}/descripciones")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_eliminar_descripcion(client: AsyncClient, objetivo_id: int):
    res = await client.post(
        "/api/descripciones/",
        json={
            "feria": "F",
            "local": "L",
            "moneda": "PESOS",
            "precio": 100,
            "objetivo_id": objetivo_id,
        },
    )
    did = res.json()["id"]
    response = await client.delete(f"/api/descripciones/{did}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_obtener_descripcion_404(client: AsyncClient):
    response = await client.get("/api/descripciones/9999")
    assert response.status_code == 404

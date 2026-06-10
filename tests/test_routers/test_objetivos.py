import pytest
from httpx import AsyncClient


@pytest.fixture
async def usuario_id(client: AsyncClient) -> int:
    res = await client.post(
        "/api/usuarios/", json={"nombre": "T", "mail": "t@t.com", "password": "p"}
    )
    return res.json()["id"]


@pytest.mark.asyncio
async def test_crear_objetivo(client: AsyncClient, usuario_id: int):
    response = await client.post(
        "/api/objetivos/", json={"nombre": "Mi objetivo", "usuario_id": usuario_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Mi objetivo"
    assert data["usuario_id"] == usuario_id


@pytest.mark.asyncio
async def test_listar_objetivos_por_usuario(client: AsyncClient, usuario_id: int):
    await client.post("/api/objetivos/", json={"nombre": "O1", "usuario_id": usuario_id})
    await client.post("/api/objetivos/", json={"nombre": "O2", "usuario_id": usuario_id})
    response = await client.get(f"/api/objetivos/?usuario_id={usuario_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_actualizar_objetivo(client: AsyncClient, usuario_id: int):
    res = await client.post("/api/objetivos/", json={"nombre": "Viejo", "usuario_id": usuario_id})
    oid = res.json()["id"]
    response = await client.put(f"/api/objetivos/{oid}", json={"nombre": "Nuevo"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Nuevo"


@pytest.mark.asyncio
async def test_eliminar_objetivo(client: AsyncClient, usuario_id: int):
    res = await client.post("/api/objetivos/", json={"nombre": "Del", "usuario_id": usuario_id})
    oid = res.json()["id"]
    response = await client.delete(f"/api/objetivos/{oid}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_obtener_objetivo_404(client: AsyncClient):
    response = await client.get("/api/objetivos/9999")
    assert response.status_code == 404

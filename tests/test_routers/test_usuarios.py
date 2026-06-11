import pytest
from httpx import AsyncClient


# @pytest.mark.asyncio: marca el test como asíncrono para que pytest lo ejecute
# sobre un event loop de asyncio.
# AsyncClient: cliente HTTP asíncrono de httpx para enviar requests sin servidor real.
@pytest.mark.asyncio
async def test_crear_usuario(client: AsyncClient):
    response = await client.post(
        "/api/usuarios/",
        json={"nombre": "Test User", "mail": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Test User"
    assert data["mail"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_crear_usuario_duplicado(client: AsyncClient):
    payload = {"nombre": "Test", "mail": "dupe@example.com", "password": "secret"}
    await client.post("/api/usuarios/", json=payload)
    response = await client.post("/api/usuarios/", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_listar_usuarios(client: AsyncClient):
    await client.post("/api/usuarios/", json={"nombre": "A", "mail": "a@b.com", "password": "x"})
    await client.post("/api/usuarios/", json={"nombre": "B", "mail": "b@b.com", "password": "x"})
    response = await client.get("/api/usuarios/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_obtener_usuario(client: AsyncClient):
    res = await client.post(
        "/api/usuarios/", json={"nombre": "X", "mail": "x@y.com", "password": "p"}
    )
    uid = res.json()["id"]
    response = await client.get(f"/api/usuarios/{uid}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "X"


@pytest.mark.asyncio
async def test_obtener_usuario_404(client: AsyncClient):
    response = await client.get("/api/usuarios/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_eliminar_usuario(client: AsyncClient):
    res = await client.post(
        "/api/usuarios/", json={"nombre": "X", "mail": "del@x.com", "password": "p"}
    )
    uid = res.json()["id"]
    response = await client.delete(f"/api/usuarios/{uid}")
    assert response.status_code == 204
    response = await client.get(f"/api/usuarios/{uid}")
    assert response.status_code == 404

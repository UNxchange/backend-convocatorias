
import pytest
import sys
import os
from httpx import AsyncClient
from fastapi import status
from bson import ObjectId

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main app object and other necessary components
from app.main import app
from app.database import get_convocatoria_collection
from app.security import create_access_token

# --- Test Setup and Fixtures ---

@pytest.fixture(scope="module")
def admin_token():
    return create_access_token({"sub": "admin@example.com", "role": "administrador"})

@pytest.fixture(scope="module")
def normal_user_token():
    return create_access_token({"sub": "user@example.com", "role": "usuario"})

@pytest.fixture(autouse=True)
async def setup_and_teardown_db():
    # Setup: Ensure the collection is clean before each test
    collection = get_convocatoria_collection()
    await collection.delete_many({})
    yield
    # Teardown: Clean up the collection after each test
    await collection.delete_many({})


# --- Test Cases ---

# --- POST /convocatorias/ ---

@pytest.mark.asyncio
async def test_create_convocatoria_admin(admin_token):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/convocatorias/",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "subscriptionYear": "2025",
                "country": "Test Country",
                "institution": "Test Institution",
                "agreementType": "Test Agreement",
                "validity": "2025-12-31",
                "subscriptionLevel": "Test Level",
            },
        )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["country"] == "Test Country"
    assert "_id" in data

@pytest.mark.asyncio
async def test_create_convocatoria_normal_user(normal_user_token):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/convocatorias/",
            headers={"Authorization": f"Bearer {normal_user_token}"},
            json={
                "subscriptionYear": "2025",
                "country": "Test Country",
                "institution": "Test Institution",
                "agreementType": "Test Agreement",
                "validity": "2025-12-31",
                "subscriptionLevel": "Test Level",
            },
        )
    assert response.status_code == status.HTTP_403_FORBIDDEN

# --- GET /convocatorias/ ---

@pytest.mark.asyncio
async def test_get_convocatorias_authenticated(normal_user_token):
    # First, create a convocatoria to be retrieved
    collection = get_convocatoria_collection()
    await collection.insert_one({
        "subscriptionYear": "2025",
        "country": "Test Country",
        "institution": "Test Institution",
        "agreementType": "Test Agreement",
        "validity": "2025-12-31",
        "state": "Vigente",
        "subscriptionLevel": "Test Level",
        "languages": ["English"],
    })

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/convocatorias/",
            headers={"Authorization": f"Bearer {normal_user_token}"},
        )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["country"] == "Test Country"


@pytest.mark.asyncio
async def test_get_convocatorias_unauthenticated():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/convocatorias/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# --- GET /convocatorias/{id} ---

@pytest.mark.asyncio
async def test_get_convocatoria_by_id(normal_user_token):
    collection = get_convocatoria_collection()
    result = await collection.insert_one({"country": "Find Me"})
    convocatoria_id = str(result.inserted_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/convocatorias/{convocatoria_id}",
            headers={"Authorization": f"Bearer {normal_user_token}"},
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["country"] == "Find Me"

# --- PATCH /convocatorias/{id} ---

@pytest.mark.asyncio
async def test_update_convocatoria_admin(admin_token):
    collection = get_convocatoria_collection()
    result = await collection.insert_one({"country": "Original"})
    convocatoria_id = str(result.inserted_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(
            f"/convocatorias/{convocatoria_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"country": "Updated"},
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["country"] == "Updated"

# --- DELETE /convocatorias/{id} ---

@pytest.mark.asyncio
async def test_delete_convocatoria_admin(admin_token):
    collection = get_convocatoria_collection()
    result = await collection.insert_one({"country": "To Delete"})
    convocatoria_id = str(result.inserted_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/convocatorias/{convocatoria_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
    assert response.status_code == status.HTTP_204_NO_CONTENT



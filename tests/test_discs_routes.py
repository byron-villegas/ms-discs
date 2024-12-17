import random
import pytest

from app import create_app
from app.discs.service import get_discs


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_get_discs(client):
    response = client.get("/api/discs")
    assert response.status_code == 200

def test_get_disc_by_sku(app, client):
    with app.app_context():
        disc = get_discs()[0]
        sku = str( disc["sku"])
        response = client.get("/api/discs/" + sku)
        assert response.status_code == 200

def test_save_disc(app, client):
    with app.app_context():
        disc = get_discs()[0]
        disc["sku"] = random.randint(2000, 3000)
        response = client.post("/api/dics", json=disc)
        assert response.status_code == 200
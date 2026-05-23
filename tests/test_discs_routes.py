import random

import pytest

from app import create_app
from app.discs.models import Disc


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def sample_disc():
    return Disc(
        sku="1",
        name="Disc 1",
        description="Desc 1",
        author="Author A",
        yearCreated=2020,
        type="CDS",
    )


def test_get_discs(client, monkeypatch, sample_disc):
    from app.discs import routes

    monkeypatch.setattr(
        routes.service,
        "get_filtered_discs",
        lambda type_value=None, favorite=False, page=1, size=10: {
            "items": [sample_disc.model_dump()],
            "page": page,
            "size": size,
            "totalItems": 1,
            "totalPages": 1,
        },
    )

    response = client.get("/api/discs")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["items"] == [sample_disc.model_dump()]
    assert payload["page"] == 1
    assert payload["size"] == 10


def test_get_discs_with_pagination(client, monkeypatch, sample_disc):
    from app.discs import routes

    monkeypatch.setattr(
        routes.service,
        "get_filtered_discs",
        lambda type_value=None, favorite=False, page=1, size=10: {
            "items": [sample_disc.model_dump()],
            "page": page,
            "size": size,
            "totalItems": 1,
            "totalPages": 1,
        },
    )

    response = client.get("/api/discs?page=2&size=5")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["page"] == 2
    assert payload["size"] == 5


def test_get_discs_combined_filters(client, monkeypatch, sample_disc):
    from app.discs import routes

    captured = {}

    def fake_get_filtered_discs(type_value=None, favorite=False, page=1, size=10):
        captured["type_value"] = type_value
        captured["favorite"] = favorite
        captured["page"] = page
        captured["size"] = size
        return {
            "items": [sample_disc.model_dump()],
            "page": page,
            "size": size,
            "totalItems": 1,
            "totalPages": 1,
        }

    monkeypatch.setattr(routes.service, "get_filtered_discs", fake_get_filtered_discs)

    response = client.get("/api/discs?type=cds&favorite=true&page=3&size=7")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["page"] == 3
    assert payload["size"] == 7
    assert captured["type_value"] == "CDS"
    assert captured["favorite"] is True
    assert captured["page"] == 3
    assert captured["size"] == 7


def test_get_discs_favorite_false_does_not_filter(client, monkeypatch, sample_disc):
    from app.discs import routes

    captured = {}

    def fake_get_filtered_discs(type_value=None, favorite=False, page=1, size=10):
        captured["type_value"] = type_value
        captured["favorite"] = favorite
        captured["page"] = page
        captured["size"] = size
        return {
            "items": [sample_disc.model_dump()],
            "page": page,
            "size": size,
            "totalItems": 1,
            "totalPages": 1,
        }

    monkeypatch.setattr(routes.service, "get_filtered_discs", fake_get_filtered_discs)

    response = client.get("/api/discs?favorite=false")
    assert response.status_code == 200

    assert captured["favorite"] is False


def test_get_discs_invalid_favorite(client):
    response = client.get("/api/discs?favorite=maybe")
    assert response.status_code == 400


def test_get_discs_invalid_page(client):
    response = client.get("/api/discs?page=0")
    assert response.status_code == 400


def test_get_disc_by_sku(client, monkeypatch, sample_disc):
    from app.discs import routes

    monkeypatch.setattr(routes.service, "find_by_sku", lambda sku: sample_disc.model_dump())

    response = client.get("/api/discs/1")
    assert response.status_code == 200


def test_save_disc(client, monkeypatch, sample_disc):
    from app.discs import routes

    monkeypatch.setattr(routes.service, "save_disc", lambda disc: sample_disc)

    disc = sample_disc.model_dump()
    disc["sku"] = str(random.randint(2000, 3000))
    response = client.post("/api/discs", json=disc)
    assert response.status_code == 200
import random

import pytest

from app import create_app
from app.discs.models import Disc
from app.discs.service import find_by_sku, get_discs, save_disc
from app.exceptions.error_negocio_exception import ErrorNegocioException


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def sample_discs():
    return [
        Disc(
            sku="1",
            name="Disc 1",
            description="Desc 1",
            author="Author A",
            yearCreated=2020,
            type="CDS",
        ),
        Disc(
            sku="2",
            name="Disc 2",
            description="Desc 2",
            author="Author B",
            yearCreated=2021,
            type="VINYLS",
        ),
    ]


def test_get_products(app, monkeypatch, sample_discs):
    from app.discs import service

    monkeypatch.setattr(service.repository, "find_discs", lambda type_value, favorite, page, size: (sample_discs, 2))

    with app.app_context():
        products = get_discs()

        assert products["items"] == [disc.model_dump() for disc in sample_discs]
        assert products["page"] == 1
        assert products["size"] == 10
        assert products["totalItems"] == 2
        assert products["totalPages"] == 1


def test_get_filtered_products(app, monkeypatch, sample_discs):
    from app.discs import service

    captured = {}

    def fake_find_discs(type_value, favorite, page, size):
        captured["type_value"] = type_value
        captured["favorite"] = favorite
        captured["page"] = page
        captured["size"] = size
        return sample_discs, 2

    monkeypatch.setattr(service.repository, "find_discs", fake_find_discs)

    with app.app_context():
        products = service.get_filtered_discs("CDS", True, 2, 5)

        assert products["items"] == [disc.model_dump() for disc in sample_discs]
        assert captured["type_value"] == "CDS"
        assert captured["favorite"] is True
        assert captured["page"] == 2
        assert captured["size"] == 5


def test_get_product_by_sku(app, monkeypatch, sample_discs):
    from app.discs import service

    monkeypatch.setattr(service.repository, "find_by_sku", lambda sku: sample_discs[0])

    with app.app_context():
        product = find_by_sku("1")

        assert product is not None


def test_get_product_by_sku_not_found(app, monkeypatch):
    from app.discs import service

    monkeypatch.setattr(service.repository, "find_by_sku", lambda sku: None)

    with app.app_context():
        with pytest.raises(ErrorNegocioException, match="Disco no encontrado"):
            find_by_sku(21)


def test_save_product(app, monkeypatch, sample_discs):
    from app.discs import service

    monkeypatch.setattr(service.repository, "find_by_sku", lambda sku: None)
    saved = {}

    def fake_save(disc):
        saved["disc"] = disc

    monkeypatch.setattr(service.repository, "save", fake_save)

    with app.app_context():
        product = sample_discs[0].model_dump()
        product["sku"] = str(random.randint(1, 1000))
        save_disc(product)

        assert saved["disc"]["sku"] == product["sku"]


def test_save_product_exists(app, monkeypatch, sample_discs):
    from app.discs import service

    monkeypatch.setattr(service.repository, "find_by_sku", lambda sku: sample_discs[0])

    with app.app_context():
        product = sample_discs[0].model_dump()
        with pytest.raises(ErrorNegocioException, match="Disco ya existe"):
            save_disc(product)
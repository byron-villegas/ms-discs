import random
import pytest

from app import create_app
from app.exceptions.error_negocio_exception import ErrorNegocioException
from app.exceptions.error_tecnico_exception import ErrorTecnicoException
from app.discs.service import find_by_sku, get_discs, save_disc


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

def test_get_products(app):
    with app.app_context():
        products = get_discs()

        assert products is not None

def test_get_product_by_sku(app):
        with app.app_context():
            products = get_discs()
            product = find_by_sku(products[0]["sku"])

            assert product is not None

def test_get_product_by_sku_not_found(app):
        with app.app_context():
            with pytest.raises(ErrorTecnicoException, match="Producto no encontrado"):
                find_by_sku(21)

def test_save_product(app):
        with app.app_context(): 
            products = get_discs()
            product = products[0]
            product["sku"] = random.randint(1, 1000) 
            save_disc(product)
            assert len(get_discs()) != products

def test_save_product_exists(app):
        with app.app_context(): 
            products = get_discs()
            product = products[0]
            with pytest.raises(ErrorNegocioException, match="Producto ya existe"):
                save_disc(product)
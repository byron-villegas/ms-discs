
from http.client import HTTPException
import re

from flask import Response, abort, jsonify, make_response
from app.exceptions.error_negocio_exception import ErrorNegocioException
from app.discs import repository

def get_discs():
    discs = repository.find_all()

    return discs

def get_discs_by_type(type: str):
    pattern = re.compile(r"[A-Za-z0-9]+")

    if not re.fullmatch(pattern, type):
        abort(make_response(jsonify({"type": "Solo admite letras y numeros"}), 400))

    discs = repository.find_by_type(type)

    return discs

def get_favorite_discs():

    discs = repository.find_favorite()

    return discs

def find_by_sku(sku: str):
    disc = repository.find_by_sku(sku)

    if disc is None:
        raise ErrorNegocioException("EXDNE01", "Disco no encontrado")

    return disc

def save_disc(disc):
    disc = repository.find_by_sku(disc.sku)

    if disc is not None:
        raise ErrorNegocioException("EXDYE01", "Disco ya existe")
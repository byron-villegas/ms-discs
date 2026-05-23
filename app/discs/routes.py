from flask import jsonify, request
from app.discs import bp
from app.discs import service
from flask import Response
from flasgger import swag_from
from pydantic import ValidationError


def _parse_positive_int(param_name: str, default: int):
    raw_value = request.args.get(param_name)

    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError:
        return None


def _parse_bool(param_name: str):
    raw_value = request.args.get(param_name)

    if raw_value is None:
        return False, True

    normalized_value = raw_value.strip().lower()

    if normalized_value in ("true", "1", "yes", "on"):
        return True, True

    if normalized_value in ("false", "0", "no", "off"):
        return False, True

    return False, False


def _parse_order(param_name: str = "order"):
    raw_value = request.args.get(param_name)

    if raw_value is None:
        return "author", 1, True

    normalized_value = raw_value.strip().lower()

    if not normalized_value:
        return "", 1, False

    direction = 1

    if normalized_value.endswith("-"):
        normalized_value = normalized_value[:-1]
        direction = -1
    elif normalized_value.endswith("+"):
        normalized_value = normalized_value[:-1]
    elif raw_value.endswith(" "):
        # Flask decodifica '+' sin escapar como espacio en query params.
        direction = 1

    if normalized_value in ("name", "author", "year"):
        return normalized_value, direction, True

    return "", direction, False


@bp.route("/discs", methods=["GET"])
def get_discs():
    """
    Obtener lista de discos
    ---
    tags:
      - Discs
    summary: Obtener lista de discos
    description: Retorna todos los discos habilitados. Puede filtrar por tipo, favoritos o combinar ambos filtros
    parameters:
      - name: type
        in: query
        description: Filtrar por tipo de disco (cds, vinyls, cassettes)
        required: false
        schema:
          type: string
          pattern: ^[A-Za-z0-9]+$
        example: cds
      - name: favorite
        in: query
        description: Filtrar solo discos favoritos. Usa false para no aplicar el filtro.
        required: false
        schema:
          type: boolean
          default: false
        example: true
      - name: page
        in: query
        description: Número de página, inicia en 1
        required: false
        schema:
          type: integer
          minimum: 1
        example: 1
      - name: size
        in: query
        description: Cantidad de resultados por página
        required: false
        schema:
          type: integer
          minimum: 1
        example: 15
      - name: order
        in: query
        description: Orden por campo y dirección. Usa name+, name-, author+, author-, year+, year-
        required: false
        schema:
          type: string
          pattern: ^(name|author|year)(\\+|-)$
        example: author+
    responses:
      200:
        description: Lista paginada de discos obtenida exitosamente
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                $ref: '#/definitions/Disc'
            page:
              type: integer
              example: 1
            size:
              type: integer
              example: 10
            totalItems:
              type: integer
              example: 25
            totalPages:
              type: integer
              example: 3
          required:
            - items
            - page
            - size
            - totalItems
            - totalPages
      400:
        description: Error de validación
        schema:
          type: object
          properties:
            type:
              type: string
              example: "Solo admite letras y numeros"
    """
    type = request.args.get('type', None)
    page = _parse_positive_int('page', 1)
    size = _parse_positive_int('size', 15)
    favorite_enabled, favorite_valid = _parse_bool('favorite')
    order_field, order_direction, order_valid = _parse_order('order')

    if page is None or size is None:
        return jsonify({"page": "page y size deben ser enteros positivos"}), 400

    if page < 1 or size < 1:
        return jsonify({"page": "page y size deben ser mayores que cero"}), 400

    if not favorite_valid:
      return jsonify({"favorite": "favorite debe ser true o false"}), 400

    if not order_valid:
      return jsonify({"order": "order debe ser name+, name-, author+, author-, year+ o year-"}), 400

    discs = service.get_filtered_discs(
        type.upper() if type is not None else None,
        favorite_enabled,
        page,
        size,
        order_field,
        order_direction,
    )

    return jsonify(discs)

@bp.route("/discs/<string:sku>", methods=["GET"])
def get_disc_by_sku(sku: str):
    """
    Obtener un disco por SKU
    ---
    tags:
      - Discs
    summary: Obtener un disco por SKU
    description: Retorna la información detallada de un disco específico
    parameters:
      - name: sku
        in: path
        description: SKU único del disco
        required: true
        type: string
        example: "093624933595"
    responses:
      200:
        description: Disco encontrado exitosamente
        schema:
          $ref: '#/definitions/Disc'
      400:
        description: Disco no encontrado
        schema:
          $ref: '#/definitions/BusinessError'
    """
    disc = service.find_by_sku(sku)

    return jsonify(disc)

@bp.route("/discs", methods=["POST"])
def post_disc():
    """
    Crear un nuevo disco
    ---
    tags:
      - Discs
    summary: Crear un nuevo disco
    description: Agrega un nuevo disco a la colección
    parameters:
      - name: body
        in: body
        description: Datos del disco a crear
        required: true
        schema:
          $ref: '#/definitions/Disc'
    responses:
      200:
        description: Disco creado exitosamente
      400:
        description: Error de validación o disco ya existe
        schema:
          oneOf:
            - $ref: '#/definitions/BusinessError'
            - $ref: '#/definitions/ValidationError'
    """
    try:
        disc = request.json
        if not disc:
            return jsonify({"error": "Request body is required"}), 400
        
        service.save_disc(disc)
        return Response("", 200, mimetype="application/json")
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
from flask import jsonify, request
from app.discs import bp
from app.discs import service
from flask import Response
from flasgger import swag_from
from pydantic import ValidationError


@bp.route("/discs", methods=["GET"])
def get_discs():
    """
    Obtener lista de discos
    ---
    tags:
      - Discs
    summary: Obtener lista de discos
    description: Retorna todos los discos habilitados. Puede filtrar por tipo o favoritos
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
        description: Filtrar solo discos favoritos
        required: false
        schema:
          type: string
        example: "true"
    responses:
      200:
        description: Lista de discos obtenida exitosamente
        schema:
          type: array
          items:
            $ref: '#/definitions/Disc'
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

    if type is not None:
        discs = service.get_discs_by_type(type.upper())
        return jsonify(discs)

    favorite = request.args.get('favorite', None)

    if favorite is not None:
        discs = service.get_favorite_discs()
        return jsonify(discs)

    discs = service.get_discs()

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
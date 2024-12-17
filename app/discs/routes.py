from flask import jsonify, request
from flask_cors import cross_origin
from app.discs import bp
from app.discs import service
from flask import Response

@bp.route("/discs", methods=["GET"])
@cross_origin(origin='*', headers=['Content- Type','Authorization'])
def get_discs():
    type = request.args.get('type', None)

    if type is not None:
        discs = service.get_discs_by_type(type)
        return jsonify(discs)

    favorite = request.args.get('favorite', None)

    if favorite is not None:
        discs = service.get_favorite_discs()
        return jsonify(discs)

    discs = service.get_discs()

    return jsonify(discs)

@bp.route("/discs/<string:sku>", methods=["GET"])
def get_disc_by_sku(sku: str):
    disc = service.find_by_sku(sku)

    return jsonify(disc)

@bp.route("/discs", methods=["POST"])
def post_disc():
    disc = request.json

    service.save_disc(disc)

    return Response("", 200, mimetype="application/json")
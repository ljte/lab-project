from flask import jsonify


def resource_not_found(e):
    return jsonify(error=str(e)), 404


def bad_request(e):
    return jsonify(error=str(e)), 400

from flask import jsonify


def resource_not_found(e):
    print(str(e))
    return jsonify(error=str(e)), 404

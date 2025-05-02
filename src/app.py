"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_list_family():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def post_member():
    member = request.json
    print("añadido", member)
    jackson_family.add_member(member)
    return member, 200

@app.route('/members/<int:id>', methods=['GET'])
def get_only_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"Error": "Miembro no encontrado"}), 404
    return jsonify(member)

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_only_member(id):
    member = jackson_family.delete_member(id)
    if member is None:
        return jsonify({"Error": "Miembro no encontrado"}), 404
    return jsonify({"done": True, "Delete_member": member}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
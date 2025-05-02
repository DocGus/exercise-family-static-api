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

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Add initial family members
john = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}
jane = {
    "first_name": "Jane",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}
jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [3]
}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all members


@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Get a specific member by ID


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def post_member():
    # Obtener los datos del miembro desde el cuerpo de la solicitud
    member_data = request.get_json()

    # Validar que los campos esenciales estén presentes
    if not member_data or "first_name" not in member_data or "age" not in member_data:
        return jsonify({"error": "Missing required fields: 'first_name' and 'age'"}), 400

    # Añadir el miembro a la familia
    new_member = jackson_family.add_member(member_data)

    # Devolver la respuesta con el nuevo miembro y un código de estado 200 (OK)
    return jsonify({"done": True, "member": new_member}), 200


# Delete a member by ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if result.get("done"):
        return jsonify({"done": True}), 200
    return jsonify({"done": False}), 404


# Run the server
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sistemacrud"

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping') 
    print("MongoDB conectado com sucesso!")
except ConnectionFailure as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    exit(1)

db = client[DB_NAME]
collection = db["usuarios"]

def serialize_document(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@app.route("/", methods=['GET'])
def get_usuarios():
    try:
        usuarios = list(collection.find({}))
        serialized_usuarios = [serialize_document(user) for user in usuarios]
        return jsonify(serialized_usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=['POST'])
def add_usuario():
    try:
        data = request.get_json()
        if not data or "name" not in data or "email" not in data:
            return jsonify({"error": "Dados inválidos. 'name' e 'email' são obrigatórios."}), 400

        result = collection.insert_one(data)
        new_user = collection.find_one({"_id": result.inserted_id})
        
        return jsonify(serialize_document(new_user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/<id>", methods=['PUT'])
def update_usuario(id):
    try:
        data = request.get_json()
        
        obj_id = ObjectId(id)

        updated_user = collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": data},
            return_document=ReturnDocument.AFTER
        )
        
        if updated_user:
            return jsonify(serialize_document(updated_user)), 200
        else:
            return jsonify({"error": "Usuário não encontrado."}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/<id>", methods=['DELETE'])
def delete_usuario(id):
    try:
        obj_id = ObjectId(id)

        deleted_user = collection.find_one_and_delete({"_id": obj_id})
        
        if deleted_user:
            return jsonify({"message": "Usuário deletado com sucesso!"}), 200
        else:
            return jsonify({"error": "Usuário não encontrado."}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=3001, debug=True)
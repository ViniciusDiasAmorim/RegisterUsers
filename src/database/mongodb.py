from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from datetime import datetime
from models.usuario import Usuario


MONGO_URI = "mongodb+srv://grupo05:rrgCSeJAQTIo6MSM@cluster0.grtjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client["DbUsuarios"]  
usuarios_collection = db["usuarios"] 

def parse_usuario(usuario):
    return {
        "id": str(usuario["_id"]),
        "nome": usuario["nome"],
        "email": usuario["email"],
        "telefone": usuario["telefone"],
        "nome_usuario": usuario["nome_usuario"],
        "senha": usuario["senha"],
        "ativo": usuario["ativo"],
        "data_criacao": usuario["data_criacao"],
        "data_atualizacao": usuario["data_atualizacao"]
    }

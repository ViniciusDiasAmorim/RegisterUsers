from fastapi import HTTPException
from database.mongodb import usuarios_collection, parse_usuario
from models.dto import UsuarioAtualizacaoDTO
from models.usuario import Usuario
from bson.objectid import ObjectId
from datetime import datetime, timedelta


async def buscar_todos_usuarios():
    usuarios = []
    async for usuario in usuarios_collection.find():
        usuario["id"] = str(usuario["_id"])
        usuarios.append(usuario)
    return usuarios
    
async def criar_usuario(usuario: Usuario):
    validar_nome(usuario.nome_usuario)
    validar_email(usuario.email)
    validar_senha(usuario.senha)
    usuario.nome_usuario = f"{usuario.nome.lower()}.{usuario.nome.split()[-1].lower()}"
    usuario.data_criacao = usuario.data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    usuario.ativo = True
    novo_usuario = await usuarios_collection.insert_one(usuario.dict(exclude_unset=True))
    return await obter_usuario_por_id(novo_usuario.inserted_id)

async def obter_usuario_por_id(usuario_id: str):
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if usuario:
        return parse_usuario(usuario)

async def atualizar_usuario(usuario_id: str, usuario: UsuarioAtualizacaoDTO):
    validar_nome(usuario.nome_usuario)
    validar_email(usuario.email)
    validar_senha(usuario.senha)
    usuario_dict = usuario.dict(exclude_unset=True)
    usuario_dict["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M") 
    await usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": usuario_dict})
    return await obter_usuario_por_id(usuario_id)

async def redefinir_senha(usuario_id: str, dados: dict):
    validar_senha(dados["senha"])
    dados["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    await usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": dados})
    return await obter_usuario_por_id(usuario_id)

async def deletar_usuario(usuario_id: str):
    await usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    return {"msg": "Usuário deletado com sucesso"}

async def obter_usuario_por_nome_usuario(nome_usuario: str):
    usuario = await usuarios_collection.find_one({"nome_usuario": nome_usuario})
    if usuario:
        return parse_usuario(usuario)
    
async def login_usuario(nome_usuario: str, senha: str):
    usuario = await usuarios_collection.find_one({"nome_usuario": nome_usuario})
    if usuario and usuario["senha"] == senha:
        if usuario.get("ativo") is True:
            session_expiration = datetime.now() + timedelta(hours=2)
            await usuarios_collection.update_one(
                {"_id": usuario["_id"]},
                {"$set": {"session_expiration": session_expiration}}
            )
            return {"msg": "Login realizado com sucesso", "session_expiration": session_expiration}
        else:
            raise HTTPException(status_code=403,
            detail={
                "code": "INACTIVE_USER",
                "description": "O usuario esta inativo",
                "parameter_name": "inativo"
            })
    else:
        raise HTTPException(status_code=400, detail={
            "code" : "INVALID_CREDENTIALS",
            "description": "o nome de usuario ou senha sao invalidos",
            "parameters": "senha or nome_usuario"
        })

    
def validar_nome(nome: str):
    nome = nome.strip()
    if not nome:
        raise HTTPException(
            status_code = 400,
            detail={
                "code": "INVALID_NOME",
                "description": "O nome de usuario não pode estar vazio.",
                "parameter_name": "nome_usuario"
            }
        )
    
    if nome.count('.') != 1:
        raise HTTPException(
            status_code = 400,
            detail={
                "code": "INVALID_FORMAT",
                "description": "O nome de usuario deve estar no formato 'nome.sobrenome'.",
                "parameter_name": "nome_usuario"
            }
        )

    partes = nome.split('.')
    nome, sobrenome = partes

    if not nome or not sobrenome:
        raise HTTPException(
            status_code = 400,
            detail={
                "code": "INVALID_FORMAT",
                "description": "O nome de usuario deve estar no formato 'nome.sobrenome'.",
                "parameter_name": "nome_usuario"
            }
        )

def validar_email(email: str):
    if "@" not in email or "." not in email:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_EMAIL",
                "description": "O email fornecido não é válido.",
                "parameter_name": "email"
            }
        )
    
def validar_senha(senha: str):
    if len(senha) < 8:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "WEAK_PASSWORD",
                "description": "A senha deve ter pelo menos 8 caracteres.",
                "parameter_name": "senha"
            }
        )

async def verificar_sessao_valida(usuario_id: str):
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if usuario:
        if usuario.get("session_expiration") and usuario["session_expiration"] < datetime.now():
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "SESSION_EXPIRED",
                    "description": "Sessao expirada. Faça login novamente."
                }
            )
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
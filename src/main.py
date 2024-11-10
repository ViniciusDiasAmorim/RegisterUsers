from typing import List
from fastapi import FastAPI, HTTPException
from models.usuario import Usuario
from controllers.usuario_controller import (
    criar_usuario,
    obter_usuario_por_id,
    atualizar_usuario,
    deletar_usuario,
    login_usuario,
    redefinir_senha,
    buscar_todos_usuarios
)

app = FastAPI()

@app.get("/usuarios", response_model=List[Usuario])
async def listar_usuarios():
    return await buscar_todos_usuarios()

@app.post("/usuarios/", response_model=Usuario)
async def endpoint_criar_usuario(usuario: Usuario):
    return await criar_usuario(usuario)

# @app.get("/usuarios/{usuario_id}", response_model=Usuario)
# async def endpoint_obter_usuario(usuario_id: str):
#     usuario = await obter_usuario_por_id(usuario_id)
#     if not usuario:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
#     return usuario

@app.put("/usuarios/{usuario_id}", response_model=Usuario)
async def endpoint_atualizar_usuario(usuario_id: str, usuario: Usuario):
    usuario = await atualizar_usuario(usuario_id, usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.delete("/usuarios/{usuario_id}")
async def endpoint_deletar_usuario(usuario_id: str):
    await deletar_usuario(usuario_id)
    return {"msg": "Usuário deletado com sucesso"}

@app.post("/usuarios/login/")
async def endpoint_login(nome_usuario: str, senha: str):
    return await login_usuario(nome_usuario, senha)

@app.put("/usuarios/redefinir_senha/{usuario_id}")
async def endpoint_redefinir_senha(usuario_id: str, nova_senha: str):
    usuario = await obter_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await redefinir_senha(usuario_id, {"senha": nova_senha})
    return {"msg": "Senha atualizada com sucesso"}

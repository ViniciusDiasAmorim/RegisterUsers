from datetime import datetime
from pydantic import BaseModel

class Usuario(BaseModel):
    nome: str
    email: str
    telefone: str
    nome_usuario: str
    senha: str
    ativo: bool = True
    data_criacao: str = datetime.now().strftime("%d/%m/%Y %H:%M")
    data_atualizacao: str = datetime.now().strftime("%d/%m/%Y %H:%M")
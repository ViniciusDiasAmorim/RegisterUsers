from pydantic import BaseModel

class UsuarioCriacaoDTO(BaseModel):
    nome: str
    email: str
    telefone: str
    nome_usuario: str
    senha: str

class UsuarioAtualizacaoDTO(BaseModel):
    nome: str = None
    email: str = None
    telefone: str = None
    nome_usuario: str = None
    senha: str = None
    ativo: bool = None

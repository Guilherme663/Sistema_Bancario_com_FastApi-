from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.cliente_service import criar_cliente_service
from app.repositories.clientes_repo import buscar_cliente_por_email
from app.core.auth import verificar_senha, criar_token

router = APIRouter()


class CadastroRequest(BaseModel):
    nome: str
    email: str
    senha: str

class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/clientes", status_code=201)
async def cadastrar_cliente(dados: CadastroRequest):
    try:
        await criar_cliente_service(dados.nome, dados.email, dados.senha)
        return {"msg": "Cliente criado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:

        raise HTTPException(status_code=400, detail="Email já cadastrado")


@router.post("/login")
async def login(dados: LoginRequest):
    usuario = await buscar_cliente_por_email(dados.email)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    user_id, nome, email, senha_hash = usuario

    if not verificar_senha(dados.senha, senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(user_id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "nome": nome
    }
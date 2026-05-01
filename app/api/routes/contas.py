from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.conta_service import criar_conta_service, depositar, sacar
from app.repositories.conta_repo import buscar_conta
from app.repositories.transacoes_repo import listar_transacoes
from app.core.auth import verificar_token

router = APIRouter()


class ValorRequest(BaseModel):
    valor: float


@router.post("/contas", status_code=201)
async def criar_conta(user_id: int = Depends(verificar_token)):
    # user_id vem do token — o usuário cria conta pra si mesmo
    try:
        await criar_conta_service(user_id)
        return {"message": "Conta criada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/contas/depositar")
async def depositar_conta(body: ValorRequest, user_id: int = Depends(verificar_token)):
    try:
        novo_saldo = await depositar(user_id, body.valor)
        return {"message": "Depósito realizado", "novo_saldo": novo_saldo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/contas/sacar")
async def sacar_conta(body: ValorRequest, user_id: int = Depends(verificar_token)):
    try:
        novo_saldo = await sacar(user_id, body.valor)
        return {"message": "Saque realizado", "novo_saldo": novo_saldo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contas/extrato")
async def extrato(user_id: int = Depends(verificar_token)):
    conta = await buscar_conta(user_id)

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    conta_id = conta[0]  # SELECT id, cliente_id, saldo → índice 0 é o id
    transacoes = await listar_transacoes(conta_id)

    return {"transacoes": transacoes}
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "troque-por-uma-chave-longa-e-aleatoria")
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
security = HTTPBearer()


def criar_token(user_id: int) -> str:

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_MINUTOS)
    dados = {
        "sub": str(user_id),  
        "exp": expiracao
    }
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)


async def verificar_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:

    token = credentials.credentials

    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = dados.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return int(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
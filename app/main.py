from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import clientes, contas
from app.db.database import criar_tabela

@asynccontextmanager
async def lifespan(app: FastAPI):
    await criar_tabela()  # cria as tabelas ao iniciar
    yield               # aplicação roda aqui
    # (opcional) limpeza ao encerrar ficaria depois do yield

app = FastAPI(lifespan=lifespan)

app.include_router(clientes.router)
app.include_router(contas.router)   
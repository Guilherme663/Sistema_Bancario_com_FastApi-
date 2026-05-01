from app.repositories.clientes_repo import criar_cliente
from app.core.auth import pwd_context

async def criar_cliente_service(nome: str, email: str, senha: str):
    if "@" not in email:
        raise ValueError("Email inválido")

    if len(senha) < 6:
        raise ValueError("Senha deve ter pelo menos 6 caracteres")

    # bcrypt transforma a senha em hash — nunca salvamos a senha real
    senha_hash = pwd_context.hash(senha)

    await criar_cliente(nome, email, senha_hash)
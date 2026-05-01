import aiosqlite
from app.db.database import DB_NAME

async def criar_cliente(nome: str, email: str, senha_hash: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )
        await db.commit()

async def buscar_cliente_por_email(email: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT id, nome, email, senha FROM usuarios WHERE email = ?",
            (email,)
        ) as cursor:
            return await cursor.fetchone()
        # retorna (id, nome, email, senha) ou None se não encontrar

async def buscar_cliente_por_id(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT id, nome, email FROM usuarios WHERE id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone()
        # retorna (id, nome, email) ou None
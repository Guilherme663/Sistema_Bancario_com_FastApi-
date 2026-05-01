import aiosqlite
from app.db.database import DB_NAME

#aqui ele cria a conta do cliente, com saldo 0
async def criar_conta(cliente_id:int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO contas (cliente_id, saldo) VALUES (?, 0)",
            (cliente_id,)
        )
        await db.commit()
        
#aqui ele busca a conta do cliente, para verificar o saldo e etc
async def buscar_conta(cliente_id:int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT * FROM contas WHERE cliente_id = ?",
            (cliente_id,)
        ) as cursor:
            return await cursor.fetchone()

async def atualizar_saldo(cliente_id:int, novo_saldo:float):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE contas SET saldo = ? WHERE cliente_id = ?",
            (novo_saldo, cliente_id,)
        )
        await db.commit()
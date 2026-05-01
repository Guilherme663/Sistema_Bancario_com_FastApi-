import aiosqlite 
from app.db.database import DB_NAME

#aqui ele verifica a o id da conta, o tipo do registro e o valor solicitado
async def registrar_transacao(conta_id, tipo, valor):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO transacoes(conta_id, tipo, valor) VALUES (?,?,?)",(conta_id, tipo, valor)
        )
        await db.commit()

#aqui ele verifica o id da conta e lista todas as informaçoes de registros baseando-se em "tipo, valor e data"      
async def listar_transacoes(conta_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT tipo,valor,data FROM transacoes WHERE conta_id = ?", (conta_id,)
        ) as cursor:
            return await cursor.fetchall()
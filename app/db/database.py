import aiosqlite

DB_NAME = "clientes.db"

async def criar_tabela():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        #tabela clientes
        await db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
        """)
        #tabela contas
        await db.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            saldo REAL DEFAULT 0,
            FOREIGN KEY (cliente_id) REFERENCES usuarios (id)
        )
        """)
        
        await db.execute("""
        CREATE TABLE IF NOT EXISTS transacoes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_id INTEGER,
            tipo TEXT, --deposito ou saque
            valor REAL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(conta_id) REFERENCES contas(id)
        )
        """)
        
        await db.commit()
        

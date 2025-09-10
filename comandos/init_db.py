import asyncio
import aiosqlite

async def init_db():
    async with aiosqlite.connect("../database.db") as db:  # <<--- ahora apunta a database.db
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tienda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                nombre TEXT NOT NULL,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL
            )
        """)
        await db.commit()
        print("✅ Base de datos inicializada con la tabla 'tienda' en database.db.")

if __name__ == "__main__":
    asyncio.run(init_db())

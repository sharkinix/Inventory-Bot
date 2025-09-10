import aiosqlite
from config import DB_FILE

def register(bot):
    @bot.command()
    async def additem(ctx, categoria: str, nombre: str, precio_venta: float, precio_compra: float):
        async with aiosqlite.connect("database.db") as db:
            await db.execute(
                "INSERT INTO tienda (categoria, nombre, precio_venta, precio_compra) VALUES (?, ?, ?, ?)",
                (categoria, nombre, precio_venta, precio_compra),
            )
            await db.commit()
        await ctx.send(
            f"✅ Producto agregado:\n"
            f"- 📂 Categoría: **{categoria}**\n"
            f"- 🏷 Nombre: **{nombre}**\n"
            f"- 💰 Venta: **{precio_venta}** | Compra: **{precio_compra}**"
        )


    @bot.command()
    async def removeitem(ctx, categoria: str, nombre: str):
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "SELECT * FROM tienda WHERE categoria = ? AND nombre = ?",
                (categoria, nombre)
            )
            item = await cursor.fetchone()
            if not item:
                await ctx.send("❌ El ítem no existe en esa categoría.")
                return

            await db.execute(
                "DELETE FROM tienda WHERE categoria = ? AND nombre = ?",
                (categoria, nombre)
            )
            await db.commit()
            await ctx.send(f"🗑️ Ítem **{nombre}** eliminado de categoría **{categoria}**.")


    @bot.command()
    async def updateitem(ctx, categoria: str, nombre: str, precio_venta: float = None, precio_compra: float = None):
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "SELECT categoria, nombre, precio_venta, precio_compra FROM tienda WHERE categoria = ? AND nombre = ?",
                (categoria, nombre)
            )
            item = await cursor.fetchone()
            if not item:
                await ctx.send("❌ El ítem no existe en esa categoría.")
                return

            nuevo_precio_venta = precio_venta if precio_venta is not None else item[2]
            nuevo_precio_compra = precio_compra if precio_compra is not None else item[3]

            await db.execute(
                "UPDATE tienda SET precio_venta = ?, precio_compra = ? WHERE categoria = ? AND nombre = ?",
                (nuevo_precio_venta, nuevo_precio_compra, categoria, nombre)
            )
            await db.commit()
            await ctx.send(
                f"✅ Ítem **{nombre}** en categoría **{categoria}** actualizado:\n"
                f"- 💰 Venta: {nuevo_precio_venta} | Compra: {nuevo_precio_compra}"
            )


    @bot.command()
    async def shop(ctx, categoria: str = None):
        async with aiosqlite.connect(DB_FILE) as db:
            if categoria:
                cursor = await db.execute("SELECT nombre, precio_compra, precio_venta FROM tienda WHERE categoria = ?", (categoria,))
                items = await cursor.fetchall()
                if not items:
                    await ctx.send(f"❌ No hay productos en la categoría **{categoria}**.")
                    return
                mensaje = f"**🛍️ Productos en {categoria.capitalize()}**\n\n"
            else:
                cursor = await db.execute("SELECT categoria, nombre, precio_compra, precio_venta FROM tienda ORDER BY categoria")
                items = await cursor.fetchall()
                if not items:
                    await ctx.send("🛒 La tienda está vacía.")
                    return
                
                mensaje = "**🛍️ Productos y Precios**\n\n"
                mensaje += "Categoría | Nombre | Venta | Compra\n"
                mensaje += "----------------------------------\n"

            for item in items:
                if categoria:
                    mensaje += "| Nombre | Venta | Compra\n"
                    mensaje += "----------------------------------\n"
                    mensaje += f"{item[0]} | ${item[1]} | ${item[2]}\n"
                else:
                    mensaje += f"[{item[0]}] {item[1]} | ${item[2]} | ${item[3]}\n"

            await ctx.send(f"```\n{mensaje}\n```")


    @bot.command()
    async def renameitem(ctx, categoria: str, nombre_actual: str, nuevo_nombre: str):
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "SELECT * FROM tienda WHERE categoria = ? AND nombre = ?",
                (categoria, nombre_actual)
            )
            item = await cursor.fetchone()
            if not item:
                await ctx.send("❌ El ítem no existe en esa categoría.")
                return

            try:
                await db.execute(
                    "UPDATE tienda SET nombre = ? WHERE categoria = ? AND nombre = ?",
                    (nuevo_nombre, categoria, nombre_actual)
                )
                await db.commit()
                await ctx.send(f"✏️ Ítem renombrado de **{nombre_actual}** a **{nuevo_nombre}** en categoría **{categoria}**.")
            except aiosqlite.IntegrityError:
                await ctx.send("⚠️ El nuevo nombre ya existe en esa categoría. Elige otro nombre.")



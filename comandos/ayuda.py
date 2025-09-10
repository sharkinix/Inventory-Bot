import discord

def register(bot):
    @bot.command()
    async def ayuda(ctx):
        embed = discord.Embed(
            title="🤖 Bienvenido al Bot de Inventario",
            description="Aquí tienes la lista de comandos disponibles:",
            color=discord.Color.green()
        )

        # Gestión de productos
        embed.add_field(
            name="🛒 Gestión de Productos",
            value=(
                "1️⃣ `!additem <categoria> <nombre> <precio_compra> <precio_venta>` → Agrega o actualiza un producto\n"
                "2️⃣ `!updateitem <categoria> <nombre> [precio_compra] [precio_venta]` → Modifica los precios\n"
                "3️⃣ `!renameitem <nombre_actual> <nuevo_nombre>` → Cambia el nombre de un producto\n"
                "4️⃣ `!removeitem <nombre>` → Elimina un producto"
            ),
            inline=False
        )

        # Consultas
        embed.add_field(
            name="📋 Consultas",
            value=(
                "5️⃣ `!shop` → Lista completa de productos\n"
                "6️⃣ `!precio <nombre>` → Consulta el precio de un producto"
            ),
            inline=False
        )

        # Moderación
        embed.add_field(
            name="🧹 Moderación",
            value="7️⃣ `!clear [cantidad]` → Borra mensajes (por defecto 1)",
            inline=False
        )

        embed.set_footer(text="✨ Usa estos comandos para administrar tu tienda fácilmente")

        await ctx.send(embed=embed)

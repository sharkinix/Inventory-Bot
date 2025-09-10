from discord.ext import commands

def register(bot):
    @bot.command()
    @commands.has_permissions(administrator=True)  # Solo admins
    async def clear(ctx, cantidad: int = 1):
        """Elimina mensajes del canal. Solo administradores."""
        deleted = await ctx.channel.purge(limit=cantidad)
        await ctx.send(f"🧹 Se eliminaron {len(deleted)} mensaje(s).", delete_after=5)

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos de administrador para usar este comando.")

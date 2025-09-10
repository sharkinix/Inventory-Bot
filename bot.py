import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from comandos import ayuda, tienda, util


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


# Registrar comandos
ayuda.register(bot)
tienda.register(bot)
util.register(bot)

# Conexión a la DB (opcional)
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

bot.run(TOKEN)

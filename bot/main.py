from core import MyClient

import discord


client = MyClient(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready!")
    client.loop.create_task(client.heartbeat())

client.run("token")
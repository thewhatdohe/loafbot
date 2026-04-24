import discord
import os
import random

# ---token---
token = os.getenv("TOKEN")


class MyClient(discord.Client):
    user: discord.ClientUser

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})\n') # logs
    async def on_message(self, message):
        if message.author.id == self.user.id: # ignore self sent messages
            return
        # ---!hello---
        if message.content.startswith('!hello'):
            await message.reply('Hello World!')

        # ---!say---
        if message.content.startswith('!say'):
            await message.reply(message.content.removeprefix('!say'))

        # ---!roll---
        if message.content.startswith('!roll'):
            data = message.content.split()

            try:
                n1 = int(data[1])
                n2 = int(data[2])
                await message.reply(str(random.randint(n1, n2)))
            except (IndexError, ValueError):
                await message.reply("Syntax: !roll <# min> <# max>")



if token is None:
    raise ValueError("TOKEN environment variable not set")

# ---intents---
intents = discord.Intents.default() # initialize permission requests
intents.message_content = True 

# ---main---
client = MyClient(intents=intents)
client.run(token)
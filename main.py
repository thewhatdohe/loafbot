import discord
import os

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
            say_command_reply = message.content.removeprefix('!say')
            await message.reply(say_command_reply)

if token is None:
    raise ValueError("TOKEN environment variable not set")

# ---intents---
intents = discord.Intents.default() # initialize permission requests
intents.message_content = True 

# ---main---
client = MyClient(intents=intents)
client.run(token)
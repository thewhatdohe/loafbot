import discord
from discord.ext import commands
import os
import random
import asyncio
import string

# ---token---
token = os.getenv("TOKEN")

if token is None:
    raise ValueError("TOKEN environment variable not set")

# ---intents---
intents = discord.Intents.default() # initialize permission requests
intents.message_content = True

# ---main---
bot = commands.Bot(command_prefix='!', intents=intents)

MAX_REACTIONSPAM = 50 # keep reaction bursts from tripping discord's rate limit

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})\n') # logs


# ---!hello---
@bot.command()
async def hello(ctx):
    """Says hello."""
    await ctx.reply('Hello World!')


# ---!say---
@bot.command()
async def say(ctx, *, text: str = ''):
    """Repeats back whatever you say."""
    if not text:
        await ctx.reply('Syntax: !say <text>')
        return
    await ctx.reply(text)


# ---!roll---
@bot.command()
async def roll(ctx, min_n: int = None, max_n: int = None):
    """Rolls a random number between min and max."""
    if min_n is None or max_n is None:
        await ctx.reply('Syntax: !roll <# min> <# max>')
        return
    await ctx.reply(str(random.randint(min_n, max_n)))


# ---!talk---
@bot.command()
async def talk(ctx):
    """AI chat mode (not implemented yet)."""
    await ctx.reply("AI mode isn't implemented yet, stay tuned!")


# ---!ping---
@bot.command()
async def ping(ctx):
    """Shows the bot's latency."""
    await ctx.reply(f'Pong! {round(bot.latency * 1000)}ms')


# ---!coinflip---
@bot.command()
async def coinflip(ctx):
    """Flips a coin."""
    await ctx.reply(random.choice(['Heads', 'Tails']))


# ---!choose---
@bot.command()
async def choose(ctx, *options: str):
    """Picks randomly from a list of options."""
    if len(options) < 2:
        await ctx.reply('Syntax: !choose <option 1> <option 2> ...')
        return
    await ctx.reply(random.choice(options))


# ---!8ball---
@bot.command(name='8ball')
async def eight_ball(ctx, *, question: str = ''):
    """Ask the magic 8-ball a question."""
    if not question:
        await ctx.reply('Syntax: !8ball <question>')
        return
    responses = [
        "It is certain.", "Without a doubt.", "Yes, definitely.",
        "You may rely on it.", "As I see it, yes.", "Most likely.",
        "Outlook good.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful.",
    ]
    await ctx.reply(random.choice(responses))


# ---!reverse---
@bot.command()
async def reverse(ctx, *, text: str = ''):
    """Reverses the given text."""
    if not text:
        await ctx.reply('Syntax: !reverse <text>')
        return
    await ctx.reply(text[::-1])


# ---!avatar---
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Shows a member's avatar (yours by default)."""
    member = member or ctx.author
    await ctx.reply(member.display_avatar.url)


# ---!userinfo---
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Shows info about a member (yours by default)."""
    member = member or ctx.author
    embed = discord.Embed(title=str(member), color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Account created', value=discord.utils.format_dt(member.created_at), inline=False)
    if isinstance(member, discord.Member) and member.joined_at:
        embed.add_field(name='Joined server', value=discord.utils.format_dt(member.joined_at), inline=False)
    await ctx.reply(embed=embed)


# ---!serverinfo---
@bot.command()
async def serverinfo(ctx):
    """Shows info about the current server."""
    guild = ctx.guild
    if guild is None:
        await ctx.reply("This command only works in a server.")
        return
    embed = discord.Embed(title=guild.name, color=discord.Color.blurple())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name='ID', value=guild.id, inline=False)
    embed.add_field(name='Members', value=guild.member_count, inline=False)
    embed.add_field(name='Created', value=discord.utils.format_dt(guild.created_at), inline=False)
    await ctx.reply(embed=embed)


# ---!poll---
@bot.command()
async def poll(ctx, *, question: str = ''):
    """Posts a yes/no poll that reacts with thumbs up/down."""
    if not question:
        await ctx.reply('Syntax: !poll <question>')
        return
    poll_message = await ctx.reply(f'**{question}**')
    await poll_message.add_reaction('👍')
    await poll_message.add_reaction('👎')


# ---!remindme---
@bot.command()
async def remindme(ctx, seconds: int = None, *, text: str = ''):
    """Reminds you of something after N seconds (max 3600)."""
    if seconds is None:
        await ctx.reply('Syntax: !remindme <seconds> <message>')
        return
    seconds = max(1, min(seconds, 3600))
    await ctx.reply(f"Okay, I'll remind you in {seconds} seconds.")
    await asyncio.sleep(seconds)
    reminder = text or "here's your reminder!"
    await ctx.reply(f'{ctx.author.mention} {reminder}')


# ---!emojify---
@bot.command()
async def emojify(ctx, *, text: str = ''):
    """Turns text into regional indicator emoji letters."""
    if not text:
        await ctx.reply('Syntax: !emojify <text>')
        return
    digit_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    out = []
    for c in text.lower():
        if c in string.ascii_lowercase:
            out.append(f':regional_indicator_{c}: ')
        elif c in string.digits:
            out.append(f':{digit_names[int(c)]}: ')
        elif c == ' ':
            out.append('   ')
        else:
            out.append(c + ' ')
    await ctx.reply(''.join(out))


# ---!reactionspam---
@bot.command()
async def reactionspam(ctx, emoji: str = None, amount: int = None):
    """Reacts to the last <amount> messages in this channel with <emoji>."""
    if emoji is None or amount is None:
        await ctx.reply('Syntax: !reactionspam <emoji> <amount of messages>')
        return

    amount = max(1, min(amount, MAX_REACTIONSPAM))

    reacted = 0
    async for msg in ctx.channel.history(limit=amount, before=ctx.message):
        try:
            await msg.add_reaction(emoji)
            reacted += 1
        except discord.HTTPException:
            pass
        await asyncio.sleep(0.25) # avoid hammering the rate limit

    if reacted == 0:
        await ctx.reply(f"Couldn't react with {emoji} to any messages. Is it a valid emoji?")


bot.run(token)

import discord
import time
import sys
import traceback
import re
import asyncio
import random
from discord.ext import commands
import os
import pyshorteners
from discord.utils import get
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
import translators as ts
import aiohttp
import requests
import datetime




PREFIX = '.'
client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')
#Bot has been started
@client.event

async def on_ready():
    print("Бот прокинувся та готовий до роботи!")
    await client.change_presence(status = discord.Status.online, activity=discord.Game('.help'))

for cog in os.listdir(r"cogs"):
    if cog.endswith(".py"):
        try:
            cog =f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)

        except Exception as e:
            print(f"{cog} не можуть бути завантажені.")
            raise e

# World
slavauk = ['слава україні', 'слава украине', 'slava ukraini', "glory to ukraine"]
slavanac = ['slava nacii', 'glory of the nation', 'слава нації', 'слава нации']
ukponad = ['ukraine', 'украина', 'україна']


# Clear messages
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 101):
    await ctx.channel.purge(limit=amount + 1)

# Kick user

@client.command()
@commands.has_permissions(kick_members= True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    await ctx.channel.purge(limit = 1)
    if member == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи користувача!", description='Ви не вказали учасника, якого збираєтесь вигнати.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.kick @user spam```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif reason == None:
        emb = discord.Embed(title=":x:Чуваче, ти хочешь вигнати цьому вылупка просто так? ", description='Вкажи причину, козак.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.kick @user spam```', inline=False)
        emb.add_field(name='Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: москаль||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    else:
        emb = discord.Embed(title='Учасник', colour = discord.Color.purple())
        emb.set_author(name = member.name, icon_url= member.avatar_url)
        emb.set_thumbnail(url='https://www.upload.ee/image/14236852/_________-2.png')
        emb.add_field(name= '🧨 Був кікнутий', value=f'з цього сервера по причині {reason}.')
        emb.set_footer(text='Це зробив адміністратор: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)
        await member.send(embed = emb)
        await asyncio.sleep(2)
        await member.kick(reason=reason)

        
@client.command(pass_context=True)
async def botservers(ctx):
    await client.say("Кількість серверів, на яких є я існую: " + str(len(client.servers)) + " серверів🤏")
    
        
# Ban user
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member = None, time = None, *, reasone = None):
    await ctx.channel.purge(limit = 1)
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    if member == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи користувача!", description='Ви не вказали учасника, якому збираєтесь закрити ротяку.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.ban @user spam```', inline=False)
        emb.add_field(name='Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: лох||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif reasone == None:
        emb = discord.Embed(title=":x:Чуваче, ти хочешь заткнути рота цьому вылупку просто так? ",
                            description='Вкажи причину, козак.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.ban @user spam```', inline=False)
        emb.add_field(name='Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: москаль||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    tempmute = int(time[:-1]) * time_convert[time[-1]]
    emb = discord.Embed(title='Учасник', colour=discord.Color.purple())
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.set_thumbnail(url='https://www.upload.ee/image/14236852/_________-2.png')
    emb.add_field(name='🥏 Був заблокований', value='на цьому сервері.')
    emb.add_field(name=f'Час блокування {time}.', value=f'По причині {reasone}.', inline=False)
    emb.set_footer(text='Це зробив адміністратор: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
    await member.send(embed=emb)
    await asyncio.sleep(2)
    await member.ban()
    await asyncio.sleep(tempmute)
    banned_user = await ctx.guild.bans()
    for ban_entry in banned_user:
        user = ban_entry.user
        await ctx.guild.unban(user)
        emb = discord.Embed(title='Учасник', colour=discord.Color.purple())
        emb.set_author(name=user.name, icon_url=user.avatar_url)
        emb.set_thumbnail(url='https://www.upload.ee/image/14236852/_________-2.png')
        emb.add_field(name='✨ Був розблокований', value='на цьому сервері.')
        emb.set_footer(text='Це зробив адміністратор: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    return

# Unban user
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    banned_user = await ctx.guild.bans()
    for ban_entry in banned_user:
        user = ban_entry.user
        await ctx.guild.unban(user)
        emb = discord.Embed(title='Учасник', colour=discord.Color.purple())
        emb.set_author(name=user.name, icon_url=user.avatar_url)
        emb.set_thumbnail(url='https://www.upload.ee/image/14236852/_________-2.png')
        emb.add_field(name='✨ Був розблокований', value='на цьому сервері.')
        emb.set_footer(text='Це зробив адміністратор: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    return

# Mute user
@client.command()
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member = None, time = None, *, reasone = None):
    await ctx.channel.purge(limit=1)
    muted_role = discord.utils.get(ctx.guild.roles, name= "Muted")
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    if member == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи користувача!", description='Ви не вказали учасника, якому збираєтесь закрити ротяку.', colour = discord.Color.purple())
        emb.add_field(name = 'Правильний вигляд команди:', value='```.mute @user 10s spam```', inline=False)
        emb.add_field(name = 'Види часу:', value='s - секунди; m - хвилини; h - години; d - дні', inline=False)
        emb.add_field(name = 'Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: лох||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed = emb)
    elif time == None:
        emb = discord.Embed(title=":x:Вилупок, вкажи час!", description='Ви не вказали час, на який треба закрити ротяку.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.mute @user 10s spam```', inline=False)
        emb.add_field(name='Види часу:', value='s - секунди; m - хвилини; h - години; d - дні', inline=False)
        emb.add_field(name='Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: лох||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif reasone == None:
        emb = discord.Embed(title=":x:Чуваче, ти хочешь заткнути рота цьому вылупку просто так? ", description='Вкажи причину, козак.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.mute @user 10s spam```', inline=False)
        emb.add_field(name='Види часу:', value='s - секунди; m - хвилини; h - години; d - дні', inline=False)
        emb.add_field(name='Причини:', value='Причини можуть бути індивідуальні. ||Навіть причина: лох||', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif muted_role == None or muted_role == False:
        permissions = discord.Permissions(change_nickname=True)
        mute_role = await ctx.guild.create_role(name='Muted', permissions=permissions, color= discord.Color.red())
        for text_channel in ctx.guild.text_channels:
            await text_channel.set_permissions(mute_role, send_messages=False)
    else:
        tempmute = int(time[:-1]) * time_convert[time[-1]]
        emd = discord.Embed(title='👤 Учаснику',
                            description=f'{member.mention} закрив ротяку, адміністратор: @{ctx.author.name} на {time}, по причині {reasone}.',
                            colour=discord.Color.purple())
        emd.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emd)
        await member.add_roles(muted_role)
        await asyncio.sleep(tempmute)
        await member.remove_roles(muted_role)
        emd = discord.Embed(title='✨ Учасник', description=f'{member.mention} знову може відкрити ротяку.',
                            colour=discord.Color.purple())
        emd.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emd)

#Unmute
@client.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if member == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи користувача!", description='Ви не вказали учасника, якому збираєтесь закрити ротяку.', colour = discord.Color.purple())
        emb.add_field(name = 'Правильний вигляд команди:', value='```.unmute @user```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed = emb)
    else:
        emd = discord.Embed(title='✨ Учасник', description=f'{member.mention} знову може відкрити ротяку.',
                            colour=discord.Color.purple())
        emd.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emd)
        await member.remove_roles(muted_role)

# Mention user
@client.command()
async def tag(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if member == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи користувача!", description='Ви не вказали учасника, якого збираєтесь покликати.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.tag @user```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    emb = discord.Embed(title='🔔 Учасник', description=f'**{member.mention}, тебе гукає гайдамака: {ctx.author.mention}**', colour = discord.Color.purple())
    emb.set_footer(text = ctx.author.name, icon_url= ctx.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed = emb)
    await member.send(embed = emb)

#Show avatar
@client.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title = "🔗 Завантажити", url=ctx.author.avatar_url)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_image(url=ctx.author.avatar_url)
        emb.set_footer(text=f'Аватар користувача: {ctx.author.name}.')
        await ctx.send(embed=emb)
    else:
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title = "🔗 Завантажити", url=member.avatar_url)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_image(url=member.avatar_url)
        emb.set_footer(text=f'Аватар користувача: {member.name}.')
        await ctx.send(embed=emb)

#Show server avatar
@client.command()
async def serverava(ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title = "🔗 Завантажити", url=ctx.guild.icon_url)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_image(url=ctx.guild.icon_url)
        emb.set_footer(text=f'Аватар сервера: {ctx.guild.name}.')
        await ctx.send(embed=emb)

format = "**%d** %b | %Y "
format2 = "%d %b | %B %Y "
#Server Info
@client.command()
@commands.guild_only()
async def server(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    name = ctx.guild.name
    description = str(ctx.guild.description)
    role_count = len(ctx.guild.roles)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    channels = text_channels + voice_channels
    icon = str(ctx.guild.icon_url)
    embed = discord.Embed(
        title = name,
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=icon)
    embed.set_author(name = "Інформація про сервер: ", icon_url=icon)
    embed.add_field(name=":id: Server ID", value=id, inline=True)
    embed.add_field(name=":clock1: Створений", value=f"{ctx.guild.created_at.strftime(format)}", inline=True)
    embed.add_field(name=f":closed_lock_with_key: Ролі", value=f"**{role_count}** Ролей")
    embed.add_field(name=f":busts_in_silhouette: Учасники ({memberCount})", value=f"**{memberCount}** Учасників", inline=True)
    embed.add_field(name= f":speech_balloon: Канали ({channels})", value= f"**{text_channels}** Текстові| **{voice_channels}** Голосові")
    embed.add_field(name= "🍼 Створений", value= "by Lukash#2604")
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#Randomly
@client.command()
async def roll(ctx, snum = None):
    await ctx.channel.purge(limit=1)
    if snum == None:
        emb = discord.Embed(title='🎲 Випадкове число:', description= f"**{(random.randint(1,101))}**", color= discord.Color.purple())
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title='🎲 Випадкове число:', description=f"**{(random.randint(1, int(snum)))}**", color=discord.Color.purple())
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb)

#Coin:
@client.command()
async def coin(ctx, snum = None):
    await ctx.channel.purge(limit=1)
    variants = ['Орел', 'Решка']
    emb = discord.Embed(title='🪙 Випала сторона монети:', description=f"**{(random.choice(variants))}**", colour = discord.Color.purple())
    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    await ctx.send(embed = emb)

#Short your link
@client.command()
async def short(ctx, url = None):
    await ctx.channel.purge(limit=1)
    if url == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи посилання!", description='Ви не вказали посилання, яке збираєтесь скоротити.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.short https://www.google.com```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    else:
        url = url
        s = pyshorteners.Shortener()
        shorturl = s.tinyurl.short(url)
        emb = discord.Embed(title = '🔗 Ось ваше посилання:', description= f"Link: {shorturl}")
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

#TicTacToe
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("Це хід: <@" + str(player1.id) + ">.")
        elif num == 2:
            turn = player2
            await ctx.send("Це хід: <@" + str(player2.id) + ">.")
    else:
        await ctx.send("Ви вже граєте! Закінчить цю гру, щоб почати нову.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1
                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " переміг!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Нічия!")
                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Впевніться, що ви вибрали правильні числа від 1 до 9.")
        else:
            await ctx.send("Це не твій хід.")
    else:
        await ctx.send("Розпочніть гру за допомогою команди: .tictactoe.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Будь ласка, вкажіть опонента.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Будь ласка, перевірте тег опонента.")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Будь ласка, введіть позицію, яку ви хочете позначити.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Обов’язково введіть ціле число.")

#mems
@client.command(pass_context=True)
async def meme(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="", description="", colour = discord.Color.purple())

    async with aiohttp.ClientSession() as cs:
        URL = ['https://www.reddit.com/r/RussiaUkraineWarMemes/new.json?sort=hot', 'https://www.reddit.com/r/ukrainememes/new.json?sort=hot', 'https://www.reddit.com/r/uamemesforces/new.json?sort=hot', 'https://www.reddit.com/r/ukraine22memes/new.json?sort=hot', 'https://www.reddit.com/r/UkrainianMemes/new.json?sort=hot', 'https://www.reddit.com/r/Ukraine_in_memes/new.json?sort=hot', 'https://www.reddit.com/r/dankmemes/new.json?sort=hot']
        async with cs.get(random.choice(URL)) as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            embed.set_footer(text = ctx.author.name, icon_url= ctx.author.avatar_url)
            embed.set_author(name = client.user.name, icon_url= client.user.avatar_url)
            await ctx.send(embed=embed)

#Create a text channel
@client.command()
@commands.has_permissions(manage_channels = True)
async def createtext(ctx, channel_name):
    await ctx.channel.purge(limit=1)
    guild = ctx.guild
    channel = await guild.create_text_channel(channel_name)

#Create a category
@client.command()
@commands.has_permissions(manage_channels = True)
async def createcat(ctx, category_name):
    guild = ctx.guild
    await guild.create_category_channel(category_name)
    await ctx.channel.purge(limit=1)

#Delete a text channel
@client.command()
@commands.has_permissions(manage_channels = True)
async def deletetext(ctx, channel_name):
    await ctx.channel.purge(limit=1)
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        await channel.delete()

#Dog
@client.command()
async def dog(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="🐶 Песик!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#cat
@client.command()
async def cat(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="😺 Котик!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#panda
@client.command()
async def panda(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/panda')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/panda')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="🐼 Панда!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#fox
@client.command()
async def fox(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/fox')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/fox')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="🦊 Лис!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#bird
@client.command()
async def bird(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/bird')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/bird')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="🐔 Пташка!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#Koala
@client.command()
async def koala(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/Koala')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/Koala')
      factjson = await request2.json()
      translator_factjson = ts.google(factjson['fact'], translator=ts.google, to_language='uk')
      translation = str(translator_factjson)
   embed = discord.Embed(title="🐨 Коала!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.add_field(name="Цікавий факт:", value=f"**{translation}**")
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#Joke
@client.command()
async def joke(ctx):
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
       request2 = await session.get('https://some-random-api.ml/joke')
       factjson = await request2.json()
       translator_factjson = ts.google(factjson['joke'], translator=ts.google, to_language='uk')
       translation = str(translator_factjson)
       embed = discord.Embed(title="🃏 Жарт!", color=discord.Color.purple())
       embed.add_field(name="HorukraineBot's", value=f"**{translation}**")
       embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
       embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
       await ctx.send(embed=embed)

#anime
@client.command()
async def anime(ctx):
   animes = ["https://some-random-api.ml/animu/wink", "https://some-random-api.ml/animu/pat", "https://some-random-api.ml/animu/hug"]
   await ctx.channel.purge(limit=1)
   async with aiohttp.ClientSession() as session:
      request = await session.get(random.choice(animes))
      dogjson = await request.json()
      # This time we'll get the fact request as well!
   embed = discord.Embed(title="", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
   await ctx.send(embed=embed)

#Create password
@client.command()
async def password(ctx, length: int = None):
    await ctx.channel.purge(limit=1)
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = length
    password = ''

    if length == None:
        for i in range(8):
            password += random.choice(chars)
        embed = discord.Embed(title = "Пароль згенеровано.", colour = discord.Color.purple())
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="🧾 Пароль:", value=f"```{password}```", inline=False)
        embed.add_field(name="Вид команди:", value=f"```.password 21```", inline=False)
        embed.add_field(name="Довжина паролю:", value=f"*З 1 до 1000 символів.*", inline=False)
        await ctx.author.send(embed=embed)
    else:
        length = length
        for i in range(length):
            password += random.choice(chars)
        embed = discord.Embed(title="🔑 Пароль згенеровано.", colour=discord.Color.purple())
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="🧾 Пароль:", value=f"```{password}```", inline=False)
        embed.add_field(name="Вид команди:", value=f"```.password 21```", inline=False)
        embed.add_field(name="Довжина паролю:", value=f"*З 1 до 1000 символів.*", inline=False)
        await ctx.author.send(embed=embed)

#weathering
@client.command()
async def weather(ctx, *, city: str = None):
    await ctx.channel.purge(limit=1)
    if city == None:
        emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи місто!",
                            description='Ви не вказали місто, де хочете дізнатися погоду.',
                            colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.weather citi```', inline=False)
        emb.add_field(name='Назву міста можно писати:', value='```на Українській та москальській мові.```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    else:
        api_key = "f2954a7666f59b7c9b62f994ad7298b6"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                ts_weather_description = ts.google(weather_description, translator=ts.google, to_language='uk')
                eather_description = z[0]["description"]
                embed = discord.Embed(title=f"🌈 Погода в {city_name}",
                                      color=ctx.guild.me.top_role.color,
                                      timestamp=ctx.message.created_at, )
                embed.add_field(name="⛅ Опис:", value=f"**{ts_weather_description}**", inline=False)
                embed.add_field(name="🌡 Температура(C):", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                embed.add_field(name="💧 Вологість повітря(%):", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(name="🗜 Атмосферний тиск(hPa):", value=f"**{current_pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                await channel.send(embed=embed)
        else:
            emb = discord.Embed(title=":x:Трясся твоїй матері! Вкажи правильне місто!",
                                description='Ви не правильно вказали місто, де хочете дізнатися погоду.',
                                colour=discord.Color.purple())
            emb.add_field(name='Правильний вигляд команди:', value='```.weather citi```', inline=False)
            emb.add_field(name='Назву міста можно писати:', value='```на Українській та москальській мові.```',
                          inline=False)
            emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.author.send(embed=emb)

#crypto
@client.command()
async def crypto(ctx, type = None):
   await ctx.channel.purge(limit=1)
   if type == None:
       emb = discord.Embed(title=":x:Ви вказали не правильну криптовалюту!",
                           description='Ви не правильно вказали валюту, курс якої хочете дізнатися.',
                           colour=discord.Color.purple())
       emb.add_field(name='Правильний вигляд команди:', value='```.crypto BTC```', inline=False)
       emb.add_field(name='Доступні криптовалюти:', value='```BTC, ETH, LTC, BUSD, SOL, USDT, XRP, BNB, ADA, USDS```',
                     inline=False)
       emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
       emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
       await ctx.author.send(embed=emb)
   elif type == "BTC":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Bitcoin!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/64px-Bitcoin.svg.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "ETH":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Ethereum!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://static.okx.com/cdn/assets/imgs/221/5F33E3F751873296.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "LTC":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Litecoin!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/200x200/2.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "BUSD":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=BUSD&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс BUSD!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://changenow.io/images/cached/busdbsc.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "SOL":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=SOL&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Solana!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://cdn3d.iconscout.com/3d/premium/thumb/solana-4437052-3684819.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "USDT":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=USDT&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Tether!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/200x200/825.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "XRP":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс XRP!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://totalcoin.io/uploads/coins/big/xrp.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "BNB":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=BNB&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Binance Coin!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://sapienwallet.com/wp-content/uploads/2020/11/logo2.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "ADA":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=ADA&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс Cardano!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://assets-global.website-files.com/5e73a1e3ba24f2cd5dd2232a/620b32e6370a500fec9b11c5_ada.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   elif type == "USDS":
       async with aiohttp.ClientSession() as session:
           request2 = await session.get('https://min-api.cryptocompare.com/data/price?fsym=USDS&tsyms=USD,UAH,EUR')
           factjson = await request2.json()
           embed = discord.Embed(title="💱 Курс USD Coin!", color=discord.Color.purple())
           embed.add_field(name="💵 USD:", value=f"**{factjson['USD']}**", inline=False)
           embed.add_field(name="💶 EUR:", value=f"**{factjson['EUR']}**", inline=False)
           embed.add_field(name="💳 UAH:", value=f"**{factjson['UAH']}**", inline=False)
           embed.set_thumbnail(url='https://totalcoin.io/uploads/coins/big/usdc.png')
           embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
           embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
           await ctx.send(embed=embed)
   else:
       emb = discord.Embed(title=":x:Перевірте назву криптовалюту!",
                           description='Ви не правильно вказали валюту, курс якої хочете дізнатися.',
                           colour=discord.Color.purple())
       emb.add_field(name='Правильний вигляд команди:', value='```.crypto BTC```', inline=False)
       emb.add_field(name='Доступні криптовалюти:', value='```BTC, ETH, LTC, BUSD, SOL, USDT, XRP, BNB, ADA, USDS```',
                     inline=False)
       emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
       emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
       await ctx.author.send(embed=emb)

#rate
@client.command()
async def rate(ctx, type = None):
    await ctx.channel.purge(limit=1)
    today = datetime.datetime.now()
    today_format = today.strftime("%d** **%m** **%Y")
    if type == None:
        emb = discord.Embed(title=":x:Ви вказали не правильну валюту!",
                            description='Ви не правильно вказали валюту, курс якої хочете дізнатися.',
                            colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.rate USD```', inline=False)
        emb.add_field(name='Доступні валюти:', value='```USD, EUR, GBP, CNY, PLN```',
                      inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif type == "USD":
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://api.monobank.ua/bank/currency')
            rates = await request2.json()
            embed = discord.Embed(title="💱 Курс Долару!", color=discord.Color.purple())
            embed.add_field(name="💵 USD:", value=f"**{rates[0]['rateSell']}**", inline=False)
            embed.add_field(name="📆 Дата:", value=f"**{today_format}**", inline=False)
            embed.set_thumbnail(url='https://www.pngarts.com/files/3/Green-Dollar-PNG-Picture.png')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    elif type == "EUR":
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://api.monobank.ua/bank/currency')
            rates = await request2.json()
            embed = discord.Embed(title="💱 Курс Євро!", color=discord.Color.purple())
            embed.add_field(name="💶 EUR:", value=f"**{rates[1]['rateSell']}**", inline=False)
            embed.add_field(name="📆 Дата:", value=f"**{today_format}**", inline=False)
            embed.set_thumbnail(url='https://iconape.com/wp-content/png_logo_vector/eur.png')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    elif type == "GBP":
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://api.monobank.ua/bank/currency')
            rates = await request2.json()
            embed = discord.Embed(title="💱 Курс Фунту стерлінгу!", color=discord.Color.purple())
            embed.add_field(name="💳 GBP:", value=f"**{rates[3]['rateCross']}**", inline=False)
            embed.add_field(name="📆 Дата:", value=f"**{today_format}**", inline=False)
            embed.set_thumbnail(url='https://images.vexels.com/media/users/3/135999/isolated/preview/6c3f3472afd2cc726de1a1779b868503-gbp-pound-coin-icon.png')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    elif type == "CNY":
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://api.monobank.ua/bank/currency')
            rates = await request2.json()
            embed = discord.Embed(title="💱 Курс Китайского юаню!", color=discord.Color.purple())
            embed.add_field(name="💳 CNY:", value=f"**{rates[6]['rateCross']}**", inline=False)
            embed.add_field(name="📆 Дата:", value=f"**{today_format}**", inline=False)
            embed.set_thumbnail(url='https://ecnydigitalyuan.com/wp-content/uploads/2021/04/e-cny-1.png')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    elif type == "PLN":
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://api.monobank.ua/bank/currency')
            rates = await request2.json()
            embed = discord.Embed(title="💱 Курс Злотого!", color=discord.Color.purple())
            embed.add_field(name="💳 PLN:", value=f"**{rates[82]['rateCross']}**", inline=False)
            embed.add_field(name="📆 Дата:", value=f"**{today_format}**", inline=False)
            embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/2413/2413195.png')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    else:
        emb = discord.Embed(title=":x:Ви вказали не правильну валюту!",
                            description='Ви не правильно вказали валюту, курс якої хочете дізнатися.',
                            colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.rate USD```', inline=False)
        emb.add_field(name='Доступні валюти:', value='```USD, EUR, GBP, CNY, PLN```',
                      inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)

#Movies
@client.command()
async def movie(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("🕑 Треба трошки почекати...")
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://k2maan-moviehut.herokuapp.com/api/random')
        movie = await request.json()
        movie_name = movie['name']
        URL = f'https://serpapi.com/search.json?q={movie_name} the movie logo&tbm=isch&ijn=0&api_key=af6cd4b226a344ce4868d8235a465999d1570667f78d9552430f2109ada00516'
        data = requests.get(URL).json()
    embed = discord.Embed(title="📽️ Випадковий фільм!", color=discord.Color.purple())
    embed.add_field(name="🎞️ Назва:", value=f"**{ts.google(movie['name'], translator=ts.google, to_language='uk')}**")
    embed.add_field(name="🎬 Режисер:", value=f"**{ts.google(movie['director'], translator=ts.google, to_language='uk')}**")
    embed.add_field(name="📆 Рік випуску:", value=f"**{movie['releaseYear']}**")
    embed.add_field(name="🕜 Тривалість:", value=f"**{ts.google(movie['runtime'], translator=ts.google, to_language='uk')}**")
    embed.add_field(name="🗒️ Жанри:", value=f"**{ts.google(movie['genre'], translator=ts.google, to_language='uk')}**")
    embed.add_field(name="📊 Рейтинг:", value=f"**{movie['imdbRating']}**")
    embed.add_field(name="📒 Опис:", value=f"**{ts.google(movie['overview'], translator=ts.google, to_language='uk')}**")
    embed.set_thumbnail(url=f"{data['suggested_searches'][0]['thumbnail']}")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#ip
@client.command()
async def ip(ctx, ip = None):
    await ctx.channel.purge(limit=1)
    URL = f'http://apiip.net/api/check?ip={ip}&accessKey=37d3f651-c2da-4a26-a6d8-34720fd68c90'
    data = requests.get(URL).json()
    if ip == None:
        emb = discord.Embed(title=":x:Ви не вказали ip-адресу!", description='Ви не вказали ip-адрес, інформацію про який хочете дізнатися.', colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.ip 127.0.0.1```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    elif 'success' in data:
        emb = discord.Embed(title=":x:Неправильний ip-адрес!",
                            description='Ви не правильно вказали ip-адрес, інформацію про який хочете дізнатися.',
                            colour=discord.Color.purple())
        emb.add_field(name='Правильний вигляд команди:', value='```.ip 127.0.0.1```', inline=False)
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)
    else:
        emb = discord.Embed(title="Інформація про ip-адресу!",
                            description=f'**IP:** **``{ip}``**',
                            colour=discord.Color.purple())
        emb.add_field(name='Код континенту:', value=data['continentCode'], inline=False)
        emb.add_field(name='Назва континенту:', value=data['continentName'], inline=False)
        emb.add_field(name='Код країни:', value=data['countryCode'], inline=False)
        emb.add_field(name='Назва країни:', value=data['countryName'], inline=False)
        emb.add_field(name='Офіційна назва країни:', value=data['officialCountryName'], inline=False)
        emb.add_field(name='Місто:', value=data['city'], inline=True)
        emb.add_field(name='Поштовий індекс:', value=data['postalCode'], inline=False)
        emb.add_field(name='Столиця країни:', value=data['capital'], inline=True)
        emb.add_field(name='Прапор:', value=data['countryFlagEmoj'], inline=True)
        emb.set_thumbnail(url='https://lumpics.ru/wp-content/uploads/2016/05/Programmy-dlya-smeny-IP.png')
        emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=emb)


# Help
@client.command()

async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='**Головна сторінка:**', description='http://horukraine.mypressonline.com', colour = discord.Color.purple())
    emb.set_author(name = client.user.name, icon_url= client.user.avatar_url)
    emb.set_thumbnail(url = 'https://www.upload.ee/image/14236852/_________-2.png')
    emb.set_footer(text = ctx.author.name, icon_url= ctx.author.avatar_url)
    emb.add_field(name = 'Список команд:', value="http://horukraine.mypressonline.com/command.html", inline=False)
    emb.add_field(name = 'Допомогти ЗСУ:', value='https://war.ukraine.ua/donate/', inline=False)
    await ctx.author.send(embed = emb)

@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()

    if msg in slavauk:
        await message.channel.send("💙 💛 **Героям слава!** 💙 💛")

    if msg in slavanac:
        await message.channel.send('💙 💛 **Смерть ворогам!** 💙 💛')

    if msg in ukponad:
        await message.channel.send('💙 💛 **Понад усе!** 💙 💛')

token = open('token.txt', 'r').readline()
client.run(token)



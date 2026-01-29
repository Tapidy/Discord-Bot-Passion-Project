import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
import os
import youtube_dl
import ffmpeg
import random
from random import choice
import asyncio
import praw
from praw import reddit
import web
from web import keep_alive

userAgent = 'Passion Project Bot'

cID = 'MA9it9NnaAuKdQ'

cSC= 'yk952A4ExUpF1bPVuQHOWQfOSte52A'

userN = '//insert username here//'

userP = '//insert password here//'

numFound = 0

reddit = praw. Reddit (user_agent=userAgent, client_id=cID, client_secret=cSC, username=userN, password=userP, check_for_async=False)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=',', case_insensitive=True, intents=intents)

song_played=[]

@client.event
async def on_ready():
    print('Bot is online!')
    print('---------------------')
    await client.change_presence(activity = discord.Streaming(name = "Things", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    for filename in os.listdir('./cog'):
        if filename.endswith('.py'):
            client.load_extension(f'cog.{filename[:-3]}')
    print('---------------------')

@client.command(name='meme', help='sends a meme in the channel')
async def meme(ctx):
  async with ctx.typing():
    subreddit = reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit = 150)

    for submission in top:
      all_subs.append(submission)
  
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name, color = 0xFF5733)

    em.set_image(url = url)
  await ctx.send(embed = em)

ydl_opts = {
    'format': 'bestaudio/best',
    'default_search': 'auto',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def endSong(guild, path):
    os.remove(path)

@client.event
async def on_member_join(member):
    try:
      channel = discord.utils.get(member.guild.channels, name='welcome')
      await channel.send(f'Welcome {member.mention}!  :D** ** See `,help` command for details!')
    except:
      pass
        
@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['Hello', '**o/**', 'Hello, how are you?', 'Hi']
    await ctx.send(choice(responses))

@client.command(name='end', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@client.command(name='credits', help='This command returns the TRUE credits')
async def creditz(ctx):
    await ctx.send('**Tapidy#6594**')

@client.command(name='join', help='this command make the bot join a voice channel')
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
    except:
        await ctx.send(ctx.author.mention + " Please join a voice channel.")
        return False

    vc = ctx.voice_client
    if vc == None:
        await channel.connect()
        await ctx.send(ctx.author.mention + '** I Have Joined Your Channel**')
    return True

@client.command(name='play', help='this command plays a song')
async def play(ctx, url):
    data = await join(ctx)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    if data == True:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
        guild = ctx.message.guild
        voice_client = guild.voice_client
        for file in os.listdir("./"):
          if file.endswith(".mp3") and not voice_client.is_playing() and file not in song_played and not voice == None :
            voice_client.play(discord.FFmpegPCMAudio(file), after=lambda x: endSong(guild, file))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
            await ctx.send(ctx.author.mention + '** Now Playing Requested Audio**')
  
@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()
    await ctx.send(ctx.author.mention + '** Audio Paused**')
@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
    await ctx.send(ctx.author.mention + '** Audio Resumed**')

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    await ctx.send(ctx.author.mention + '** Bye**')
@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()
    await ctx.send(ctx.author.mention + '** Audio Stopped**')

@client.command(name='addrole', help='gives and removes roles *Only people with admin can use it*')
async def addrole(ctx, role: discord.Role, user: discord.Member):
  if ctx.author.guild_permissions.administrator:
    await user.add_roles(role)
    await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
@client.command() 
async def removerole(ctx, role: discord.Role, user: discord.Member):
  if ctx.author.guild_permissions.administrator:
    await user.remove_roles(role)
    await ctx.send(f"Successfully removed {role.mention} from {user.mention}.")

@client.command(pass_context = True, help='work in progress')
async def movie(ctx):
  async with ctx.typing():
    await ctx.send(file=discord.File(r'smth/shrek_movie.webm'))


keep_alive()
client.run('//insert token here//')
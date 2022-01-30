
from requests import get
from cogs.cog_dependencies.Downloader import YTDL
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from discord.player import FFmpegPCMAudio
# -*- coding: utf-8 -*-

# optionFile = open("cogs/options.txt", "r").readline()

##Instatiate empty options
# options ={}
# Loop through options.txt and concantenate each line to String options
# with open("cogs/options.txt", "r") as f:
#     x = f.readlines()
#     for y in x:
#         options = options + y

options = {
    'format': 'bestaudio/best',
    'extractaudio': True,  # only keep the audio
    'audioformat': "mp3",  # convert to mp3
    # 'outtmpl': '%(id)s',    # name the file the ID of the video
    'noplaylist': True,  # only download single song, not playlist
    'outtmpl': '%USERPROFILE%\Documents\discord bot\cache\\' + '%(title)s' + '.mp3',
    'forceduration': True
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #      'preferredcodec': 'mp3'
    # }],
}

class musicMan(commands.Cog):
    """Bot commands for playing music."""
    classDownloaderList = []
    isPlaying = asyncio.Event()
    isPlaying.set()
    current_song = ""
    url_downloader = YTDL(options)
    hasPlayer = False
    def __init__(self, bot):
        self.bot = bot

    # save file as the YouTube ID   
    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Joins channel if user who calls the command is in a voice channel and returns voice client for use elsewhere"""
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                voice = await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)
                voice = ctx.voice_client
        else:
            await ctx.send("You must be in a voice channel to use this command.")
        return voice
    @commands.command(pass_context=True)
    async def queue(self, ctx):
        """Displays the queue to Discord chat."""
        songs = self.queue_string_builder(self.url_downloader.queue.get_queue())
        await ctx.send(songs)
    
    def queue_string_builder(self,queue):
        """Builds the string to be displayed in Discord chat that contains the queue."""
        songs = "Currently Playing: " + self.current_song + "\n"+ "Queue: \n"
        i = 0
        for song in queue:
            i += 1
            songs = songs + str(i) + ": " + song + "\n"
        return songs
        
    @commands.command(pass_context=True)
    async def play(self, ctx, *args):
        """Queues a song to be played by player.
        runs the player() method only if it is not already running, as defined by
        the class attribute hasPlayer."""
        if len(args) == 0:
            await ctx.send("Specify a search or file.")
        else:
            voice = await ctx.invoke(self.bot.get_command('join'))
            try:    
                get(args[0])
            except:
                url =f"ytsearch:{args}"
                search = True
            else:
                url = args[0]
                search = False   
            try:               
                self.url_downloader.download_and_get_info(url, search)
                self.url_downloader.queue.add_song(self.url_downloader.video_title)
                await ctx.send("Song added to queue.")
            except PermissionError:
                try:
                    self.url_downloader.queue.add_song(self.url_downloader.video_title)
                    await ctx.send("Song added to queue.")
                except CommandInvokeError:
                    print(CommandInvokeError)              
            if(not self.hasPlayer):
                print("Here")
                                        #Bot literally takes too long and disconnects before this can happen
                await self.player(voice)
                    
                    
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = ctx.voice_client
        voice.pause()
        
    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice = ctx.voice_client
        voice.resume()
        
    @commands.command(pass_context=True)
    async def volume(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Enter a volume.")
        else:
            try:    
                input_volume = int(args[0])
                if(input_volume < 0 or input_volume > 100):
                    await ctx.send("Enter a volume between 0 and 100.")
                else:
                    new_volume = input_volume * .01
                    voice = ctx.voice_client
                    voice.source = discord.PCMVolumeTransformer(voice.source, volume = new_volume)
            except ValueError:
                await ctx.send("Enter a number between 0 and 100.")            
                       
    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """Skips current song in queue."""
        voice = ctx.voice_client
        voice.stop()
        self.isPlaying.set()
        await ctx.send(self.current_song + " Skipped.")
                 
    async def player(self, voice):
        """Contains the voice player object from Discord.py.\n
        Runs forever and sets hasPlayer to true until the last song in the queue is played, which sets it to false 
        and breaks the loop. """
        while (True):
            await self.isPlaying.wait()
            self.hasPlayer = True
            self.isPlaying.clear()
            
            current_queue = self.url_downloader.queue.get_queue()          
            video_title = current_queue[0]
            self.current_song = video_title
            
            source = FFmpegPCMAudio('cache\\' + video_title + '.mp3')
            
            voice.play(source, after=lambda e: self.isPlaying.set())
            self.url_downloader.queue.next_song()
            
            print("Playing " + video_title)
            if(not self.url_downloader.queue.has_next()):
                await self.isPlaying.wait()
                if(not self.url_downloader.queue.has_next()):   #this looks silly but i think it is not
                    break
        self.hasPlayer = False


#priority
#Migrate to nextcord and yt-dlp
#No Priority TODO: Set up environment or local variable for music cache to make portable
def setup(bot):
    bot.add_cog(musicMan(bot))

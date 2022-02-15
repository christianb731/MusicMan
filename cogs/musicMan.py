from requests import get
from cogs.cog_dependencies.Downloader import YTDL
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from discord.player import FFmpegPCMAudio

options = {
    'format': 'bestaudio/best',
    'extractaudio': True,  # only keep the audio
    'audioformat': "mp3",  # convert to mp3
    'noplaylist': True,  # only download single song, not playlist
    'outtmpl': '%USERPROFILE%\Documents\discord bot\cache\\' + '%(title)s' + '.mp3',
    'forceduration': True
}

class musicMan(commands.Cog):
    """Bot commands for playing music."""
    classDownloaderList = []
    hasNext = asyncio.Event()
    notPlaying = asyncio.Event()
    notPlaying.set()
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
                self.hasNext.set()
                await ctx.send("Song added to queue.")
            except PermissionError:
                try:
                    self.url_downloader.queue.add_song(self.url_downloader.video_title)
                    self.hasNext.set()
                    await ctx.send("Song added to queue.")
                except CommandInvokeError:
                    print(CommandInvokeError)              
            if(not self.hasPlayer):
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
        try:
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
        except Exception:
            await ctx.send("Bot is not playing.")
                          
    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """Skips current song in queue."""
        voice = ctx.voice_client
        voice.stop()
        await ctx.send(self.current_song + " Skipped.")
                 
    async def player(self, voice):
        """Contains the voice player object from Discord.py.\n
        A loop that runs for as long as the program is running and waits for itself to stop playing to play the next song. \n
        Also waits for the queue to not be empty to attempt to play the next song in the queue."""
        while (True):
            await self.notPlaying.wait()
            await self.hasNext.wait()
            self.hasPlayer = True
            current_queue = self.url_downloader.queue.get_queue()      
            if(len(current_queue) > 0):       
                video_title = current_queue[0]
                self.current_song = video_title
                source = FFmpegPCMAudio('cache\\' + video_title + '.mp3')
                voice.play(source, after=lambda e: self.notPlaying.set())
                self.notPlaying.clear()
                self.url_downloader.queue.next_song()
                print("Playing " + video_title)
            else:
                self.hasNext.clear()

def setup(bot):
    bot.add_cog(musicMan(bot))

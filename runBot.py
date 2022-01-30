import discord
from discord.ext import commands


TOKEN = open("token.txt", "r").readline()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    print ('Logged in as {0.user}'.format(client))

def runBot(x):
    x.run(TOKEN)

try:
    client.load_extension('cogs.startupCommands')
    client.load_extension('cogs.musicMan')
    print("Successfully loaded Cogs")
except Exception as e:
    print(e)

#Trying to figure out how to add cogs to the bot
if __name__ =="__main__":
    runBot(client)
    
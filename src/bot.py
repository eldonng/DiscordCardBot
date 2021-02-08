import discord
from discord.ext import commands
from src import Bridge

client = discord.Client()
game = Bridge.Bridge()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('fak u eldon'):
        await message.channel.send('WAT')

    if message.content.startswith('!join'):
        if game.gameStarted:
            await message.channel.send(game.addPlayer(message.author))
            if game.numOfPlayers() == 4:
                await message.channel.send('All players found! Starting game...')
                game.startGame()
                for player in game.players:
                    await player.name.send(player.displayHand())
        else:
            await message.channel.send('Game has not started. Use \'!startgame\' to start a game!')

    if message.content.lower().startswith('!startgame'):
        if not game.gameStarted:
            game.setGameChannel(message.channel)
            game.setGameStarted(True)
            await message.channel.send('Game Started!')
            await message.channel.send(game.addPlayer(message.author))
        else:
            await message.channel.send('Game has already started!')

    if message.content.lower().startswith('!endgame'):
        await message.channel.send('Game Ended')
        game.endGame()

bot = commands.Bot(command_prefix='$')


@bot.command(name='test')
async def nine_nine(ctx):
    await ctx.send("testing here")


client.run('ODA3OTgxNjk1NjMzODUwMzc4.YB_5lw.ZsZWqKaxpstJ-oZGT8mxtmEUuz0')

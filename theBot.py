#Module Importation
import json
import discord
from discord.ext import commands
import asyncio
import os
import sys
import datetime
import CalculateLib
import logging
from discord.ext import tasks
from collections import defaultdict, deque
from image_gen import generate_image
import string
from io import BytesIO
import random

adminlist =[382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952]

#Commands Def
desc = ("Bot made by molchu, CodeWritten and Amethysm for a game called Hackers to make simple and complex calculations")

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))
connections = nested_dict(2, bool)

bot = commands.Bot(command_prefix = "Alexa ", description=desc, help_command = None, case_insensitive = True)
bot.remove_command('help')


@bot.event
async def on_ready():
    logChannel = bot.get_channel(681216619955224583)
    print("Up and running")
    await logChannel.send('Bot Boottime was passed, Bot Online')
    await bot.change_presence(status = discord.Status.online)

@bot.event
async def on_message(message):
    logChannel = bot.get_channel(691104272066150480)
    messagecontent = message.content
    pingfilter = "@"
    if messagecontent.count(pingfilter) == 0: 	
      currentchannel = bot.get_channel(message.channel.id)
      if message.guild is None:
          print(message.author.name + '#' + message.author.discriminator + ": " + message.content)
      messageLister = messagecontent.split(" ")
      if message.author == bot.user:
          return
      if message.author.bot:
          return
      if messageLister[0] == "Alexa":
          await logChannel.send(f'=========== NEW LOG ===========\nContent of message: {message.content} \nDate and Time in UTC: {str(message.created_at)} \nServer Orgin: {currentchannel.guild.name} channel: {currentchannel.name} \nMessage sender\'s name: ```{message.author.name}#{message.author.discriminator}```\n=========== END LOG ===========')
      await bot.process_commands(message)
    
@bot.event
async def on_command_error(ctx,error):
    if error == asyncio.TimeoutError:    
#    embed = discord.Embed(color = 0xff0000)#    
#    embed.add_field(name="Oops, an error occured!", value = error, inline = False)
        await ctx.send(f"<@{ctx.author.id}>, you failed to enter a node name within the time limit, command cancelled")
        print (error)
    else:
        await ctx.send('Oops, an error occured! {}'.format(error))
        print(error)
    
@bot.command(aliases = ['o','k','b','oo','m','e','r'], description= 'no shiet', brief = "does nothing", hidden = True)
async def test(ctx):
    await ctx.send('ok boomer')
    
@bot.command(description = "Enables/Disables Status Check Loops, ADMIN ONLY")
async def statusCheck(ctx, args):
    if args == "True" and ctx.author.id in (382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952):
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name = "Started Bot Status Update Task Loop", value = "Set Successfully", inline= False)
        embed.set_footer(text= f"Requested by {ctx.author.display_name + '#' + ctx.author.discriminator}", icon_url= ctx.author.avatar_url)
        await ctx.send (embed=embed)
        statusChecks.start()
        
    elif args == "False" and ctx.author.id in (382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952):
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name = "Stopped Bot Status Update Task Loop", value = "Set Successfully", inline= False)
        embed.set_footer(text= f"Requested by {ctx.author.display_name + '#' + ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        statusChecks.stop()
        
    elif args == "Send" and ctx.author.id in (382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952):
        channel = bot.get_channel(664250913376043049)
        currentDate= datetime.datetime.now()
        embed= discord.Embed(color = 0x00ff00)
        embed.add_field (name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
        embed.add_field (name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
        embed.add_field (name = "Status: Gateway", value = "Online", inline = False)
        embed.add_field (name = "Status: Bot", value = "Online", inline = False)
        embed.add_field (name = "Status: Heroku", value = "Online", inline = False)
        await channel.send(embed=embed)
        
    elif args == 'sendHere':
        currentDate= datetime.datetime.now()
        embed= discord.Embed(color = 0x00ff00)
        embed.add_field (name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
        embed.add_field (name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
        embed.add_field (name = "Status: Gateway", value = "Online", inline = False)
        embed.add_field (name = "Status: Bot", value = "Online", inline = False)
        embed.add_field (name = "Status: Heroku", value = "Online", inline = False)
        await ctx.send(embed=embed)
        
@tasks.loop(seconds = 1800)
async def statusChecks():
    channel = bot.get_channel(664250913376043049)
    currentDate= datetime.datetime.now()
    embed= discord.Embed(color = 0x00ff00)
    embed.add_field (name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
    embed.add_field (name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
    embed.add_field (name = "Status: Gateway", value = "Online", inline = False)
    embed.add_field (name = "Status: Bot", value = "Online", inline = False)
    await channel.send(embed=embed)
    
    
@bot.command(description="(This shows the help page that you're currently viewing).", brief="`.help [command]`")
async def help(ctx, *, args=None):
    if args is not None:
        b = args.split()
    try:
        if args is None:
            embed = discord.Embed(color=0x00ff00, title = desc)
            a = list(bot.commands)
            for i in range(0,len(bot.commands)):
                if a[i].hidden == True:
                    pass
                else:
                    embed.add_field(name=a[i].name, value = str(a[i].description),inline=False)
            embed.set_footer(text="For more information on any command type |.help <command>| (work in progress)")
            await ctx.author.send(embed=embed)
            await ctx.send('A message with the help page sent to your DM!')
        elif len(b) == 1:
            reqCommand = bot.get_command(b[0])
            embed = discord.Embed(color=0x00ff00,title = "Help page for " + reqCommand.name + " command:")
            embed.add_field(name="Usage: ", value = str(reqCommand.brief),inline=True)
            if len(reqCommand.aliases) != 0:
                embed.add_field(name="Aliases: ", value = str(reqCommand.aliases), inline = False)
            else:
                embed.add_field(name="Aliases: ", value = "No aliases", inline = False)
            embed.add_field(name="Description on usage:", value = reqCommand.description,inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("Failed sending the message with the help page. Did you block the bot?")

@bot.command(hidden= True)
async def userinfo(ctx, args1):
    guser= ctx.guild.get_member(int(args1))
    await ctx.send(f"{guser},\n{guser.id},\n{guser.display_name},\n{guser.bot},\n{guser.top_role},\n{guser.joined_at},\n{guser.activities},\n{guser.guild},\n{guser.nick}")
                         
@bot.command(description = "Return the latency of the bot. Can also be triggered with .ping", aliases=['ping'], brief = "`Alexa ping`")
async def latency(ctx):
    await ctx.send("Pong! "  + str(round(bot.latency * 1000)) + "ms.")
    
@bot.command(description="Calculates ",brief='`Alexa calculate {program} {program level} {program amount} {node} {node level} {node amount} (repeat)`', aliases=['calc','dmgcalc'])
async def calculate(ctx, *, args):
    result = CalculateLib.calculate(args)
    if result is None:
        await ctx.send('The node is unable to be taken over')
    elif result > 180:
        await ctx.send('The node is unable to be taken over')
    else:
        await ctx.send(f'The node is taken over in {result} seconds')
        
@bot.command(description="Calculate the visibility of stealth program.", brief='`Alexa stealthCalc {scanner level} {stealth program} {level} {amount} {another stealth program} {level} {amount} (and so on)`')
async def stealthCalc(ctx,*,args):
    result = CalculateLib.stealthCalc(args)
    if result > 3600:
        await ctx.send('Cannot install all the programs, alarm triggered before finishing')
    else:
        await ctx.send(f'The total amount of visibility point needed for installing all the programs is {result}')
        
@bot.command(brief = "`Alexa lsStat {program/node} {stat} [level]` ", aliases=['info'],description="(This lists the Paremeters of a certain program or node. For example: beamCannon DPS will list all dps values of beam cannon for all levels, or beamCannon DPS 21 to only list the level 21 value.typeProgramAndNodeNamesLikeThisPlease (They're case sensitive)")
async def lsStat(ctx, *, args):
    argsList = args.split(' ')
    embed=discord.Embed(color=0x00ff00)
    with open("{}.json".format(argsList[0]), "r") as f:
        temp1 = json.load(f)
    if len(argsList) == 3:
        if 'imageAddress' in temp1.keys():
            embed.set_thumbnail(url = temp1['imageAddress'][argsList[2]])
        embed.add_field(name= "Level " + argsList[2] + " " + argsList[0].capitalize() + "'s "  + argsList[1] + ":", value = temp1[argsList[1]][argsList[2]],inline=True)
        await ctx.send(embed=embed)
    elif len(argsList) == 2 and isinstance(temp1[argsList[1]], dict):
        if 'imageAddress' in temp1.keys() and isinstance(temp1['imageAddress'], dict) is False:
            embed.set_thumbnail(url = temp1['imageAddress'])
        for i in range(0,len(temp1[argsList[1]])):
            a = []
            b = []
            for key in temp1[argsList[1]].keys():
                a.append(key)
            for value in temp1[argsList[1]].values():
                b.append(value)
            name = a[i]
            value = b[i]
            embed.add_field(name='Level ' + str(name), value = value, inline=True   )
        await ctx.send(embed=embed)
    elif len(argsList) == 2 and isinstance(temp1[argsList[1]],dict) is False:
        value = temp1[argsList[1]]
        embed.add_field(name = argsList[0].capitalize() + " " + argsList[0].capitalize() + "'s " + argsList[1].capitalize(), value = value, inline = False)
        await ctx.send(embed=embed)
##Alexa dpsCalc {program} {level} {amount} {node} {level} 0 (repeat if needed)
@bot.command(brief = "`Currently dead, use calculate instead`", description="This command calculates the raw DPS of all programs. This does not account for projectile travel time and therefore assumes every program has a hit interval of 1 second, and damage is also calculated for 1 second, so the number might be ever so off. This uses the same syntax as projCalc, which you will find below. typeProgramAndNodeNamesLikeThisPlease")
async def dpsCalc(ctx, *, args):
    argsList = args.split(" ")
    i = 0
    argsName = []
    argsLevel = []
    argsAmount = []
    while i < len(argsList):
        argsName.append(argsList[i])
        i = i+3
    i = 1
    while i < len(argsList):
        argsLevel.append(argsList[i])
        i = i+3
    i = 2
    while i < len(argsList):
        argsAmount.append(argsList[i])
        i = i+3
    argsTuple = zip(argsName, argsLevel, argsAmount)
    dpsamount = 0.0
    boiii = 0.0
    anotherTempValueYetAgain = 0.0
    for x, y, z in argsTuple:
        with open("{}.json".format(x), "r") as f:
            temp1 = json.load(f)
            if temp1["isAStructure"] == 0:
                boii = temp1["DPS"]
                dpsamount = dpsamount + float(boii[str(y)])*float(z)
                #i have no idea how to fix install time so for now it will stay bugged to shit
                ohGodPleaseStop = boiii-float(temp1["installTime"])
                if float(temp1["DPS"])*ohGodPleaseStop > anotherTempValueYetAgain*ohGodPleaseStop:
                    boiii = float(temp1["installTime"])
                    anotherTempValueYetAgain = float(temp1["DPS"])
                elif boiii == 0:
                    boiii = float(temp1["installTime"])
                boii = temp1["firewall"]
                boiii = boiii + (float(boii[str(y)]) / float(dpsamount))
                dpsamount = 0.0
##    embed=discord.Embed(color=0x00ff00)
##    embed.add_field(name="Calculation Complete!",value="It took {} seconds to hack the base.".format(boiii))
    await ctx.send("It took {} seconds to hack the base.".format(boiii))
    
@bot.command(brief = '`Alexa projCalc {program} {level} {amount} {node} {level} 0 (repeat)`',description="This command calculates time based on projectile firing intervals and install times of the programs. This command assumes that projectiles are instant hitting and doesn't take into account the time it takes for a projectile to reach the target. The syntax is as follows: command <programName> <level> <amountOfProgram> <nodeName> <level> <putARandomNumberHere>. The bot will stack all of the program damage prior to the node entering and then will calculate all of the collected dps against the node it finds, reset the dps and then start calculating again. So, you can port the whole base into text and the bot will calculate it. typeProgramAndNodeNamesLikeThisPlease")
async def projCalc(ctx, *, args):
    argsList = args.split(" ")
    i = 0
    argsName = []
    argsLevel = []
    argsAmount = []
    while i < len(argsList):
        argsName.append(argsList[i])
        i = i+3
    i = 1
    while i < len(argsList):
        argsLevel.append(argsList[i])
        i = i+3
    i = 2
    while i < len(argsList):
        argsAmount.append(argsList[i])
        i = i+3
    argsTuple = zip(argsName, argsLevel, argsAmount)
    projamount = 0.0
    pleaseend = 0.0
    mysuffering = 0.0
    weDontHaveTime = 0.0
    temporaryvalue = 0
    for x, y, z in argsTuple:
        if x == "beamCannon":
            await ctx.send("beams aren't projectile so the whole command intentionally crashed")
            break
        with open("{}.json".format(x), "r") as f:
            temp1 = json.load(f)
            if temp1["isAStructure"] == 0:
                temp2 = temp1["DPS"]
                temp3 = temp1["installTime"]
                temp4 = temp1["hitInterval"]
                if mysuffering < temp4:
                    mysuffering = temp4
                if pleaseend < temp3:
                    pleaseend = temp3
                projamount = projamount + float(temp2[str(y)])*float(z)
                temporaryvalue = 0
            else:
                temp2 = temp1["firewall"]
                structureFirewall = temp2[str(y)]
                floatedStructureFirewall = float(structureFirewall)
                while floatedStructureFirewall > 0.0:
                    if projamount <= 0:
                        await ctx.send("you can't have negative programs so good job crashing the whole command")
                        break
                    if temporaryvalue == 1:
                        weDontHaveTime = weDontHaveTime + mysuffering
                    floatedStructureFirewall = floatedStructureFirewall - projamount
                    temporaryvalue = 1
                weDontHaveTime = weDontHaveTime + pleaseend
    embed=discord.Embed(color=0x00ff00)
    embed.add_field(name="Calculation Complete!",value="It took {} seconds to hack the base.".format(weDontHaveTime))
    await ctx.send("It took {} seconds to hack the base.".format(weDontHaveTime))
    
@bot.command(brief='`Alexa playDespacito/reboot`', description="This restarts the bot, which is useful if something goes wrong or the bot freezes. Only a select few people are able to use this command.",aliases=['reboot'])
async def playDespacito(ctx):
    if ctx.author.id in (382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952):
        authid= ctx.author
        embed = discord.Embed(color = 0x00ff00)
        embed.add_field(name="Shutdown Command Sent, Bot Rebooting in 3 seconds", value = "Sent By {}".format(authid), inline = False)
        await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await bot.close()
        os.execl(sys.executable, sys.executable, * sys.argv)
    else:
        await ctx.send("Sorry, you aren't allowed to use this command. Are you the admin of the server you are executing this in? DM CodeWritten#4044 to be added to the exceptions list!")
        
        
@bot.command(description="Load a module on to the bot, so we (dev team) don't have to restart the bot each time we change a single line of code in the module")
async def load(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.load_extension(f'cogs.{extension}')
            print(f'{extension} has been loaded')
    
        else:
            await ctx.send(f'{extension} has been loaded')
            bot.load_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")
    
@bot.command(description="Unload a module in the bot, in the case of abusing a command in that module")
async def unload(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.unload_extension(f'cogs.{extension}')
            print(f'{extension} has been unloaded')
    
        else:
            await ctx.send(f'{extension} has been unloaded')
            bot.unload_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")
    
@bot.command(description="Reload a module in the bot")
async def reload(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.reload_extension(f'cogs.{extension}')
            print(f'{extension} has been reloaded')
    
        else:
            await ctx.send(f'{extension} has been reloaded')
            bot.reload_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")

@load.error
async def load_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to load")
    
        
@unload.error
async def unload_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to unload")
    
        
@reload.error
async def reload_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to reload")
    
        
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@bot.command(description = "in progress", hidden = True)
async def netBuild(ctx):
    await ctx.send("Network building started in {}'s DM!".format(ctx.author.name))
    try:
        await ctx.author.send('Network building started!')
    except discord.Forbidden:
        await ctx.send("Hmm, looks like I couldn't DM you. Did you block the bot?")
    connections = nested_dict(2,bool)
    nodeList = {'netCon'}
    i = 0
    queue = deque()
    queue.append('netCon')
    try:
        def check(m):
            return m.author == ctx.author and m.guild is None
        while queue:
            curNode = queue.pop()
            await ctx.author.send('Input all nodes connected to node: {}.'.format(curNode))
            msg = await bot.wait_for('message', timeout = 20.0, check=check)
            if msg.content == 'end':
                for i in connections:
                    connections[i] = dict(connections[i])
                await ctx.author.send(dict(connections))
                break
            msgContent = (msg.content).split()
            for b in range(0,len(msgContent)):
                connections[msgContent[b]][curNode] = True
                connections[curNode][msgContent[b]] = True
                if msgContent[b] not in nodeList: queue.append(msgContent[b])
                nodeList.add(msgContent[b])
        connections = dict(connections)
        for i in connections:
            connections[i] = dict(connections[i])
        print(connections)
        await ctx.author.send(dict(connections))
        im = generate_image(connections)
        with BytesIO() as image_binary:
            im.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
    except EOFError:
        await ctx.send("idk")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)        

statusRunning = True

async def botStatusLoop():
    presencelist = ["Working on Taking Over The World","Competing with Keyboard Cat","Playing Dead","Listening to 2 Servers","Idling but not Idling"]
    i = -1
    while statusRunning == True:
        i = i + 1
        if (i >= len(presencelist)): i = 0
        await bot.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=presencelist[i]))
        await asyncio.sleep(10)

@bot.command(description = "Changes bot status")
async def botStatus(ctx, args1):
    if args1 == "Offline":
        statusRunning = False
        await bot.change_presence(status=discord.Status.invisible)

    if args1 == "Online":
        statusRunning = False
        bot.loop.create_task(botStatusLoop())

token = os.environ.get('BOT_TOKEN')
bot.run(token)
#bot.close()


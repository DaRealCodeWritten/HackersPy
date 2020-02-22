#Module Importation
import json
import discord
from discord.ext import commands
import asyncio
import time
import subprocess
import os
import math
import sys
import random
import datetime
from discord.ext import tasks

#Bot Functionality
async def timeCal(progDamage,progInstallTime,progHitInterval,progProjectileTime,progAmount,isProgMulti,nodeFirewall,nodeRegeneration,nodeAmount):
    firewall = nodeFirewall
    regen = nodeRegeneration
    time = progInstallTime
    i = 0
    if int(progAmount) <= 0:
        return None
    if isProgMulti == 0:
        for x in range(1,int(nodeAmount)+1):
            while True:
                if firewall <= 0:
                    break
                i += 0.1
                if i == max(progHitInterval - progProjectileTime, 0.1):
                    if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10:
                        firewall -= progDamage * int(progAmount) / 10
                    else:
                        return None
                    i = 0
                firewall += (firewall / 100 * regen) / 10
                time += 0.1
                if time > 10000:
                    return time
            firewall = nodeFirewall
    else:
        while True:
            if firewall <= 0:
                break
            i += 0.1
            if i == max(progHitInterval - progProjectileTime, 0.1):
                if (progDamage * int(progAmount)) / 10 > (firewall / 100 * regen) / 10:
                    firewall -= progDamage * int(progAmount) / 10
                else:
                    return None
                i = 0
            firewall += (firewall / 100 * regen) / 10
            time += 0.1
            if time > 10000:
                return time
    return time

async def stealthCal(visibility, stealthProgVisibility, stealthProgInstallTime):
    time = 0
    i = 0
    while True:
        time += 20
        time += (stealthProgInstallTime * (stealthProgVisibility / 100 * visibility))
        i += 1
        if i == stealthProgInstallTime:
            break
        if time >= 3600:
            break
    return round(time,0)            

            
#Commands Def
desc = ("Bot made by molchu, CodeWritten and Amethysm for a game called Hackers to make simple and complex calculations")

bot = commands.Bot(command_prefix = "Alexa ", description=desc, help_command = None, case_insensitive = True)
bot.remove_command('help')

botToken = os.environ.get(BOT_TOKEN)

@bot.event
async def on_ready():
    print("Up and running")
    presencelist = ["Working on Taking Over The World","Competing with Keyboard Cat","Playing Dead","Listening to 2 Servers","Idling but not Idling"]
    while True:
        for i in range(0, len(presencelist)):
            game = discord.Game(presencelist[i])
            await bot.change_presence(status=discord.Status.online, activity = game)
            await asyncio.sleep(120)
    
    channel= bot.get_channel(679214195119620117)
    await channel.send('Bot Boottime was passed, Bot Online')

@bot.event
async def on_message(message):
    """Logs messages sent to the bot via DM."""
    if message.guild is None:
        print(message.author.name + message.author.discriminator + ": " + message.content)

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(color = 0xff0000)
    embed.add_field(name="Oops, an error occured!", value = error, inline = False)
    await ctx.send('Oops, an error occured! {}'.format(error))
    print(error)

@bot.command(aliases = ['o','k','b','oo','m','e','r'], description= 'no shiet', brief = "does nothing", hidden = True)
async def test(ctx):
    await ctx.send('ok boomer')

@bot.command(description = "Enables/Disables Status Check Loops, ADMIN ONLY")
async def statusCheck(ctx, args):
    if args == "True" and ctx.author.id in (525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208):
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name = "Started Bot Status Update Task Loop", value = "Set Successfully", inline= False)
        embed.set_footer(text= f"Requested by {ctx.author.display_name + '#' + ctx.author.discriminator}", icon_url= ctx.author.avatar_url)
        await ctx.send (embed=embed)
        statusChecks.start()

    elif args == "False" and ctx.author.id in (525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208):
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name = "Stopped Bot Status Update Task Loop", value = "Set Successfully", inline= False)
        embed.set_footer(text= f"Requested by {ctx.author.display_name + '#' + ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        statusChecks.stop()

    elif args == "Send" and ctx.author.id in (525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208):
        channel = bot.get_channel(679214195119620117)
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
    channel = bot.get_channel(679214195119620117)
    currentDate= datetime.datetime.now()
    embed= discord.Embed(color = 0x00ff00)        
    embed.add_field (name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
    embed.add_field (name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
    embed.add_field (name = "Status: Gateway", value = "Online", inline = False)
    embed.add_field (name = "Status: Bot", value = "Online", inline = False)
    embed.add_field (name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
    embed.add_field (name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
    embed.add_field (name = "Status: Gateway", value = "Online", inline = False)
    embed.add_field (name = "Status: Bot", value = "Online", inline = False)
    embed.add_field (name = "Status: Heroku", value = "Online", inline = False)
    await channel.send(embed=embed)

@tasks.loop(seconds = 1800)
async def statusChecks():
    channel = bot.get_channel(679214195119620117)
    currentDate= datetime.datetime.now()
    embed= discord.Embed(color = 0x00ff00)        
    embed.add_field(name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
    embed.add_field(name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
    embed.add_field(name = "Status: Gateway", value = "Online", inline = False)
    embed.add_field(name = "Status: Bot", value = "Online", inline = False)
    embed.add_field(name = "STATUS CHECK", value = 'At {}'.format(currentDate), inline = False)
    embed.add_field(name = "Status: Ping", value = '{} ms'.format(str(round(bot.latency * 1000))), inline = False)
    embed.add_field(name = "Status: Gateway", value = "Online", inline = False)
    embed.add_field(name = "Status: Bot", value = "Online", inline = False)
    embed.add_field(name = "Status: Heroku", value = "Online", inline = False)
    await channel.send(embed=embed)
    embed.add_field(name = "Status: Heroku", value = "Online", inline = False)

        
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

@bot.command(description = "Return the latency of the bot. Can also be triggered with .ping", aliases=['ping'], brief = "`Alexa ping`")
async def latency(ctx):
    await ctx.send("Pong! "  + str(round(bot.latency * 1000)) + "ms.")
    
@bot.command(description="Calculates ",brief='`Alexa calculate {program} {program level} {program amount} {node} {node level} {node amount} (repeat)`', aliases=['calc','dmgcalc'])
async def calculate(ctx, *, args):
    argsList = args.split()
    progsName = []
    progsLevel = []
    progsAmount = []
    nodesName = []
    nodesLevel = []
    nodesAmount = []
    i = 0
    while i <= len(argsList) - 1:
        progsName.append(argsList[i])
        progsLevel.append(argsList[i+1])
        progsAmount.append(argsList[i+2])
        nodesName.append(argsList[i+3])
        nodesLevel.append(argsList[i+4])
        nodesAmount.append(argsList[i+5])
        i += 6
    i = 0 
    while i < len(nodesAmount):
        with open('{}.json'.format(progsName[i])) as f:
            a = json.load(f)
        with open('{}.json'.format(nodesName[i])) as g:
            b = json.load(g)
##async def timeCal(progDamage,progInstallTime,progHitInterval,progProjectileTime,progAmount,isProgMulti,nodeFirewall,nodeRegeneration,nodeAmount)
            takeOverTime = 0
            time = await timeCal(a['DPS'][progsLevel[i]], a['installTime'],a['hitInterval'],a['projectileTime'],progsAmount[i],a['isMulti'],b['firewall'][nodesLevel[i]],b['firewallRegeneration'],nodesAmount[i])
            if time is not None:
                takeOverTime += time
            elif time is None:
                await ctx.send("The node(s) is (are) unable to be taken over.")
                return 
            if progsName[i] == 'beamCannon':
                takeOverTime += 0.5 
            i += 1
    await ctx.send("Calculation finished! Node(s) was captured in " + str(takeOverTime) + " seconds (or " + str(takeOverTime // 60) + " minute(s) " + str(takeOverTime - minute * 60) + " second(s))")

@bot.command(description="Calculate the visibility of stealth program.", brief='`Alexa stealthCalc {scanner level} {stealth program} {level} {amount} {another stealth program} {level} {amount} (and so on)`')
async def stealthCalc(ctx,*,args):
    argsList = args.split()
    nodeLevel = argsList[0]
    progsName = []
    progsLevel = []
    progsAmount = []
    i = 1
    visibility = 0
    while i < len(argsList):
        progsName.append(argsList[i])
        progsLevel.append(argsList[i+1])
        progsAmount.append(argsList[i+2])
        i += 3
    with open('scanner.json','r') as b:
        c = json.load(b)
##async def stealthCal(visibility, stealthProgVisibility, stealthProgInstallTime):
    for i in range(0,len(progsName)):
        with open('{}.json'.format(progsName[i]),'r') as f:
            a = json.load(f)
            e = progsAmount[i]
        for d in range(1,int(e)+1):
            visibility += await stealthCal(c['visibility'][nodeLevel], a['visibility'][progsLevel[i]], a['installTime'])
    await ctx.send("Visibility needed to use all of the programs: {} visibility.".format(visibility))

@bot.command(description="We dont know what this does, maybe its an easter egg?", hidden = True)
async def suffer(ctx):
    embed = discord.Embed(color = 0xff0000)
    embed.add_field(name="The Bang Bang created everything. however there was never nothing, and thats why there is always nothing. nothing is everywhere, its so every you dont need a where", value = str, inline = False)
    await ctx.send(embed=embed)

@bot.command(description = "Lists nodeNames and keys aswell as programNames and keys", aliases = ['wtf'])
async def listitems(ctx):
    await ctx.send ("Programs: beamCannon (doesnt work with projCalc as beam is not a projectile) shuriken blaster maniac worm\n Nodes: codeGate (does not have filter emulation as of now) core serverFarm database coinMiner coinMixer scanner sentry turret blackIce guardian evolver,\n Keys: DPS (progs) firewall (Nodes)")

@bot.command(hidden = True)
async def killAmethysm(ctx):
    randkill = ["Gun", "Drowning", "Molchu"]
    chosenrandkill = random.choice(randkill)
    if chosenrandkill == "Gun":
        await ctx.send("Amethysm was shot by a gun! Bang! he's dead!")

    if chosenrandkill == "Drowning":
        await ctx.send("Molchu threw Amethysm off a glacier and he couldn't swim, :(")

    if chosenrandkill == "Molchu":
        await ctx.send("Molchu and Amethysm Dueled with swords, molchu stabs Amethysm and he dies :(")

@bot.command(hidden = True)
async def killCode(ctx):
    randkill = ["Gun", "Drowning", "Molchu"]
    chosenrandkill = random.choice(randkill)
    if chosenrandkill == "Gun":
        await ctx.send("CodeWritten was shot by a gun! Bang! he's dead!")

    if chosenrandkill == "Drowning":
        await ctx.send("Molchu threw CodeWritten off a glacier and he couldn't swim, :(")

    if chosenrandkill == "Molchu":
        await ctx.send("Molchu and CodeWritten Dueled with swords, molchu stabs CodeWritten and he dies :(")

@bot.command(hidden = True)
async def killMolchu(ctx):
    randkill = ["Gun", "Drowning", "Molchu"]
    chosenrandkill = random.choice(randkill)
    if chosenrandkill == "Gun":
        await ctx.send("Molchu was shot by a gun! Bang! he's dead!")

    if chosenrandkill == "Drowning":
        await ctx.send("CodeWritten threw Molchu off a glacier and he couldn't swim, :(")

    if chosenrandkill == "Molchu":
        await ctx.send("Molchu and CodeWritten Dueled with swords, CodeWritten stabs molchu and he dies :(")

@bot.command(brief = '`Alexa kill {member}`', description="Kill someone you hate. More death messages coming soon!")
async def kill(ctx,member:discord.Member=None):
    if member is None:
        await ctx.send("You decided to look around for someone to kill with your new gun, but there wasn't anyone nearby. You ended up killing yourself.")
    else:
        a = random.randint(1,10)
        if a == 1:
            await ctx.send(member.name + " was filled with " + ctx.author.name + "'s worms.")
        elif a == 2:
            await ctx.send(member.name + " was brutally killed after stating that beam cannon is better than shuriken.")
        elif a == 3:
            await ctx.send(member.name + " was dead trying to triple protector a node. They forgot they didn't have any protectors left.")
        elif a == 4:
            await ctx.send(member.name + " was captured by a hit of maniac in the face by " + ctx.author.name + ".")
        elif a == 5:
            await ctx.send(ctx.author.name + " successfully tricapped " + member.name + "'s base with only a level 1 worm.")
        elif a == 6:
            await ctx.send(member.name + " along with 3 other nodes were wraithed by " + ctx.author.name + ". That damn scanner didn't do it's job!")
        elif a == 7:
            await ctx.send(member.name + " was brutally killed in real life while doing SC Sector 13 mission.")
        elif a == 8:
            await ctx.send(member.name + " commited attacking " + ctx.author.name + "'s base without a protector.")
        elif a == 9:
            await ctx.send(member.name + "'s network cable was unplugged by their 3 years old brother while attacking " + ctx.author.name + ".")
        elif a == 10:
            await ctx.send(member.name + " was brutally triple-blastered by " + ctx.author.name + ".")

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
    if ctx.author.id in (525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208):
        authid= ctx.author
        embed = discord.Embed(color = 0x00ff00)
        embed.add_field(name="Shutdown Command Sent, Bot Rebooting in 3 seconds", value = "Sent By {}".format(authid), inline = False)
        await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await bot.close()
        os.execl(sys.executable, sys.executable, * sys.argv)
    else:
##        embed = discord.Embed(color = 0xff0000)
##        embed.add_field(name="Sorry, you aren't allowed to use this command. Are you the admin of the server you are executing this in? DM CodeWritten#4044 to be added to the exceptions list!", value = None, inline = False)
        await ctx.send("Sorry, you aren't allowed to use this command. Are you the admin of the server you are executing this in? DM CodeWritten#4044 to be added to the exceptions list!")



bot.run(botToken)

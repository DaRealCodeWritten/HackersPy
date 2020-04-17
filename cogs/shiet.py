from discord.ext import commands
CodeWLogin= 0
AmethysmLogin= 0
THKLogin= 0
CodeWPassword= "awaitYourMum"
AmethysmPassword= "None"
THKPassword= "None"
class shiet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    async def pleaseendme(self, ctx):
        await ctx.author.send("Please end me")
        await ctx.send("Please end me") 


    @commands.command(hidden = True)
    async def login(self, ctx, args1):
        execuser = ctx.author.id
        if execuser in (436646726204653589, 525334420467744768, 419742289188093952):
            if execuser == 419742289188093952 and args1 == THKPassword:
                THKLogin = 1
                await ctx.send("Welcome, THK")

            elif execuser == 525334420467744768 and args1 == AmethysmPassword:
                AmethysmLogin = 1
                await ctx.send("Welcome, Amethysm")

            elif execuser == 436646726204653589 and args1 == CodeWPassword:
                CodeWLogin = 1
                await ctx.send("Welcome, [God]CodeWritten")

            else:
                await ctx.send("UserID or Password was wrong, check again")

        else:
            genAcc = ctx.author.display_name
            genAccLogin = 0
            genAccPassword = "GenericPassword"
            if args1 == genAccPassword:
                genAccLogin = 1
                await ctx.send(f"Welcome, {genAcc}")
    
    @commands.command(hidden = True)
    async def logout(self, ctx):
        execuser = ctx.author.id
        if execuser in (436646726204653589, 525334420467744768, 419742289188093952):
            if execuser == 436646726204653589:
                CodeWLogin = 0
                await ctx.send("Bye bye, [God]CodeWritten")

            if execuser == 525334420467744768:
                AmethysmLogin = 0
                await ctx.send("Bye bye, Amethysm")

            if execuser == 419742289188093952:
                THKLogin = 0
                await ctx.send("Bye bye, THK")

    @commands.command(hidden = True)
    async def passwd(self, ctx, args1):
        execuser = ctx.author.id
        if execuser in (436646726204653589, 525334420467744768, 419742289188093952):
            if execuser == 436646726204653589:
                if CodeWLogin == 1:
                    CodeWPassword = args1
                    await ctx.send(f"Password changed to {args1}")
                elif CodeWLogin != 1:
                    await ctx.send("Sorry [God]CodeWritten, you can only perform this action whilst logged in")
            if execuser == 525334420467744768:
                if AmethysmLogin == 1:
                    AmethysmPassword = args1
                    await ctx.send(f"Password changed to {args1}")
                elif AmethysmLogin != 1:
                    await ctx.send("Sorry Amethysm, you can only perform this action whilst logged in")
            if execuser == 419742289188093952:
                if THKLogin == 1:
                    THKPassword = args1
                    await ctx.send(f"Password changed to {args1}")
                elif THKLogin != 1:
                    await ctx.send("Sorry THK, you can only perform this action whilst logged in")
            

def setup(bot):
    bot.add_cog(shiet(bot))

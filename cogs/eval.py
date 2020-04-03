import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in [382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952]
    return commands.check(predicate)

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eval', hidden = True)
    @is_owner()
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        if ctx.author.id in (382534096427024385, 525334420467744768, 436646726204653589, 218142353674731520, 218590885703581699, 212700961674756096, 355286125616562177, 270932660950401024, 393250142993645568, 210939566733918208, 419742289188093952):
            env = {
                'ctx': ctx,
                'bot': self.bot,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                'source': inspect.getsource
            }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))
        
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

def setup(bot):
    bot.add_cog(Eval(bot))

import discord, os
from discord.ext import commands
from lib import tools
 
def listup():
    return os.listdir("./cogs")

class Ping(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.tree.command(name="addon", description="modify some addons")
    async def reload(self, ctx, option: Option(str, "목표설정", choices=["reload", "unload", "load"]), target: Option(str, "재시작할 cogs 선택", choices=(listup()))):
        await ctx.send(listup())
        cogs = tools.Cogs(bot=self.bot)
        if option == "reload": #나중에 최적화 해놔라
            cogs.reload(target[:-3])
        if option == "load": #나중에 최적화 해놔라
            cogs.reload(target)
        await ctx.respond(f"{target} {option} OK!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('aa')

    @commands.tree.command(name="aa2", description="modify some addons")
    async def aa2(self, ctx):
        await ctx.respond("AAA")
 
async def setup(app):
    await app.add_cog(Ping(app))
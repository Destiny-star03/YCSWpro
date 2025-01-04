from discord.ext import commands
from discord import app_commands
import discord

class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @commands.command("테스트") #슬래시 커맨드가 아닌 단순한 prefix 커맨드(기본값: !)
    async def upload(self, ctx: commands.Context):
        await ctx.send("테스트!")

    @commands.command("따라해")
    async def upload(self, ctx: commands.Context):
        try:
            msg = (ctx.message.content).split(" ")
        except Exception as E:
            print(E)
        await ctx.send(msg[1])

    @commands.command("이채널")
    async def upload(self, ctx: commands.Context):
        await ctx.send(ctx.message.channel)

# Cog 등록
async def setup(bot):
    await bot.add_cog(slash(bot))

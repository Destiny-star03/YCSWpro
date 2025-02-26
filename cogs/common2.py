import discord
from discord.ext import commands
from discord import app_commands
import requests

class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @commands.command("테스트") #슬래시 커맨드가 아닌 단순한 prefix 커맨드(기본값: !)
    async def upload(self, ctx: commands.Context):
        await ctx.send("테스트!")


# Cog 등록
async def setup(bot):
    await bot.add_cog(slash(bot))

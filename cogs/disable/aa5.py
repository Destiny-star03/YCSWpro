from discord.ext import commands
from discord import Option
from lib import tools
import os

class aa3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="업데이트", description="reload some addons")
    async def reload(self, ctx):
        await ctx.respond("업데이트 OK!")



# Cog 등록
def setup(bot):
    bot.add_cog(aa3(bot))

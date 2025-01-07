import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
import requests, re
from bs4 import BeautifulSoup

def clener(text):
    result = re.sub(r"[*N\s]", "", text)
    return result


class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @commands.command("테스트") #슬래시 커맨드가 아닌 단순한 prefix 커맨드(기본값: !)
    async def upload(self, ctx: commands.Context):
        await ctx.send("테스트!")

    @app_commands.command(name="공지사항", description="학교 홈페이지에 있는 공지사항을 확인합니다.")
    async def gongji(self, interaction: discord.Interaction):

        try:
            ycpage = requests.get("http://www.yc.ac.kr/yonam/web/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000590")
            soup = BeautifulSoup(ycpage.text, 'html.parser')
            test_elements = soup.find_all('td')#, class_='td_subject')

            message = ""

            for a in test_elements:
                if 'td_subject' in a.get('class', []):
                    message += f"## [{clener(a.text)}](http://www.yc.ac.kr/yonam/web/cop/bbs/selectBoardArticle.do?bbsId=BBSMSTR_000000000590&nttId=77326&searchBBS=&mblDn=&pageIndex=1&searchCnd=0&searchWrd=&adminSearchYn=N)\n"
                elif 'td_datetime' in a.get('class', []):
                    message += f"-# {clener(a.text)}\n\n"
            await interaction.response.send_message(message, ephemeral=False)

        except Exception as E:
            print(E)
            await interaction.response.send_message(E, ephemeral=False)

        

# Cog 등록
async def setup(bot):
    await bot.add_cog(slash(bot))

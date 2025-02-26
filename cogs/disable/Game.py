from discord.ext import commands
from discord import app_commands
import discord, asyncio, time, random
from discord import ButtonStyle, Interaction, Embed, VoiceClient
from discord.ui import View, Button
from discord.ext.commands import Bot
from lib.tools import clock, Revolver, SoundAsset
import os

ASSET_SOUNDS = os.path.join(os.path.dirname(__file__), "..", "assets/sounds")

def asset_reload(DView, sounds):
    for i in range(len(sounds)): #사운드 리스트에서 하나씩 리턴함
        button = discord.ui.Button(style=discord.ButtonStyle.gray, label=f"{i+1}: {sounds[i]}", custom_id=str(i))#, emoji=bt_list[i])
        try: DView.add_item(button)
        except ValueError:
            print("밸류 에러")
    return DView


async def voice_connect(self, interaction): #나중에 모듈화 해서 글로벌 하게 사용하기
    voice: VoiceClient = None
    connection: VoiceClient
    for connection in self.bot.voice_connections: #voice_connections run.py 메인
        if connection.channel.id == interaction.user.voice.channel.id:
            voice = connection
            break
    if voice == None:
        old_connection = interaction.guild.voice_client
        if old_connection != None:
            await old_connection.disconnect()
            self.bot.voice_connections.remove(old_connection)
        voice = await interaction.user.voice.channel.connect()
        self.bot.voice_connections.append(voice)
    return voice

class Game(commands.Cog,):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        # print(f'{self.bot.user}의 슬래시 커맨드가 동기화되었습니다.')

    @app_commands.command(name="타이머", description="시간 포메팅")
    @app_commands.describe(option="시간")
    async def choose(self, interaction: discord.Interaction, option: int):
        try:
            print(clock(option))
            await interaction.response.send_message(clock(option))
        except Exception as E:
            print(E)

    @commands.command("사운드")#사운드나 패키지로 함수 하나로 수정해놔라. ex(asset_play)
    async def upload(self, ctx: commands.Context):
        channel = self.bot.get_channel(1075726581642838096)
        embed = Embed(title=f"사운드에셋: 로딩중", description=f"")
        menu = await channel.send(embed=embed)
        
        self.sounds = os.listdir(ASSET_SOUNDS)
        page_len = (len(self.sounds) // 25) + 1
        for i in range(page_len):
            view = View(timeout=9e9**2)
            if i == 0:
                refresh_btn = Button(
                    style=ButtonStyle.primary,
                    label="새로고침",
                    custom_id="refresh"
                )
                refresh_btn.callback = self.upload
                view.add_item(refresh_btn)

            start = i * 25
            end = (i + 1) * 25
            if i == 0:
                end -= len(view.children)

            sound_frag = self.sounds[start:end]
            for ii, sound in enumerate(sound_frag): #사운드 리스트에서 하나씩 리턴함
                index = str((i * 25) + ii)
                button = Button(style=ButtonStyle.gray, label=f"{index}: {sound}", custom_id=index)
                button.callback = self._on_button_click
                view.add_item(button)

            embed = Embed(title=f"로드: {len(self.sounds)}개", description=f"")
            await menu.edit(embed=embed, view=view)

    async def _on_button_click(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            voice = await voice_connect(self, interaction)
            sound = SoundAsset(self.bot, voice)
            key = interaction.data["custom_id"]
            if key.isdigit():
                audio_name = self.sounds[int(key)]
                await sound.play(f"{ASSET_SOUNDS}/{audio_name}")
        except Exception as E:
            print(E)

    # async def timeout_button(self, view, button, message, timeout):
    #     await asyncio.sleep(timeout)  # 타임아웃 대기
    #     button.disabled = True  # 버튼 비활성화
    #     await message.edit(view=view)  # 메시지 업데이트

    #     # 타임아웃 메시지 전송
    #     await message.channel.send("시간이 초과되었습니다. 버튼이 비활성화되었습니다.")
        

    @app_commands.command(name="러시안룰렛", description="한명이 남을때까지 계속되는 살인게임") #파티참가를 클래스로 잘 수정해놔라.
    async def roulette(self, interaction: discord.Interaction):
        try:
            party = []
            embed = Embed(title=f"러시안 룰렛", description=f"시작: {clock(10+1)}")
            async def wait(view, button, timeout):
                await asyncio.sleep(timeout)
            async def join(interaction: discord.Interaction):
                player = interaction.user.name
                await interaction.response.defer()
                if not player in party: party.append(player) #파티에 참가한 유저를 리스트 업
                embed.set_field_at(0, name="현재 참가자", value=f"{'\n'.join(party)}", inline=False)
                await interaction.edit_original_response(embed=embed, view=view)
            view = View()
            join_btn = Button(
                style=ButtonStyle.primary,
                label="참가",
                custom_id="join"
            )
            join_btn.callback = join
            view.add_item(join_btn)
            embed.add_field(name=f"현재 참가자", value=f"없음", inline=False)

            await interaction.response.send_message(embed=embed, view=view)
            voice = await voice_connect(self, interaction)
            await wait(view, join_btn, 10)#class로 리볼버 객체 만들어서 사운드 조절할것 발당 나누기 해서 대기시간 줄여서 탄 많을수록 재장전 속도 빠르게하기
            join_btn.disabled = True  # 버튼 비활성화
            
            async def press(interaction: discord.Interaction, player):
                await interaction.response.defer()
                print(interaction.user.name, player)
                if not interaction.user.name == player:
                    await interaction.response.send_message("대체로, 남의 턴을 방해하는건 예의가 아니에요.", ephemeral=True) #ephemeral=True 나만보기

                triger_btn.disabled = True
                await revolver.triger()
                embed.set_field_at(0, name="조준...!", value=f"", inline=False)
                await interaction.edit_original_response(embed=embed, view=view)
                pass

            view = View()
            triger_btn = Button(
                style=ButtonStyle.primary,
                label="당긴다.",
                custom_id="triger",
                disabled=False
            )
            view.add_item(triger_btn)
            revolver = Revolver(self.bot, voice)    #객체 가져오기 이후 변수로 호출말곤 볼일없음

            for bullet in range(1, 6): #장전 턴 지날수록 사망확률 증가
                print(f"턴 시작! 총알 수: {bullet} 유저 수: {len(party)}")
                if len(party) == 1: break #나중에 한개로 하기
                

                embed.add_field(name=f"{bullet}발 재장전중...", value=f"", inline=False)
                await interaction.edit_original_response(embed=embed, view=view)
                await revolver.reload(bullet)

                for player in range(0, len(party)):
                    print("차례존 진입")
                    embed = Embed(title=f"러시안 룰렛", description=f"{party[player]}의 차례!")
                    embed.add_field(name=f"발포: {clock(5)}", value=f"", inline=False)
                    await interaction.edit_original_response(embed=embed, view=view)
                    triger_btn.callback = press
                    await asyncio.sleep(5)

                    print("게임 시작!")
                    await asyncio.sleep(1)
                    triger_btn.disabled = False
                    silnder = random.randint(bullet, 6)
                    
                    print(silnder)
                    if silnder == 6:
                        party.remove(party[player])
                        embed.set_field_at(0, name="사망!", value=f"", inline=False)
                        await revolver.shot()
                    if silnder != 6 and bullet == 6:
                        embed.set_field_at(0, name="불량탄이었네요.", value=f"", inline=False)
                    if silnder != 6:
                        embed.set_field_at(0, name="생존!", value=f"", inline=False)
                        await revolver.empty()
                    
                    await interaction.edit_original_response(embed=embed, view=view)
                    await asyncio.sleep(2)

                    if len(party) == 1:
                        print("게임종료!")
                        embed.set_field_at(0, name="게임종료! ", value=f"생존: {party[0]}", inline=False)
                        await interaction.edit_original_response(embed=embed, view=view)
                        break; break
        except Exception as E:
            print(f"에러! {E}")
            

# Cog 등록
async def setup(bot):
    await bot.add_cog(Game(bot))
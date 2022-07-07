import discord
import asyncio
import requests
from discord.ext import commands


class covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def covid(self, ctx, *, countryName = None):
        await ctx.channel.purge(limit=1)
        try:
            if countryName is None:
                embed=discord.Embed(title=":x: Не правильно вказана команда, спробуйте так: ```.covid country```", colour=0xff0000, timestamp=ctx.message.created_at)
                embed.add_field(name = "Якщо хочете побачити статистику у світі, то спробуйте команду:", value="```.covid world```", inline=True)
                embed.set_author(name="HorukraineBot's", icon_url="https://cdn.discordapp.com/avatars/986638946937237544/d393cefab2bf4298ca876b31a349616b.webp")
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.author.send(embed=embed)


            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]

                embed2 = discord.Embed(title=f"**COVID-19 статус в {country}**!", description="Ця інформація не завжди актуальна, тому вона може бути неточною!", colour=0x0000ff, timestamp=ctx.message.created_at)
                embed2.add_field(name="**Всього випадків:**", value=totalCases, inline=True)
                embed2.add_field(name="**Сьогодні випадків:**", value=todayCases, inline=True)
                embed2.add_field(name="**Загальна кількість смертей:**", value=totalDeaths, inline=True)
                embed2.add_field(name="**Сьогодні смерті:**", value=todayDeaths, inline=True)
                embed2.add_field(name="**Одужали:**", value=recovered, inline=True)
                embed2.add_field(name="**Активні випадки:**", value=active, inline=True)
                embed2.add_field(name="**Критичні:**", value=critical, inline=True)
                embed2.add_field(name="**Випадків на один мільйон:**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Смерті на один мільйон:**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Загальні тести:**", value=totalTests, inline=True)
                embed2.add_field(name="**Тести на мільйон:**", value=testsPerOneMillion, inline=True)
                embed2.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed2.set_author(name = "HorukraineBot's", icon_url = "https://cdn.discordapp.com/avatars/986638946937237544/d393cefab2bf4298ca876b31a349616b.webp")
                embed2.set_thumbnail(url='https://www.upload.ee/image/14236852/_________-2.png')
                await ctx.send(embed=embed2)

        except:
            embed3 = discord.Embed(title="Недійсна назва країни або помилка з API! Спробуйте ще раз..! Назви країн вказуйте лише на англійській мові.", colour=0xff0000, timestamp=ctx.message.created_at)
            embed3.set_author(name=":x: Error!")
            embed2.set_footer(name="HorukraineBot's",icon_url="https://cdn.discordapp.com/avatars/986638946937237544/d393cefab2bf4298ca876b31a349616b.webp")
            await ctx.author.send(embed=embed3)


def setup(bot):
    bot.add_cog(covid(bot))
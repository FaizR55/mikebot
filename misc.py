import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import os, os.path, requests, random
from async_timeout import timeout
from functools import partial
import openai

class Misc(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='news', aliases=['berita', 'n'], description="Return random news")
    async def news(self, ctx):

        try:
            async with ctx.typing():
                url = "https://lapi.kumparan.com/v2.0/rss/"

                response = requests.get(url)

                soup = BeautifulSoup(response.content, features="xml")

                news_item = []
                items = soup.find_all("item")
                # print(items)

                for item in items:

                    try:
                        title = item.title.text
                        encoded = item.encoded.text
                        image = item.enclosure['url']
                        url = item.original_url.text
                    except Exception as e:
                        continue

                    content = ""
                    soup = BeautifulSoup(encoded, 'html.parser')
                    p_tags = soup.find_all('p')
                    for p in p_tags:
                        # print(p.get_text())
                        content += p.get_text()+'\n'

                    # print("url = "+url) 
                    # print("title = "+title)
                    # print("image = "+image)
                    # print("content = "+content)

                    # news = {"title":title, "url":url, "image":image, "content":content}
                    # news_item.append(json.dumps(news))
                    
                    news_item.append([title,url,image,content])

                # print(news_item)
                random_news = random.choice(news_item)

                news = random_news[3]
                description = (news[:1995] + '...') if len(news) > 1995 else news

                embed = discord.Embed(title = random_news[0], description = description, url = random_news[1])
                embed.set_image(url = random_news[2])
            await ctx.send(embed=embed)

        except Exception as e:
            print(news_item)
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='gpt', aliases=['chat'], description="ChatGPT")
    async def gpt(self, ctx, *, message):
        try:
            async with ctx.typing():
                print("GPT MSG = "+message)
                # Set the OpenAI API key
                openai.api_key = os.getenv("gpt_token")

                # Use the OpenAI API to generate a response to the message
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": message}]
                    )
                response_text = response.choices[0].message.content
                chunks = split_text(response_text)

            for i, chunk in enumerate(chunks):
                await ctx.send(chunk)

        except Exception as e:
            print(str(e))
            await ctx.send("An error occured, please try again")
            # await ctx.send(f"An error occurred: {str(e)}")


def split_text(text, max_chunk_size=1995):
    chunks = []
    while len(text) > max_chunk_size:
        chunk, text = text[:max_chunk_size], text[max_chunk_size:]
        chunks.append(chunk)
    chunks.append(text)
    return chunks

def setup(bot):
    bot.add_cog(Misc(bot))
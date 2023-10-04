import discord
from discord.ext import commands
import sqlite3

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saved_images = {}  # Dictionary to store saved images
        
        # Initialize the SQLite database
        self.conn = sqlite3.connect('image_filenames.db')
        self.c = self.conn.cursor()

        # Create the table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS saved_images (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            url TEXT
        )''')
        self.conn.commit()

    @commands.command()
    async def save(self, ctx, *, filename):
        # Check if the message contains attachments
        if ctx.message.attachments:
            # Save the first attached image
            attachment = ctx.message.attachments[0]

            # Insert the specified filename and URL into the database
            self.c.execute("INSERT INTO saved_images (filename, url) VALUES (?, ?)",
                        (filename, attachment.url))
            self.conn.commit()

            await ctx.send(f'Saved image as {filename}')
        else:
            await ctx.send('No image attached.')

    @commands.command(name='image', aliases=['img'], description="Send saved image")
    async def image(self, ctx, *, filename):
        # Query the database to retrieve the URL based on the filename
        self.c.execute("SELECT url FROM saved_images WHERE filename=?", (filename,))
        result = self.c.fetchone()

        if result:
            image_url = result[0]
            await ctx.send(image_url)
        else:
            await ctx.send(f'Image "{filename}" not found in the database.')

    @commands.command()
    async def list_images(self, ctx):
        # Query the database to retrieve all saved image filenames
        self.c.execute("SELECT filename FROM saved_images")
        results = self.c.fetchall()

        if results:
            image_list = "\n".join([result[0] for result in results])
            embed = discord.Embed(
                title="List of Saved Images",
                description=image_list,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send('No saved images found.')

    @commands.command()
    async def clear_images(self, ctx, *, filename=None):
        if filename:
            # Delete the specific image by filename
            self.c.execute("DELETE FROM saved_images WHERE filename=?", (filename,))
        else:
            # Delete all rows from the saved_images table
            self.c.execute("DELETE FROM saved_images")
        
        self.conn.commit()

        if filename:
            await ctx.send(f'Image "{filename}" has been deleted from the database.')
        else:
            await ctx.send('All saved images have been cleared from the database.')


def __del__(self):
    self.conn.close()

def setup(bot):
    bot.add_cog(Image(bot))
import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def teste(self, ctx):
        await ctx.send('Your command was received!')

    @commands.command()
    async def list_channels(self, ctx):
        """Lists all active channels in the server."""

        # Create an embed object
        embed = discord.Embed(
            title="Active Channels",
            description=f"List of active channels in {ctx.guild.name}",
            color=discord.Color.blue()
        )

        # Iterate through the channels and add them to the embed
        for index, channel in enumerate(ctx.guild.channels, start=1):
            embed.add_field(name=f"Channel {index}", value=channel.mention, inline=False)

        # Send the embed to the channel
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))

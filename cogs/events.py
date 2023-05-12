import aiohttp
import discord
from discord.ext import commands
import json


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        print(f"{message.author}(#{message.channel.name}): {message.content}")
        guild = discord.utils.get(self.bot.guilds, name=message.guild.name)
        target_channel = discord.utils.get(guild.channels, name=message.channel.name)

        if self.bot.user.mentioned_in(message):
            print(f"bot mentioned: {message.content}")
            if target_channel is not None:
                prompt = await get_last_messages_from_channel(target_channel, 30)
                summary, res = await make_agent_summarize("Skali", prompt)
                await message.channel.send(summary)

        if message.content in ["some", "values"]:
            self.bot.dispatch("custom_event", message)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_custom_event(self, message):
        # custom event
        print(f"bbbb")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f"{self.bot.user} has disconnected from Discord!")


async def get_last_messages_from_channel(channel, limit=10):
    print(f"Target Channel: {channel}")
    last_messages = [message async for message in channel.history(limit=limit)]
    last_messages = last_messages[::-1]  # reverse the list

    # print("Context of the last 30 messages in the channel:")
    message_groups = []
    current_user = None
    current_group = []
    for msg in last_messages:
        if msg.author != current_user:
            if current_user is not None:
                message_groups.append((current_user, current_group))
            current_user = msg.author
            current_group = [msg.content]
        else:
            current_group.append(msg.content)
    if current_user is not None:
        message_groups.append((current_user, current_group))

    prompt = ""
    for user, messages in message_groups:
        print(f"{user}(#{channel.name}): {';'.join(messages)}")
        prompt += f"{user.name}: {';'.join(messages)}"
    # Add a line to request a summary
    prompt += "\nSummary:"
    return prompt


async def make_agent_summarize(agent_name, prompt):
    print(f"Asking {agent_name} summarize: {prompt}")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://localhost:7437/api/agent/{agent_name}/chat",
            json={"prompt": prompt},
        ) as response:
            api_response = await response.json()
            inner_json = json.loads(api_response["response"])
            res = inner_json["response"]
            summary = inner_json["summary"]
            print(f"{agent_name}'s summary: {summary}")
            return summary, res


async def setup(bot):
    await bot.add_cog(Events(bot))

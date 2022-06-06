import disnake
from disnake.ext import commands
from modules.client import CustomClient


class EventsCog(commands.Cog):
    def __init__(self, client: CustomClient):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening,
                                                                    name="радио Зоны"))
        await self.client.database.load_channels()
        print("КПК запущен.")

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or message.guild is None:
            return
        if message.author.id in self.client.database.all_users:
            server_channel = await self.client.fetch_channel(
                self.client.database.get_channel(user_id=message.author.id)["_id"]
            )
            try:
                await server_channel.send(
                    embed=await self.client.message_manager.create_embed(user=message.author, message=message)
                )
            except:
                await message.add_reaction("❌")
            else:
                await message.add_reaction("✅")
            return
        elif message.channel.id in self.client.database.all_channels:
            user_channel = await self.client.fetch_user(
                self.client.database.get_channel(channel_id=message.channel.id)["user"]
            )
            try:
                await user_channel.send(
                    embed=await self.client.message_manager.create_embed(user=message.author, message=message)
                )
            except:
                await message.add_reaction("❌")
            else:
                await message.add_reaction("✅")
            return


def setup(client):
    client.add_cog(EventsCog(client))

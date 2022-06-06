import disnake
from disnake.ext import commands
from modules.client import CustomClient
import json

settings = json.load(open("jsons/message_settings.json", encoding='utf-8-sig'))


class CommandsCog(commands.Cog):
    def __init__(self, client: CustomClient):
        self.client = client

    @commands.slash_command(
        name="create-contact",
        description="Создать контакт")
    async def command_create(
            self, inter: disnake.ApplicationCommandInteraction,
            user: str = commands.Param(
                description="Введите id пользователя."),
            character: str = commands.Param(
                description="Выберите персонажа",
                choices=list(settings['characters'].keys()))):
        user = await self.client.fetch_user(int(user))
        channel = await self.client.channel_manager.create_channel(
            user=user, character=character
        )
        await channel.send("Начало переписки.")
        await inter.send("Готово")

    @commands.slash_command(
        name="delete-contact",
        description="Удалить контакт")
    async def command_delete(
            self, inter: disnake.ApplicationCommandInteraction,
            channel: disnake.TextChannel = commands.Param(
                description="Выберите канал.")):
        if channel.id not in self.client.database.all_channels:
            await inter.send("Такого контакта не существует.")
        await self.client.channel_manager.delete_channel(channel=channel)
        await inter.send("Готово")


def setup(client):
    client.add_cog(CommandsCog(client))

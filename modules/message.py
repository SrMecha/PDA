import datetime
import disnake
import json


class MessageManager:
    def __init__(self, client, owner_ids: list):
        self.owner_ids = owner_ids
        self.client = client
        self.settings = json.load(open("jsons/message_settings.json", encoding='utf-8-sig'))

    async def get_character(self, user, channel):
        if user.id in self.owner_ids:
            channel = self.client.database.get_channel(channel_id=channel.id)
            return channel['character']
        return None

    async def create_embed(self, user, message):
        character = await self.get_character(user, message.channel)
        time = datetime.datetime.now(datetime.timezone.utc)
        if character is None:
            embed = disnake.Embed(
                title="Личное сообщение:",
                description=message.content,
                color=disnake.Color(0x28830a)
            )
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            embed.set_thumbnail(url="https://i.imgur.com/IH9SEqW.png")
            embed.set_footer(text=f"{time:%H:%M %d.%m.%Y}")
            return embed
        embed = disnake.Embed(
            title="Личное сообщение:",
            description=message.content,
            color=disnake.Color(0x28830a)
        )
        embed.set_author(name=self.settings["characters"][character]['name'],
                         icon_url=self.settings["characters"][character]['avatar_url'])
        embed.set_thumbnail(url="https://i.imgur.com/IH9SEqW.png")
        embed.set_footer(text=f"{time:%H:%M %d.%m.%Y}")
        return embed


class ChannelManager:
    def __init__(self, client, contact_category_id: int, guild_id: int):
        self.client = client
        self.contact_category_id = contact_category_id
        self.guild_id = guild_id

    async def create_channel(self, user, character: str = "sidorovich"):
        guild: disnake.Guild = self.client.get_guild(self.guild_id)
        time = datetime.datetime.utcnow()
        channel = await guild.create_text_channel(
            name=f">{user.name}",
            category=await guild.fetch_channel(self.contact_category_id),
            topic=f"**Контакт:** {user.name}\n**ID:**{user.id}\n**Создан:** {time:%H:%M %d.%m.%Y}"
        )
        await self.client.database.add_channel(channel_id=channel.id, user_id=user.id, character=character)
        return channel

    async def delete_channel(self, channel):
        await self.client.database.remove_channel(channel_id=channel.id)
        await channel.delete()

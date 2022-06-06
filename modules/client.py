import disnake
from disnake.ext import commands
from modules.database import ChannelsDatabaseManager
from modules.message import MessageManager, ChannelManager


class CustomClient(commands.Bot):
    """Кастомный клиент дискорда. Выполняет те же функции что и обычный,
    но лучше использовать его для подсказок."""
    def __init__(self, mongo_key):
        intents = disnake.Intents.default()
        super().__init__(intents=intents, test_guilds=[983423676529655888])
        self.remove_command('help')
        self.database = ChannelsDatabaseManager(mongo_key)
        self.message_manager = MessageManager(self, [652472617667788801])  # 521108970283335695
        self.channel_manager = ChannelManager(
            client=self,
            contact_category_id=983423798588096552,
            guild_id=983423676529655888
        )

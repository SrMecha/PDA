import motor.motor_asyncio
import asyncio


class ChannelsDatabaseManager:
    def __init__(self, mongo_key):
        cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_key)
        cluster.get_io_loop = asyncio.get_running_loop
        db = cluster.pda
        self.channels_db = db.channels
        self.all_channels = {}
        self.all_users = {}

    async def load_channels(self):
        async for channel in self.channels_db.find():
            self.all_channels[channel['_id']] = channel
            self.all_users[channel['user']] = channel['_id']

    def get_channel(self, channel_id: int = 0, user_id: int = 0):
        if channel_id:
            return self.all_channels.get(channel_id, None)
        elif user_id:
            return self.all_channels.get(self.all_users[user_id], None)

    async def add_channel(self, channel_id: int, user_id: int, character: str):
        db_dict = {
            "_id": channel_id,
            "user": user_id,
            "character": character
        }
        self.all_channels[channel_id] = db_dict
        self.all_users[user_id] = channel_id
        await self.channels_db.insert_one(db_dict)

    async def remove_channel(self, channel_id: int):
        channel_dict = self.get_channel(channel_id)
        self.all_users.pop(channel_dict['user'])
        self.all_channels.pop(channel_id)
        await self.channels_db.delete_one({"_id": channel_id})

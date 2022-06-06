import os
from dotenv import load_dotenv
from modules.client import CustomClient

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
mongo_key = os.environ.get("MONGO_KEY")
client = CustomClient(mongo_key)
client.load_extension(f"cogs.commands")
client.load_extension(f"cogs.events")
client.run(TOKEN)

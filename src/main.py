import os
from dotenv import load_dotenv
from seafood import client

load_dotenv()

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
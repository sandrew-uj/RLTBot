import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER = int(os.getenv("OWNER"))

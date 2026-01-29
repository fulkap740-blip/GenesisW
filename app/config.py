import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

OFFERS = {
    1: {"name": "White Bird", "rate": 1.5},
    2: {"name": "Genesis", "rate": 2.0}
}
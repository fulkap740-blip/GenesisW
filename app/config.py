import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

OFFERS = {
    "White Bird": {"rate": 1.5},
    "Genesis": {"rate": 2.0},
}

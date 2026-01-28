import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8592190715:AAEEAMjH32I23ekBJyXcxuxpOvsMHVaDeDc")
ADMIN_PASSWORD = os.getenv("Su54us")

OFFERS = {
    1: {"name": "White Bird", "rate": 1.5},
    2: {"name": "Genesis", "rate": 2.0}
}
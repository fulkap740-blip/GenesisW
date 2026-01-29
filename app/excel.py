from openpyxl import Workbook
from config import OFFERS

def build_excel(requests):
    wb = Workbook()
    ws = wb.active
    ws.append(["User ID", "Offer", "Video", "Proof", "Views", "Amount", "Status"])

    for r in requests:
        ws.append([
            r["user_id"],
            OFFERS[r["offer_id"]]["name"],
            r["video"],
            r["proof"],
            r["views"],
            r["amount"],
            r["status"]
        ])

    filename = "requests.xlsx"
    wb.save(filename)
    return filename
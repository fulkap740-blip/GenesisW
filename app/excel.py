from openpyxl import Workbook

def make_excel(rows):
    wb = Workbook()
    ws = wb.active
    ws.append(["User ID", "Offer ID", "Video", "Proof", "Views", "Amount", "Status"])

    for r in rows:
        ws.append(r)

    path = "requests.xlsx"
    wb.save(path)
    return path
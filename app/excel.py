from openpyxl import Workbook

def create_excel(requests):
    wb = Workbook()
    ws = wb.active
    ws.append(["User ID", "Offer", "Video", "Proof", "Views", "Amount", "Status"])

    for r in requests:
        ws.append(r)

    path = "requests.xlsx"
    wb.save(path)
    return path
from openpyxl import Workbook


def create_excel(rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Requests"

    ws.append([
        "User ID",
        "Offer",
        "Video Link",
        "Proof Link",
        "Views",
        "Amount",
        "Status",
        "Created"
    ])

    for row in rows:
        ws.append(row)

    path = "requests.xlsx"
    wb.save(path)
    return path
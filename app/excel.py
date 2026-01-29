from openpyxl import Workbook


def create_excel(rows, filename):
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

    wb.save(filename)
    return filename

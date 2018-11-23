import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

wochen = {
    "Mon": "Mo",
    "Tue": "Di",
    "Wed": "Mi",
    "Thu": "Do",
    "Fri": "Fr",
    "Sat": "Sa",
    "Sun": "So"
}
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


wochentag = time.strftime("%a")
wochentag = wochen[wochentag]
w_string = wochentag + ".\xa0" + time.strftime("%d.%m")

def in_to_database(args):
    spende = {"user": None, "type": None, "value": None, "negativ" : False}
    for a in args:
        if a == "-":
            spende["negativ"] = True
        elif a.isdigit() or a.lstrip("-").isdigit() or a.lstrip("+").isdigit():
            spende["value"] = int(a)
        elif str(a) == "K" or str(a) == "k":
            spende["type"] = "Kristal"
        elif str(a) == "S" or str(a) == "s":
            spende["type"] = "Siegel"
        else:
            spende["user"] = str(a).lower()

    for e in spende:
        if spende[e] == None:
            return -3

    sheett = client.open('Test')
    if spende["type"] == "Kristal":
        sheet = sheett.get_worksheet(0)
        try:
            day = sheet.row_values(1)
            names = sheet.col_values(5)
        except Exception as e:
            print(e + "Problem with day & names")
            return -1

    elif spende["type"] == "Siegel":
        sheet = sheett.get_worksheet(1)
        try:
            day = sheet.row_values(2)
            names = sheet.col_values(5)
        except Exception as e:
            print(e + "Problem with day & names")
            return -1
    column = 0
    day_ex = False
    for d in day:
        column+=1
        if d == w_string:
            day_ex = True
            break
    row=0
    user_ex = False
    for n in names:
        row+=1
        if n.lower() == spende["user"]:
            user_ex = True
            break

    if not user_ex:
        return -2
    elif not day_ex:
        return -1

    curr = sheet.cell(row,column).value.replace(".", "")
    if spende["negativ"]:
        new = "=" + curr + "-" + str(spende["value"])
    else:
        new = "="+curr+"+"+str(spende["value"])
    sheet.update_cell(row,column,new)

    val = sheet.cell(row, 4).value


    return val


def kontostand(user):
    sheett = client.open('Test')
    user = user[0].lower()
    val = []
    sheet = [sheett.get_worksheet(0), sheett.get_worksheet(1)]
    for s in sheet:
        names = s.col_values(5)
        user_ex = False
        row = 0
        for n in names:
            row += 1
            if n.lower() == user:
                user_ex = True
                break
        if not user_ex:
            return -2
        else:
            val.append(s.cell(row, 4).value)
            val.append(s.title)
    return val
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

scope = None
creds = None
client = None

wochen = {
    "Mon": "Mo",
    "Tue": "Di",
    "Wed": "Mi",
    "Thu": "Do",
    "Fri": "Fr",
    "Sat": "Sa",
    "Sun": "So"
}

def into_google_init():
    global scope
    global creds
    global client
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

def get_Data(type):
    global scope
    global creds
    global client

    try:
        sheett = client.open('Nazgul')
    except Exception as e:
        print(e)
        client = gspread.authorize(creds)
        sheett = client.open('Nazgul')

    metadaten = sheett.fetch_sheet_metadata()["sheets"]

    if type == "Kristal":
        for mdata in metadaten:
            if mdata["properties"]["title"] == "Kristall-System":
                sheet = sheett.get_worksheet(mdata["properties"]["index"])
                return sheet

    elif type == "Siegel":
        for mdata in metadaten:
            if mdata["properties"]["title"] == "Münzen-System":
                sheet = sheett.get_worksheet(mdata["properties"]["index"])
                return sheet
    elif type == "ein":
        for mdata in metadaten:
            if mdata["properties"]["title"] == "vgl-SzuE":
                sheet = sheett.get_worksheet(mdata["properties"]["index"])
                return sheet
    else:
        print("daten blatt nicht vorhabend")
        return -1

def in_to_database(args):
    wochentag = time.strftime("%a")
    wochentag = wochen[wochentag]
    w_string = wochentag + ".\xa0" + time.strftime("%d.%m")
    spende = {"user": None, "type": None, "value": None, "negativ" : False}
    for a in args:
        if a == "-":
            spende["negativ"] = True
        elif a.isdigit() or a.lstrip("-").isdigit() or a.lstrip("+").isdigit():
            spende["value"] = int(a)
        elif str(a) == "K" or str(a) == "k":
            spende["type"] = "Kristal"
            day_row = 1
        elif str(a) == "S" or str(a) == "s":
            spende["type"] = "Siegel"
            day_row = 2
        else:
            spende["user"] = str(a).lower()

    for e in spende:
        if spende[e] == None:
            return -3
    sheet = get_Data(spende["type"])
    if sheet == -1:
        return -1
    try:
            day = sheet.row_values(day_row)
            names = sheet.col_values(5)
    except Exception as e:
            print(str(e) + "Problem with day & names")
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
        print("Day is "+str(w_string))
        return -4

    curr = sheet.cell(row,column).value.replace(".", "")
    if spende["negativ"]:
        new = "=" + curr + "-" + str(spende["value"])
    else:
        new = "="+curr+"+"+str(spende["value"])

    sheet.update_cell(row,column,new)
    val = sheet.cell(row, 4).value
    return val

def kontostand(user):
    global scope
    global creds
    global client
    if user:
        user = user[0].lower()
        val = []
        sheets = [get_Data("Kristal"),get_Data("Siegel")]
        if sheets[0] ==-1 or sheets[1] ==-1:
            return -1
        for s in sheets:
            try:
                    names = s.col_values(5)
            except Exception as e:
                    print(str(e) + "Problem with day & names")
                    return -1
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
    else:
        return -2

def oeffnen(args):
        wochentag = time.strftime("%a")
        wochentag = wochen[wochentag]
        w_string = wochentag + ".\xa0" + time.strftime("%d.%m")
        user =  args[0]
        sheet = get_Data("ein")
        if sheet ==-1:
            return -1
        try:
                day = sheet.row_values(1)
                names = sheet.col_values(1)
        except Exception as e:
                print(str(e) + "Problem with day & names")
                return -1

        column = 0
        day_ex = False
        for d in day:
            column+=1
            if d == w_string:
                day_ex = True
                break
        row = 0
        user_ex = False
        for n in names:
            row +=1
            if n.lower() == user.lower():
                user_ex = True
                break
        if not user_ex:
            return -2
        curr = sheet.cell(row,column).value
        new = "="+curr+"+"+"1"
        sheet.update_cell(row,column,new)
        return 0

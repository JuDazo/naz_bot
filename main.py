import asyncio
import discord
import SECRET, STATICS
import into_GoogleTab

client = discord.Client()

@client.event
@asyncio.coroutine
def in_to_database(args, client, ret, message):
    spende = {"user": None, "type": None, "value": None, "negativ" : None}
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

    if spende["negativ"]:
        spende["value"] = "-"+str(spende["value"])
    if ret == -1:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
        'Die Spende konnte nicht eingetragen werden bitte melde dich bei JuDazo das du den Fehler mit den Code -1 gefunden hast danke')))
    elif ret == -2:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
        'Der angegebene Username %s konnte nicht in der Tabelle gefunden werden \n' % (spende["user"]))))
    elif ret == -3:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
        'Bitte versuche es noch ein mal und gib diesmla alle wichtigen informationen an. \n Denk daran das Format ist'
        ' "Spende Menge Art Username" \n Art = S für Siegel \n Art = K für Kristalle\n Die Menge der Kristalle oder Sigel bitte nicht mit "." oder "," trennen' )))
    else:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
                'Spende Eingetragen:\n%s hat %s %s gespendet \nDanke das sie das Automatische spendensystem von Dän '
                'verwenden:)' % (spende["user"], spende["value"], spende["type"]))))
        ret=ret.replace(".", "")
        if int(ret) < 0 :
            yield from client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description=(
                'Du musst noch : %s %s Spenden)' % (ret.replace("-", ""),spende["type"]))))
        else:
            yield from client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description=(
                    'Du hast ein guthaben von: %s %s )' % (ret.replace("+", ""), spende["type"]))))

@client.event
@asyncio.coroutine
def on_ready():
    print("Bot is logged in seccessfully. Running on servers:\n")
    for s in client.servers:
        print(s)
        print("- %s (%s)"% (s.name , s.id))
    yield from client.change_presence(game=discord.Game(name="Ich bin das spenden luder"))


def kontostand(ret,message):
    if ret == -2:
        yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
            'Der angegebene Username konnte nicht in der Tabelle gefunden werden \n' )))
    else:
        yield from client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description=(
                "Dein Kontostand beim "+ret[1]+" beträgt "+ret[0]+" und beim "+ret[3]+" beträgt er "+ret[2])))


@client.event
@asyncio.coroutine
def on_message(message):
    if message.author.display_name != STATICS.BOT:
        if not message.attachments:
            if str(message.channel) == STATICS.CHANNEL:
                    if message.content.lower().startswith(STATICS.Spende.lower()):
                        args = message.content.split(" ")[1:]
                        ret = into_GoogleTab.in_to_database(args)
                        yield from in_to_database(args, client, ret,message)
                    elif message.content.lower().startswith(STATICS.Konto.lower()):
                            args = message.content.split(" ")[1:]
                            ret = into_GoogleTab.kontostand(args)
                            yield from kontostand(ret,message)
                    elif message.content.lower().startswith(STATICS.Eintag):
                            args = message.content.split(" ")[1:]
                            ret = into_GoogleTab.oeffnen(args)
                            #yield from kontostand(ret,message)
                    else:
                        yield from client.send_message(message.channel,
                        embed=discord.Embed(color=discord.Color.red(), description=
                        ('Das angegebene Format der Spende war nicht Richtig du hast das Key Wort "Spende" vergessen\n bitte halte dich an das Format:'
                        '\n"Spende Menge Art Username" \n Art = S für Siegel \n Art = K für Kristalle \nDanke :)')))

into_GoogleTab.into_google_init()
client.run(SECRET.TOKEN)

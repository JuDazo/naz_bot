import asyncio
import discord
import SECRET, STATICS
import into_GoogleTab

client = discord.Client()

@client.event
@asyncio.coroutine
def ret_val(args, client, ret, message):
        spende = {"user": None, "type": None, "value": None, "negativ" : None}
        if args:
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
            'Error 101 Bitte schnellst möglich Judazo per pn bescheid geben danke')))

        elif ret == -2:
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
            'Der angegebene Username konnte nicht in der Tabelle gefunden werden \n' )))
        elif ret == -3:
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
            'Bitte versuche es noch ein mal und gib diesmla alle wichtigen informationen an. \n Denk daran das Format ist'
            ' "Spende Menge Art Username" \n Art = S für Siegel \n Art = K für Kristalle\n'
            'Die Menge der Kristalle oder Sigel bitte nicht mit "." oder "," trennen' )))
        elif ret == -4:
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
            'Error 404 Bitte schnellst möglich Judazo per pn bescheid geben danke \n' )))

        elif ret == 0:
            yield from client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description=(
            'die geöffnete q wurde eingetragen \n' )))
        else:
            if isinstance(ret, (list,)):
                yield from client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description=(
                "Dein Kontostand beim "+ret[1]+" beträgt "+ret[0]+" und beim "+ret[3]+" beträgt er "+ret[2])))
            else:
                ret=ret.replace(".", "")
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=(
                    'Spende Eingetragen:\n%s hat %s %s gespendet' % (spende["user"], spende["value"], spende["type"]))))
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

@client.event
@asyncio.coroutine
def on_message(message):
    if message.author.display_name != STATICS.BOT:
        if not message.attachments:
            if str(message.channel) == STATICS.CHANNELW or str(message.channel) == STATICS.CHANNELF or str(message.channel) == STATICS.CHANNELA:
                    if message.content.lower().startswith(STATICS.Spende.lower()):
                        args = message.content.split(" ")[1:]
                        ret = into_GoogleTab.in_to_database(args)
                        yield from ret_val(args, client, ret,message)
                    elif message.content.lower().startswith(STATICS.Konto.lower()):
                            args = message.content.split(" ")[1:]
                            ret = into_GoogleTab.kontostand(args)
                            yield from ret_val(None,client,ret,message)
                    elif message.content.lower().startswith(STATICS.Eintag):
                            args = message.content.split(" ")[1:]
                            ret = into_GoogleTab.oeffnen(args)
                            yield from ret_val(None,client,ret,message)
                    else:
                        yield from ret_val(None,client,-3,message)
            elif str(message.channel) == STATICS.KUMMER:
                yield from client.send_message(client.get_channel('536127648368427008'), embed=discord.Embed(color=discord.Color.red(), description=(message.content)))
                yield from client.delete_message(message)


into_GoogleTab.into_google_init()
client.run(SECRET.TOKEN)

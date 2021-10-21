import requests
import discord
from discord.ext import tasks
from bs4 import BeautifulSoup as bs
from random import seed
from random import random

seed(1)

ips = [ "http://178.63.17.151:3128",
        "http://195.64.232.33:3128",
        "http://185.38.111.1:8080"]

TOKEN = #Token
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------------')
    send.start()

@tasks.loop(seconds=random()*10+50)
async def send():
    ipNum = round(random()*2)
    proxyDict = {
        "http"  : ips[ipNum], 
        "https" : ips[ipNum], 
        "ftp"   : ips[ipNum]
    }
    url = requests.get("https://www.cryptogame-tracker.com/pvu/", proxies=proxyDict)
    print(url.status_code)
    print(ips[ipNum])
    htmlinfo = bs(url.content, 'html.parser')
    channel = client.get_channel(875171350279512084)
    for tbody in htmlinfo.find_all("tbody"):
        for tr in tbody.find_all("tr"):
            data = []
            links = 0
            for td in tr.find_all("td"):
                data.append(td.text.strip())
                for a in td.find_all("a", href=True):
                    data.append(a["href"])
                    links += 1
            if links == 2:
                embed=discord.Embed(title="Plant Check - " + data[2]+"(UTC)", description="["+data[0]+" / "+data[1]+"] - "+data[2]+"(UTC)\nPlant: "+data[4]+"\nTerrain: "+data[6], color=discord.Color.green())
                embed.set_thumbnail(url="https://s2.coinmarketcap.com/static/img/coins/200x200/11130.png")
                print(embed)
                await channel.send(embed=embed)

client.run(TOKEN)

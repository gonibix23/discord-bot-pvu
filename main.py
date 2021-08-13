import requests
import discord
from discord.ext import tasks
from bs4 import BeautifulSoup as bs
from random import seed
from random import random

seed(1)

ips = [ "http://178.63.17.151:3128",
        "http://173.212.228.57:3128",
        "http://91.227.139.215:22222",
        "http://195.64.232.33:3128",
        "http://51.81.22.176:3128",
        "http://185.38.111.1:8080",
        "http://51.81.32.81:8888",
        "http://178.18.255.175:3128",
        "http://83.136.184.194:9991"]

TOKEN = 'ODc1MjA4MjkyODkxMjM0MzI0.YRSLPQ._qXY5fJ6fOhAYvFrAu7ne7uOzxU'
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------------')
    send.start()

@tasks.loop(seconds=random()*10+20)
async def send():
    ipNum = round(random()*8)
    proxyDict = {
        "http"  : ips[ipNum], 
        "https" : ips[ipNum], 
        "ftp"   : ips[ipNum]
    }
    url = requests.get("https://www.cryptogame-tracker.com/pvu/", proxies=proxyDict)
    print(url.status_code)
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

#!/usr/bin/env python



import os 
import discord
from dotenv import load_dotenv
import requests
from datetime import datetime

JSON_URL = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/prueba.json'

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN2")
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

dates = requests.get(JSON_URL).json()


def parser(dates):
    def dec_fechas(func):
        format_fechas = lambda x: datetime.strptime(x, "%d/%m/%Y")
        fechas = {k:format_fechas(fecha) for k, fecha in dates.items()}
        def wrapper_dec():
            content = func(fechas)
            return tuple([(f'{k} ->{v}') for k,v in content.items()])
        return wrapper_dec
    return dec_fechas

@parser(dates)
def fecha(fechas):
    return {k:datetime.strftime(v, "%d/%m/%Y") for k,v in fechas.items()}



@parser(dates)
def cuanto_falta(fechas):
    return {k: f' faltan {(v - datetime.now()).days} dias' for k,v in fechas.items()}



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == 'fecha!':
        response = fecha()
        await message.channel.send('\n'.join(response))
    if message.content == 'cuanto!':
        response = cuanto_falta()
        await message.channel.send('\n'.join(response))


client.run(TOKEN)

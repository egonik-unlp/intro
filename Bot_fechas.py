import os 
import discord
from dotenv import load_dotenv
import requests
from datetime import datetime
import json
import random 

JSON_URL = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/prueba.json'
JSON_UND = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/unidades.json'
JSON_COMP = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/comp.json'
JSON_HELP = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/help.json'
# JSON_COND = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/cond.json'



load_dotenv()
#Hay un token extra porque os.getenv es una cagada
#TOKEN = 
TOKEN = os.getenv("DISCORD_TOKEN2")
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord! For help and a command list, type h! in the chat, y nuestros goblins te van a dar una mano")
    #pasar esto al espeañol asasp 


dates = requests.get(JSON_URL).json()
unidades = requests.get(JSON_UND).json()
compuestos = requests.get(JSON_COMP).json()
Help = requests.get(JSON_HELP).json() #va con mayus para que no tome la función 
# cond = requests.get(JSON_COND).json()


def parser(dates):
    def dec_fechas(func):
        format_fechas = lambda x: datetime.strptime(x, "%d/%m/%Y")
        fechas = {k:format_fechas(fecha) for k, fecha in dates.items()}
        def wrapper_dec():
            content = func(fechas)
            return tuple([(f'{k} ->{v}') for k,v in content.items()])
        return wrapper_dec
    return dec_fechas

#Printeo lista json de unidades, super senicllo. Hay que llenar el json y pero es bastante straightforward
def get_quote():
  quote = unidades
  return(quote)


#Placeholder para f(x) con lista de compuesto/nombre: Tengo que armar todo (ej compuesto! O2: rta oxigeno)
def get_quote2():
  quote2 = compuestos
  return(quote2)

#simple help function 
def get_help():
#hay que armar un json con toda la lista de comandos, etc y contacto
    quote3 = Help 
    return(quote3)

# def get_cond():
#     quote4 = cond 
#     return(quote4)


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
    if message.content == 'h!':
        quote = get_help()
        await message.channel.send(quote)
    if message.content == 'fecha!':
        response = fecha()
        await message.channel.send('\n'.join(response))
    if message.content == 'cuanto!':
        response = cuanto_falta()
        await message.channel.send('\n'.join(response))
    #este par está con startwith, después lo cambio a ==
    if message.content.startswith('unidades!'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('compuesto!'):
        quote = get_quote2()
        await message.channel.send(quote)


client.run(TOKEN)

import os 
import json
import discord
from dotenv import load_dotenv
from collections import Counter
import requests
from functools import wraps 
from datetime import datetime
import json
import random 

JSON_URL = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/prueba.json'


load_dotenv()
#Hay un token extra porque os.getenv es una cagada
#TOKEN = mitoken
TOKEN = os.getenv("DISCORD_TOKEN2")
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

counter = Counter()
try:
    with open('counter.json', 'r') as file:
        counter.update(json.load(file))
except FileNotFoundError:
    pass


dates_aux = requests.get(JSON_URL).json()
format_fechas = lambda x: datetime.strptime(x, "%d/%m/%Y")
dates = {k:format_fechas(v) for k,v in dates_aux.items()}


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord! For help and a command list, type h! in the chat, y nuestros goblins te van a dar una mano")

def logger(counter):
    def logger_wrapper(func):
        @wraps(func)
        def counter_wrapper(*args, **kwargs):
            counter[func.__name__] += 1
            with open('counter.json', 'w') as file:
                json.dump(counter, file)
            return func(*args, **kwargs)
        return counter_wrapper
    return logger_wrapper
    


def parser(func):
    @wraps(func)
    def dec_fechas(*args, **kwargs):
        content = func(*args, **kwargs)
        return tuple([(f'{k} -> {v}') for k,v in content.items()])
    return dec_fechas



#Printeo lista json de unidades, super senicllo. Hay que llenar el json y pero es bastante straightforward
def get_quote():
  response = requests.get("https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/unidades.json")
  json_data = json.loads(response.text)
  quote = json_data
  return(quote)


#Placeholder para f(x) con lista de compuesto/nombre: Tengo que armar todo (ej compuesto! O2: rta oxigeno)
def get_quote2():
  response = requests.get("https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/comp.json")
  json_data2 = json.loads(response.text)
  quote2 = json_data2
  return('el compuesto es' + quote2)

#simple help function 
def get_help():
    response = requests.get("")#hay que armar un json con toda la lista de comandos, etc y contacto
    json_data3 = json.loads(response.text)
    quote3 = json_data3 
    return(quote3)

@logger(counter)
@parser
def fecha(fechas):
    return {k:datetime.strftime(v, "%d/%m/%Y") for k,v in fechas.items()}


@logger(counter)
@parser
def cuanto_falta(fechas):
    return {k: f' faltan {(v - datetime.now()).days} dias' for k,v in fechas.items() if (v - datetime.now()).days > 0 }

@client.event
async def on_message(message):
    if message.author == client.user:
        return    
    if message.content == 'h!':
        quote = get_help()
        await message.channel.send(quote)
    if message.content == 'fecha!':
        response = fecha(dates)
        await message.channel.send('\n'.join(response))
    if message.content == 'cuanto!':
        response = cuanto_falta(dates)
        await message.channel.send('\n'.join(response))
    #este par está con startwith, después lo cambio a ==
    if message.content.startswith('unidades!'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('compuesto!'):
        quote = get_quote2()
        await message.channel.send(quote)


client.run(TOKEN)

import json
import os
import random

import discord
import requests
from replit import db
from keep_alive import keep_alive
# token= MTEzNjg2ODE4MjYyMDEzMTM5OA.GKn_VT.ZBETbfbqi_Y5rEd7WNBMSTxyfiCjA87_M5ApeY
client = discord.Client(intents=discord.Intents.default())
sad_words = ['sad', 'depressed', 'unhappy', 'miserable', 'saddening']
s_encouragements = ['cheer up!', 'hwaiting!!', 'hang in there!']

if 'responding' not in db.keys():
  db['responding'] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_d = json.loads(response.text)
  quote = json_d[0]['q'] + '-' + json_d[0]['a']
  return (quote)


def update_encourage(encouraging_msg):
  if "encouragements" in db:
    encouragements = db['encouragements']
    encouragements.append(encouraging_msg)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_msg]


def delete_encourage(index):
  encouragements = db['encouragements']
  if (len(encouragements) > index):
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  if msg.startswith("hello"):
    await message.channel.send("Hello")
  if msg.startswith("inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  if (db['responding']):
    options = s_encouragements
    if 'encouragements' in db:
      options.extend(db['encouragements'])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('new'):
    encouraging_msg = msg.split('new ', 1)[1]
    update_encourage(encouraging_msg)
    await message.channel.send('new encouraging msg added!')

  if msg.startswith('del'):
    encouragements = []
    if 'encouragements' in db:
      index = int(msg.split("del", 1)[1])
      delete_encourage(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith('list'):
    encouragements = []
    if 'encouragements' in db:
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith('responding'):
    value = msg.split('responding ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('responding is on')
    else:
      db['responding'] = False
      await message.channel.send('responding is off')


keep_alive()
client.run(os.getenv('token'))

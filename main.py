import discord 
import requests
import os
import json
from keep_started import keep_started
import cricscore
import pyjokes
import random


def basic_score():
    match = cricscore.ScoreGet()
    x = match.get_unique_id_and_results()
    reply = ""

    y = len(x.keys())
    if(y == 0):
        reply = "No Live Macthes."
    else:
        count=1
        for i in x.keys():
          if(x[i].split("\n")[-1]=="Scores Not Available."):
            pass
          else:
            reply = reply+"\n"
            reply = reply+"**"+str(count)+")** "+x[i]+"\n"
            reply = reply+"\n"
            count+=1
            if(len(reply) >= 1400):
                break
        if(count>1):
          reply = reply +"\nNote : For Full-Scorecard type ~1-{Match-Id} for 1st ininngs and ~2-{Match-Id} for 2nd ininngs.\n"
        else:
          reply="No Live Matches."
    return reply

client=discord.Client()

def get_quote():
  r=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(r.text)
  quote=json_data[0]['q']+"\n-"+json_data[0]['a']
  return quote

def get_single_line_joke():
  c=["all","chuck","neutral"]
  emoji=[":laughing::satisfied:",":joy:",":rofl:"]
  joke = pyjokes.get_joke(language='en', category=random.choice(c))
  joke=joke+"\n"+random.choice(emoji)+random.choice(emoji)+random.choice(emoji)
  return joke

def get_first_inning(id):
    x = cricscore.detailed_scorecard(id)
    msg_reply =[ "\n"+x["match"]+"\n\n","**Toss-winning-team : **"+x["toss-win"]+"\n\n"+"**1st Innings Scorecard : **\n\n" +\
        x["1-innings"]+"\n"]
    return msg_reply

def get_second_inning(id):
    x = cricscore.detailed_scorecard(id)
    msg_reply = ["\n"+x["match"]+"\n\n","**Toss-winning-team : **"+x["toss-win"]+"\n\n"+"**2nd Innings Scorecard : **\n\n" +\
        x["2-innings"]+"\n"]
    return msg_reply

@client.event
async def on_ready():
  print("We are logged in as {0.user}".format(client))



@client.event
async def on_message(message):
  if(message.author==client.user):
    return
  elif(message.content.lower().startswith("~hi") or message.content.lower().startswith("~hello") ):
    embed=discord.Embed(
    title="CriJoQuotiFy",
    description="Hello!,{0}\nMy Name is Crijoquotify.\nI am a Bot.\nI can tell you live Cricket scores,I can tell you an Inspiring quote Also I can tell you a joke.\nSo tell me,How can i help you??\nType '~Help' For Making be able to Talk to you.".format(message.author.mention),
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")

    await message.reply(embed=embed)
  elif(message.content.lower().startswith("~quote")):
    embed=discord.Embed(
    title="Inspiring Quote!",
    description=get_quote(),
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    await message.reply(embed=embed)

  elif(message.content.lower().startswith("~joke")):
    embed=discord.Embed(
    title="One Line Joke!",
    description=get_single_line_joke(),
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    await message.reply(embed=embed)
  
  elif(message.content.lower().startswith("~clear")):
    await message.channel.purge(limit=10)

  elif(message.content.lower().startswith("~live-scores")):
    embed=discord.Embed(
    title="Live Scores!!",
    description=basic_score(),
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    await message.reply(embed=embed)
    
  
  elif(message.content.lower().startswith("~1-")):
    id = int(message.content.lower().split("-")[1])
    r=get_first_inning(id)
    embed=discord.Embed(
    title=r[0],
    description=r[1],
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    await message.reply(embed=embed)
    
  
  elif(message.content.lower().startswith("~2-")):
    id = int(message.content.lower().split("-")[1])
    r=get_second_inning(id)
    embed=discord.Embed(
    title=r[0],
    description=r[1],
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    await message.reply(embed=embed)
    
  
  
  elif(message.content.lower().startswith("~help")):
    embed=discord.Embed(
    title="Help Page!",
    description="Help page to get started with the Bot.",
    colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    embed.set_footer(text="This is help page!")
    embed.set_author(name="CriJoQuotiFy",icon_url="http://3.bp.blogspot.com/-kkl69POMqkY/V6cufY2O90I/AAAAAAAAHUs/5Ldr3t98VuAOoh2EPpa9Xi9cUF6oHGyiQCHM/s1600/cricket-wallpapers.jpg")
    embed.add_field(name="~hi/~hello",value="Getting info about myself.",inline=False)
    embed.add_field(name="~live-scores",value="Get Live Cricket Match Scores.",inline=False)
    embed.add_field(name="~1-id",value="To get 1st Innings Scorecard of the Match.",inline=False)
    embed.add_field(name="~2-id",value="To get 2nd innings Scorecard of the Match.",inline=False)
    embed.add_field(name="~quote",value="Get a Inspiring Quote.",inline=False)
    embed.add_field(name="~joke",value="Get a joke.",inline=False)
    embed.add_field(name="~clear",value="Delete last 10 messages.",inline=False)
    embed.add_field(name="~help",value="Get List of Commands.",inline=False)
    await message.reply(embed=embed)
  elif(message.content.lower().startswith("~")):
    await message.reply("Something Went Wrong,Please Try Again Later!!!")



keep_started()
client.run(os.getenv('TOKEN'))

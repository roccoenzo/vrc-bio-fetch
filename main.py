from replit import db
# bot.py
import os
import random
from nextcord.ext import commands
import nextcord
from dotenv import load_dotenv
import vrchatapi
from vrchatapi.api import authentication_api, users_api
from pprint import pprint
import json
import gspread
from gspread.client import Client
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe





with vrchatapi.ApiClient(configuration) as api_client:
  auth_api = authentication_api.AuthenticationApi(api_client)
  current_user = auth_api.get_current_user()
  print("Logged in as:", current_user.display_name)
  def SearchDisplayname(username):
        api_instance = users_api.UsersApi(api_client)
        try:
            api_response = api_instance.search_users(search=username, n=1, offset=0)
            return(api_response)
        except vrchatapi.ApiException as e:
            print("Exception when calling UsersApi->search_users: %s\n" % e)

  def SearchUID(user_id):
        api_instance = users_api.UsersApi(api_client)
        try:
          api_response = api_instance.get_user(user_id)
          pprint(api_response)
        except vrchatapi.ApiException as e:
          print("Exception when calling UsersApi->get_user: %s\n" % e)



class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.danger)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.blurple)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        self.value = False
        self.stop()



load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game('Harvesting bios'))
    print('DISCORD: We have logged in as {0.user}'.format(bot))



@bot.command()
async def bio(ctx, arg):
  response = SearchDisplayname(arg)
  await ctx.message.delete()
  if(response):
    if(hasattr(response[0], 'bio')): 
      view = Confirm()
      embed = nextcord.Embed(title=response[0].display_name, 
                            url=response[0].user_icon, 
                            description="```{} ```".format(response[0].bio), color=nextcord.Color.red())
      embed.set_author(name=response[0].username,
                      url="https://vrchat.com/home/user/{}".format(response[0].id), 
                      icon_url=response[0].user_icon)

      embed.set_thumbnail(url=response[0].current_avatar_thumbnail_image_url)
    lastMessage = await ctx.send(embed=embed, view=view)
    await view.wait()

    if(view.value == False):
      await lastMessage.delete()

    if(view.value == True):
      db[response[0].display_name] =  (response[0].bio)
      print(db.keys())
      print(db[response[0].display_name])

      lastMessage.embeds[0].color = nextcord.Color.green()
      await lastMessage.edit(embed = lastMessage.embeds[0])


@bot.command()
async def uidbio(ctx, arg):
  response = SearchUID(arg)
  await ctx.message.delete()
  if(response):
    if(hasattr(response, 'bio')): 
      view = Confirm()
      embed = nextcord.Embed(title=response.display_name, 
                            url=response.user_icon, 
                            description="```{} ```".format(response.bio), color=nextcord.Color.red())
      embed.set_author(name=response.username,
                      url="https://vrchat.com/home/user/{}".format(response.id), 
                      icon_url=response.user_icon)

      embed.set_thumbnail(url=response.current_avatar_thumbnail_image_url)
    lastMessage = await ctx.send(embed=embed, view=view)
    await view.wait()

    if(view.value == False):
      await lastMessage.delete()

    if(view.value == True):
      db[response.display_name] =  (response.bio)
      print(db.keys())
      print(db[response[0].display_name])

      lastMessage.embeds[0].color = nextcord.Color.green()
      await lastMessage.edit(embed = lastMessage.embeds[0])



bot.run(TOKEN)

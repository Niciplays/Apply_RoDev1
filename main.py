import random
from wsgiref.simple_server import make_server
import discord
import requests
from discord.ext import commands
from threading import Thread
from flask import Flask
import os
from discord import Permissions


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
API_KEY = '5822b696e7d8af961c27229bf5b1a937'

# Define a dictionary to store user warnings
user_warnings = {}
ticket_channels = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    awa = random.randint(1, 4)
    if awa == 1:
        await ctx.send('Hello!')
    if awa == 2:
        await ctx.send('Hi human!')
    if awa == 3:
        await ctx.send('Hello fellow Homo Sapien!')
    if awa == 4:
        await ctx.send('Hi person!')

@bot.command()
async def roll(ctx):
    await ctx.send(f'Here is your number: {random.randint(1, 6)}')

@bot.command()
async def bye(ctx):
    awa = random.randint(1, 3)
    if awa == 1:
        await ctx.send('See you later crocodile!')
    if awa == 2:
        await ctx.send('Bye fellow Homo Sapien!')
    if awa == 3:
        await ctx.send('Bye human...')

@bot.command()
async def encourage(ctx):
    encourage = random.randint(1, 4)
    if encourage == 1:
        await ctx.send('"How wonderful it is that nobody need wait a single moment before starting to improve the world.” ~Anne Frank')
    elif encourage == 2:
        await ctx.send('"Start where you are. Use what you have. Do what you can.” ~Arthur Ashe')
    elif encourage == 3:
        await ctx.send('"Set your goals high, and don’t stop till you get there." ~Bo Jackson')
    elif encourage == 4:
        await ctx.send('“You just can’t beat the person who never gives up.” ~Babe Ruth')

@bot.command()
async def smart(ctx):
    awa = random.randint(1, 3)
    if awa == 1:
        await ctx.send('X = -80538738812075974, Y = 80435758145817515, and Z = 12602123297335631')
    if awa == 2:
        await ctx.send('32798727498124789375769807808')
    if awa == 3:
        await ctx.send('The answer is: 47539759375469085070770697890658709879508797580')

@bot.command()
async def lol(ctx):
    await ctx.send("Don't worry I'm not going to kill you...")


@bot.command()
async def image(ctx):
    # Load the image from a file
    file = discord.File("OIP.jpg")
    file2 = discord.File("th.jpg")
    file3 = discord.File("3.jpg")
    file4 = discord.File("4.jpg")
    file5 = discord.File("5.jpg")
    file6 = discord.File("6.jpg")
    image = random.randint(1, 6)
    if image == 1:
        await ctx.send(file=file)
    if image == 2:
        await ctx.send(file=file2)
    if image == 3:
        await ctx.send(file=file3)
    if image == 4:
        await ctx.send(file=file4)
    if image == 5:
        await ctx.send(file=file5)
    if image == 6:
        await ctx.send(file=file6)

@bot.command()
async def mute(ctx, member: discord.Member):
    # Get or create the "Muted" role
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        # Define channel overwrites
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            muted_role: discord.PermissionOverwrite(send_messages=False)
        }

        # Apply channel overwrites for all text channels
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(overwrites=overwrites)

    # Add the "Muted" role to the member
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been muted.")


@bot.command()
async def unmute(ctx, member: discord.Member):
    # Check if the "Muted" role exists
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        return await ctx.send("The 'Muted' role does not exist.")

    # Check if the member has the "Muted" role
    if muted_role not in member.roles:
        return await ctx.send(f"{member.mention} is not muted.")

    # Remove the "Muted" role from the member
    try:
        await member.remove_roles(muted_role)

        # Unmute the member in all text channels
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(member, send_messages=True)

        await ctx.send(f"{member.mention} has been unmuted.")
    except discord.Forbidden:
        await ctx.send("I don't have the necessary permissions to unmute members.")



@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    # Add a warning to the user
    if member.id not in user_warnings:
        user_warnings[member.id] = 1
    else:
        user_warnings[member.id] += 1

    await ctx.send(f"{member.mention} has been warned. Reason: {reason}. They now have {user_warnings[member.id]} warnings.")

@bot.command()
async def unwarn(ctx, member: discord.Member):
    # Check if the member has warnings
    if member.id in user_warnings:
        user_warnings[member.id] -= 1
        await ctx.send(f'A warning has been removed from {member.mention}. They now have {user_warnings[member.id]} warnings.')
    else:
        await ctx.send(f'{member.mention} does not have any warnings.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    # Check if the amount is within a valid range
    if 1 <= amount <= 100:
        await ctx.channel.purge(limit=amount + 1)  # Add 1 to include the command message
        await ctx.send(f'Cleared {amount} messages.', delete_after=5)  # Delete the confirmation message after 5 seconds
    else:
        await ctx.send('Please provide a number between 1 and 100 for the amount of messages to clear.')

# Set the bot's status to "Listening to !help"
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print(f'We have logged in as {bot.user}')

def get_weather(city):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        return f'Temperature in {city}: {temperature}°C, Weather: {weather_desc}'
    else:
        print(f'Failed to fetch weather data. Status code: {response.status_code}')
        print(response.text)  # Print the response content for debugging
        return 'Error: Unable to fetch weather data.'

# Define a command to get weather information
@bot.command()
async def weather(ctx, city):
    weather_info = get_weather(city)
    await ctx.send(weather_info)

@bot.command()
async def rules(ctx):
    rules_message = (
        "Welcome to the server!\n\n"
        "1. Spam a lot\n"
        "2. Exist\n"
        "3. Evade taxes\n"
        "4. Defenestrate nico\n"
        "5. idk"
        "\nFollow these rules to maintain a positive and friendly community!"
    )

    await ctx.send(rules_message)

@bot.command()
async def new_ticket(ctx, *, support_role_name="Support Team"):
    # Create a new ticket channel
    guild = ctx.guild
    author = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True)
    }

    # Get the support role by name
    support_role = discord.utils.get(guild.roles, name=support_role_name)
    if not support_role:
        await ctx.send(f"Support role '{support_role_name}' not found. Please provide a valid support role.")
        return

    overwrites[support_role] = discord.PermissionOverwrite(read_messages=True)

    channel = await guild.create_text_channel(f'ticket-{author.name}', overwrites=overwrites)
    ticket_channels[author.id] = channel.id

    # Mention the support team
    support_mention = f"{support_role.mention} "
    await ctx.send(f"A new ticket has been created for {author.mention}. {support_mention}please assist.")
    await channel.send(f"Ticket created by {author.mention}. {support_mention}please assist. {author.mention}ask your questions here.")

@bot.command()
async def close_ticket(ctx, *, support_role_name="Support Team"):
    author_id = ctx.author.id
    author_roles = [role.name for role in ctx.author.roles]

    # Check if the author has a role that grants them support privileges
    support_roles = [support_role_name, "Owner"]  # Replace with your support role name
    is_support_member = any(role in support_roles for role in author_roles)

    # Check if the author is the ticket owner or a support member
    if author_id in ticket_channels or is_support_member:
        channel_id = ticket_channels.get(author_id)
        if channel_id:
            channel = bot.get_channel(channel_id)
            if channel:
                # Mention the support team
                support_mention = f"{discord.utils.get(ctx.guild.roles, name=support_role_name).mention} "
                await channel.send(f"{support_mention}The ticket has been closed by {ctx.author.mention}.")
                await channel.delete()
                del ticket_channels[author_id]
                await ctx.send("Ticket closed.")
            else:
                await ctx.send("Ticket channel not found.")
        else:
            await ctx.send("You don't have an open ticket.")
    else:
        await ctx.send("You don't have permission to close tickets.")



@bot.command()
async def verify(ctx):
    # Check if the user is already verified
    if "Verified" in [role.name for role in ctx.author.roles]:
        await ctx.send("You are already verified.")
        return

    # Assign a "Verified" role to the user
    verified_role = discord.utils.get(ctx.guild.roles, name="Verified")
    if verified_role:
        await ctx.author.add_roles(verified_role)
        await ctx.send("You have been verified!")
    else:
        await ctx.send("The 'Verified' role was not found. Please contact the server admin.")

# Event to welcome new members and explain the verification process
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"Welcome, {member.mention}! Please use `!verify` to complete the verification process.")

# Event to assign the "Verified" role to bot owner upon startup
@bot.event
async def on_ready():
    bot_owner_id = 938889523822223371
    bot_owner = discord.utils.get(bot.get_all_members(), id=bot_owner_id)
    verified_role = discord.utils.get(bot_owner.guild.roles, name="Verified")

    if verified_role:
        await bot_owner.add_roles(verified_role)
        print(f"Bot owner '{bot_owner.display_name}' has been verified.")

@bot.command()
async def mute_voice(ctx, member: discord.Member):
    # Get the mute role
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if mute_role:
        await member.add_roles(mute_role)
        await ctx.send(f"{member.mention} has been muted.")
    else:
        await ctx.send("Mute role not found. Please set up a mute role.")

@bot.command()
async def unmute_voice(ctx, member: discord.Member):
    # Get the mute role
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if mute_role and mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted or mute role not found.")

@bot.command()
async def deafen(ctx, member: discord.Member):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    # Check if the bot is in the same voice channel as the member
    if ctx.voice_client and ctx.voice_client.channel == voice_channel:
        await member.edit(deafen=True)
        await ctx.send(f"{member.mention} has been deafened.")
    else:
        await ctx.send("You and the member need to be in the same voice channel.")

@bot.command()
async def undeafen(ctx, member: discord.Member):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    # Check if the bot is in the same voice channel as the member
    if ctx.voice_client and ctx.voice_client.channel == voice_channel:
        await member.edit(deafen=False)
        await ctx.send(f"{member.mention} has been undeafened.")
    else:
        await ctx.send("You and the member need to be in the same voice channel.")

@bot.command()
async def move(ctx, member: discord.Member, channel: discord.VoiceChannel):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    # Check if the bot is in the same voice channel as the member
    if ctx.voice_client and ctx.voice_client.channel == voice_channel:
        await member.move_to(channel)
        await ctx.send(f"{member.mention} has been moved to {channel.name}.")
    else:
        await ctx.send("You and the member need to be in the same voice channel.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode set to {seconds} seconds in this channel.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge_user(ctx, member: discord.Member, amount: int):
    def is_user_message(message):
        return message.author == member

    deleted = await ctx.channel.purge(limit=amount, check=is_user_message)
    await ctx.send(f'Deleted {len(deleted)} messages by {member.mention}.', delete_after=5)


# Function to fetch a random cat GIF
def get_random_cat_gif():
    api_url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['url']
    return None

# Command to send a random cat GIF
@bot.command()
async def gif(ctx):
    cat_gif_url = get_random_cat_gif()
    if cat_gif_url:
        await ctx.send(cat_gif_url)
    else:
        await ctx.send("Failed to fetch a cat GIF. Try again later.")

# Function to fetch a random fact
def get_fact():
    api_url = "https://uselessfacts.jsph.pl/random.json"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'text' in data:
            return data['text']
    return None

# Command to send a random fact
@bot.command()
async def fact(ctx):
    random_fact = get_fact()
    if random_fact:
        await ctx.send(random_fact)
    else:
        await ctx.send("Failed to fetch a random fact. Try again later.")

app = Flask('')

@app.route('/')
def home():
    return 'I am alive'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()






bot.run('MTE1MTA4MjEwNzg4ODczMDE2Mg.GnhzvJ.it06YM-GYwKz1odwLcWIWio1_u18Of-C0HRcMA')

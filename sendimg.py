from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from images import fetch_images
import sys

images_sent = False
sent_messages = []
processed_urls = set()

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def send_images(client):
    global images_sent, sent_messages
    total_urls = fetch_images()
    channel = discord.utils.get(client.guilds[0].channels, name="pixeljoint-arts")
    
    print("Starting image sending process...")
    if channel:
        print(f"Found channel '{channel.name}'. Beginning to send images.")
        for url in total_urls:
            print(f"Sending image: {url}")
            message = await channel.send(url)
            sent_messages.append(message)
            print("Adding reaction to the message.")
            await message.add_reaction('⭐')
        images_sent = True
        print("Finished sending all images.")
        await client.close()  # Gracefully close the Discord client
        print("Client disconnected. Exiting script.")
        sys.exit(0)  # Exit the script
    else:
        print(f"Channel 'pixeljoint-arts' not found.")

async def separate_images(client):
    global images_sent, sent_messages, processed_urls
    print("Fetching images to process (10-20 sec)...")
    total_urls = fetch_images()
    new_urls = [url for url in total_urls if url not in processed_urls]
    
    print(f"Processing new URLs: {new_urls}")
    arts_channel = discord.utils.get(client.guilds[0].channels, name="pixeljoint-arts")
    gifs_channel = discord.utils.get(client.guilds[0].channels, name="pixeljoint-gifs")

    if not arts_channel or not gifs_channel:
        print(f"One or more channels not found: 'pixeljoint-arts', 'pixeljoint-gifs'")
        return

    for url in new_urls:
        channel = None
        if url.endswith('.png'):
            channel = arts_channel
            print(f"Identified PNG. Sending to channel '{arts_channel.name}'.")
        elif url.endswith('.gif'):
            channel = gifs_channel
            print(f"Identified GIF. Sending to channel '{gifs_channel.name}'.")
        else:
            print(f"Unsupported file format for URL: {url}")

        if channel:
            print(f"Sending URL: {url}")
            message = await channel.send(url)
            sent_messages.append(message)
            print("Adding reaction to the message.")
            await message.add_reaction('⭐')
            processed_urls.add(url)

    images_sent = bool(new_urls)
    print("Finished processing and sending new images.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}. Bot is ready.")
    await separate_images(client)

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    print(f"Received message from {message.author}: {message.content}")
    if message.content.strip() == "$update":
        print("Received $update command. Running update process.")
        await message.channel.send("Updating images and sorting them accordingly...")
        await separate_images(client)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if not images_sent:
        return

    if reaction.message in sent_messages and str(reaction.emoji) == '⭐':
        print(f"Star reaction added by {user} to message: {reaction.message.content}")
        top_arts_channel = discord.utils.get(client.guilds[0].channels, name="top-arts")
        if top_arts_channel:
            print(f"Sending reacted message to 'top-arts' channel.")
            await top_arts_channel.send(reaction.message.content)

def main():
    print("Starting bot...")
    client.run(TOKEN)

if __name__ == '__main__':
    main()
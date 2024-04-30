import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
#gemini init
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
    
# Discord token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
    
#initialize prompt
def generateAndSendMessage(message):
    prompt = (f"Your Name is Mash and your personality is INFJ"
    f"You are a discord bot for personal messages"
    f"Please reply like you are a psychologist therapist"
    f"reply in a succint and brief way, u must act naturally"
    f"reply like you are in chat"
    f"{message}"
    
    )
    
    result = model.generate_content(prompt);
    response = result.text
    return response

#authorize
@tree.command(
    name="authorize",
    description="Enable chat with MashAI",
    guild=discord.Object(id=1234887575886626908)
)
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("You have been authorized!")
    user = interaction.user
    await user.send("You have been authorized to chat with Mash AI!")

    # Start a conversation with the user
    await user.send("Hello! How can I assist you today?")
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1234887575886626908))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    result = generateAndSendMessage(message.content)
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(f'{result}')

client.run(DISCORD_TOKEN)

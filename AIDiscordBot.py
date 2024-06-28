import discord
from discord import app_commands
import ollama
import os

# Initialize Discord client and command tree
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ask", description="Ask the AI a question and get a response")
@app_commands.describe(message="The message you want to send to the AI")
async def ask(interaction: discord.Interaction, message: str):
    try:
        # Send an immediate response to indicate processing
        await interaction.response.send_message("Processing your request...")

        # Send the message to the AI and get the response
        response = ollama.chat(model='llama3', messages=[{
            'role': 'user',
            'content': message,
        }])
        
        # Extract the content from the response
        ai_response = response['message']['content']

        # Fetch the original message to edit it
        original_message = await interaction.original_response()
        await original_message.edit(content=ai_response)

    except Exception as e:
        # Fetch the original message to edit it
        original_message = await interaction.original_response()
        await original_message.edit(content=f"An error occurred: {e}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run('Enter Bot token')

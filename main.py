import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
intents.reactions = True
intents.messages = True
intents.message_content = True
intents.typing = True
intents.emojis_and_stickers = True
intents.webhooks = True
intents.integrations = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("o!", "O!"), intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync failed: {e}")

#AVATAR COMMAND

@bot.command(name="avatar")
@commands.has_permissions(administrator=True)
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=discord.Color.orange()
    )
    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need Administrator permissions to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Couldn't find that user. Try mentioning them or using their exact name.")
    else:
        await ctx.send("Something went wrong. Please try again.")

@bot.tree.command(name="avatar", description="Get the avatar of a user.")
@app_commands.describe(user="The user whose avatar you want to fetch")
async def avatar(interaction: discord.Interaction, user: discord.User):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need Administrator permissions to use this command.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title=f"{user.name}'s Avatar",
        color=discord.Color.orange()
    )
    embed.set_image(url=user.display_avatar.url)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

#BOT STATUS

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name="akhiyaan")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

bot.run(TOKEN)
import disnake
from disnake.ext import commands

# Remplace par le token de ton bot
TOKEN = "VOTRE_TOKEN_ICI"

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True  # Nécessaire pour gérer les membres (ban, kick, mute)

bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} est en ligne !")
    await bot.change_presence(activity=disnake.Game("Change moi"))

# Commande pour bannir un utilisateur
@bot.slash_command(description="Bannir un membre du serveur")
@commands.has_permissions(ban_members=True)
async def ban(interaction: disnake.AppCmdInter, member: disnake.Member, reason: str = None):
    await member.ban(reason=reason)
    embed = disnake.Embed(title="Membre banni", description=f"{member} a été banni.", color=disnake.Color.red())
    await interaction.send(embed=embed)

# Commande pour expulser un utilisateur
@bot.slash_command(description="Expulser un membre du serveur")
@commands.has_permissions(kick_members=True)
async def kick(interaction: disnake.AppCmdInter, member: disnake.Member, reason: str = None):
    await member.kick(reason=reason)
    embed = disnake.Embed(title="Membre expulsé", description=f"{member} a été expulsé.", color=disnake.Color.orange())
    await interaction.send(embed=embed)

# Commande pour muter un utilisateur (exemple basique)
@bot.slash_command(description="Mettre un membre en sourdine")
@commands.has_permissions(manage_roles=True)
async def mute(interaction: disnake.AppCmdInter, member: disnake.Member):
    role = disnake.utils.get(interaction.guild.roles, name="Muted")
    if not role:
        role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    await member.add_roles(role)
    embed = disnake.Embed(title="Membre muet", description=f"{member} a été mis en sourdine.", color=disnake.Color.yellow())
    await interaction.send(embed=embed)

# Commande pour rétablir un utilisateur
@bot.slash_command(description="Rétablir un membre")
@commands.has_permissions(manage_roles=True)
async def unmute(interaction: disnake.AppCmdInter, member: disnake.Member):
    role = disnake.utils.get(interaction.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        embed = disnake.Embed(title="Membre rétabli", description=f"{member} a été rétabli.", color=disnake.Color.green())
        await interaction.send(embed=embed)
    else:
        await interaction.send("Ce membre n'est pas en sourdine.", ephemeral=True)

# Commande ping
@bot.slash_command(description="Vérifier la latence du bot")
async def ping(interaction: disnake.AppCmdInter):
    embed = disnake.Embed(title="Pong!", description=f"Latence : {bot.latency * 1000:.2f} ms", color=disnake.Color.blue())
    await interaction.send(embed=embed)

# Commande coucou
@bot.slash_command(description="Envoyer un message de salut")
async def coucou(interaction: disnake.AppCmdInter):
    embed = disnake.Embed(title="Salut!", description="Coucou! Comment ça va?", color=disnake.Color.teal())
    await interaction.send(embed=embed)

# Commande info-server
@bot.slash_command(description="Afficher les informations du serveur")
async def info_server(interaction: disnake.AppCmdInter):
    embed = disnake.Embed(title="Informations du Serveur", color=disnake.Color.purple())
    embed.add_field(name="Nom", value=interaction.guild.name)
    embed.add_field(name="Membres", value=interaction.guild.member_count)
    embed.add_field(name="Créé le", value=interaction.guild.created_at.strftime("%Y-%m-%d"))
    await interaction.send(embed=embed)

# Commande info-utilisateur
@bot.slash_command(description="Afficher les informations d'un utilisateur")
async def info_utilisateur(interaction: disnake.AppCmdInter, member: disnake.Member = None):
    if member is None:
        member = interaction.user
    embed = disnake.Embed(title="Informations de l'Utilisateur", color=disnake.Color.green())
    embed.add_field(name="Nom", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Créé le", value=member.created_at.strftime("%Y-%m-%d"))
    await interaction.send(embed=embed)

# Commande help
@bot.slash_command(description="Liste toutes les commandes disponibles")
async def help(interaction: disnake.AppCmdInter):
    embed = disnake.Embed(title="Liste des Commandes", color=disnake.Color.gold())
    embed.add_field(name="/ban @membre [raison]", value="Bannir un membre.")
    embed.add_field(name="/kick @membre [raison]", value="Expulser un membre.")
    embed.add_field(name="/mute @membre", value="Mettre un membre en sourdine.")
    embed.add_field(name="/unmute @membre", value="Rétablir un membre.")
    embed.add_field(name="/ping", value="Vérifier la latence du bot.")
    embed.add_field(name="/coucou", value="Envoyer un message de salut.")
    embed.add_field(name="/info_server", value="Afficher les informations du serveur.")
    embed.add_field(name="/info_utilisateur [@membre]", value="Afficher les informations d'un utilisateur.")
    await interaction.send(embed=embed)

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
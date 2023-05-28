import os

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import random

load_dotenv(dotenv_path="config")
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, description="Bot python")

#########################################################
# Lorsque le bot se connecte au serveur Discord
#########################################################
"""@bot.event
async def on_ready():
    print("Le bot est connecté")


##########################################################
# Lorsqu' un utilisateur entre une salutation
##########################################################
"""


@bot.event
async def on_ready():
    # CREATION D' UNE COMPTEUR DE SERVEUR DEFINISSANT LE NOMBRE DE SERVEUR AUQUEL EST CONNECTER LE BOT
    guild_count = 0

    # BOUCLE QUI PERMET D' AFFICHER LE NOMBRE DE SERVEUR AUQUEL LE BOT EST CONNECTER
    for guild in bot.guilds:
        # AFFICHE L' ID DU SERVEUR ET SON NOM
        print(f"- {guild.id} (nom: {guild.name})")

        # INCREMENTE LE COMPTEUR DE SERVEUR
        guild_count = guild_count + 1

    # AFFICHE DANS COMBIEN DE SERVEUR IL EST CONNECTER
    print("FLASH_BOT est dans " + str(guild_count) + " serveurs.")
    print("Le bot est pret !")


@bot.event
async def on_member_join(member):
    # LORSQU' UN MEMEBRE A REJOINS LE SERVEUR
    general_channel = client.get_channel(728983315005079556)
    # le canal general
    general_channel.send(f"Bienvenue sur le serveur {member.display_name} !")


@bot.event
async def on_message(message):
    # Vérifiez que le message n'a pas été envoyé par le bot lui-même pour éviter les boucles infinies.
    if message.author == bot.user:
        return

    # Si le message commence par !hello, le bot répondra avec une salutation aléatoire.
    if message.content.startswith('!hello'):
        salutations = ['Salut!', 'Bonjour!', 'Coucou!', 'Yo!']
        response = random.choice(salutations)
        await message.channel.send(response)

    # Si le message commence par ! Poll, le bot commencera un sondage en ajoutant des réactions aux messages.
    if message.content.startswith('!poll'):
        question = message.content[5:]  # Récupère la question du sondage à partir du message
        await message.channel.send("Sondage: " + question)
        await message.add_reaction('\U0001F44D')  # Ajoute une réaction pouce levé
        await message.add_reaction('\U0001F44E')  # Ajoute une réaction pouce baissé


@bot.command(name="info")
async def InfoServeur(ctx):
    serveur = ctx.guild
    nombreDeChainesTexte = len(serveur.text_channels)
    nombreDeChainesVocale = len(serveur.voice_channels)
    Description_du_serveur = serveur.description
    Nombre_de_personnes = serveur.member_count
    Nom_du_serveur = serveur.name
    message = f"Le serveur **{Nom_du_serveur}** contient *{Nombre_de_personnes}* personnes ! " \
              f"\nLa description du serveur est {Description_du_serveur}. " \
              f"\nCe serveur possède {nombreDeChainesTexte} " \
              f"salons écrit et {nombreDeChainesVocale} salon vocaux."
    await ctx.send(message)


@bot.event
async def sondage(ctx, message, question, *options):
    """
    Commande pour créer un sondage. Exemple d'utilisation: !sondage "Quel est votre animal préféré ?" "Chien" "Chat" "Poisson"
    """
    if message.content.startswith("!sondage"):
        # Vérifier que l'utilisateur a fourni des options
        if len(options) <= 1:
            await ctx.send("Vous devez fournir au moins deux options.")
            return

        # Créer l'embed pour le sondage
        embed = discord.Embed(title=question, color=0x00ff00)

        # Ajouter les options
        for i, option in enumerate(options):
            emoji = chr(0x1f1e6 + i)  # utiliser des émojis pour les options
            embed.add_field(name=f"{emoji} {option}", value="0", inline=False)

        # Envoyer le message avec l'embed
        message = await ctx.send(embed=embed)

        # Ajouter les réactions pour chaque option
        for i in range(len(options)):
            emoji = chr(0x1f1e6 + i)
            await message.add_reaction(emoji)

bot.run(os.getenv("TOKEN"))

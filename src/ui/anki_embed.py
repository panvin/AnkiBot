import disnake
from disnake import Colour

class AnkiEmbed():

    def batch_embed(self, guild, batch, deck_count):
        
        batch_member = self.get_member_or_role_from_id(guild = guild, id = batch.batch_member)
        batch_manager = self.get_member_or_role_from_id(guild = guild, id =batch.batch_manager)
        study_channel = self.get_channel_from_id(guild = guild, id = batch.study_channel)
        if batch.delay is None:
            delay = "Non défini"
        else:
            delay = batch.delay

        embed = disnake.Embed(title="Informations Batch", color=Colour.blue())
        details_title = "__Détails:__"
        details_value=f"**Nom:** {batch.batch_name} - **ID: {batch.id}**\n**Responsable:** {batch_manager}\n**Membres:** {batch_member}\n\n**Channel de travail:** {study_channel} - **Délai:** {delay} min(s)\n**Nombre de decks contenu dans la Promotion:** {deck_count}"
        help_title="__Commandes:__"
        help_value=f"__Modification du responsable:__\n `/update_batch_manager {batch.id} <@utilisateur>/<@rôle>`\n __Gestion des Batchs__: `/manage_batch`"

        embed.add_field(name = details_title, value = details_value, inline=False)
        embed.add_field(name = help_title,    value = help_value,    inline=False)
        return embed

    def deck_embed(self, guild, deck, card_count):
        
        deck_manager = batch_manager = self.get_member_or_role_from_id(guild = guild, id =deck.deck_manager)
        
        embed = disnake.Embed(title="Informations Deck", color=Colour.blue())
        details_title = "__Détails:__"
        details_value=f"**Nom:** {deck.deck_name} - **ID: **{deck.id}\n**Responsable:** {deck_manager}\n**Nombre de Cartes contenu dans le Deck:** {card_count}"
        help_title="__Commandes utilitaires__"
        help_value=f"__Ajout/Modification du responsable:__\t `/update_deck_manager {deck.id} <@utilisateur>/<@rôle>`\n __Gestion des decks__: `/manage_deck`"

        embed.add_field(name = details_title, value = details_value, inline=False)
        embed.add_field(name = help_title,    value = help_value,    inline=False)
        return embed

    def card_embed(self, card):
        
        embed = disnake.Embed(title="Informations Carte question", color=Colour.blue())
        details_title = "__Détails:__"
        details_value=f"**Nom:** {card.card_name} - **ID: **{card.id}"
        question_title = "__Question:__"
        question_value=f"{card.first_field}"
        answer_title = "__Réponse:__"
        answer_value=f"{card.second_field}"
        
        embed.add_field(name = details_title,  value = details_value,  inline=False)
        embed.add_field(name = question_title, value = question_value, inline=False)
        embed.add_field(name = answer_title,   value = answer_value,   inline=False)
        return embed


    def get_member_or_role_from_id(self, guild : disnake.Guild, id: int):
        member = disnake.utils.find(lambda member : member.id == id, guild.members)
        role = disnake.utils.find(lambda role : role.id == id, guild.roles)
        if role is not None:
            return role.mention
        elif member is not None: 
            return member.mention
        elif id is not None:
            return "Rôle ou Membre non reconnu"
        else:
            return "Non défini"

    def get_channel_from_id(self, guild : disnake.Guild, id: str):
        channel = disnake.utils.find(lambda channel : channel.id == id, guild.text_channels)
        if channel is None:
            return "Non défini"
        else: 
            return channel.mention

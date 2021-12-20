from sql import ValorSQL
from valor import Valor
from discord.ext.commands import Context
import discord
from util import ErrorEmbed, LongTextEmbed, LongFieldEmbed
import random
from datetime import datetime
import requests
import commands.common
from util import get_uuid

async def _register_link(valor: Valor):
    desc = "Links Discord ID to Minecraft UUID"
    
    @valor.command()
    async def link(ctx: Context, user: discord.Member, username: str):
        if "-" in username:
            return await ctx.send(embed=ErrorEmbed("Invalid user name")) # lazy sanitation 
        if not commands.common.role1(user):
            return await ctx.send(embed=ErrorEmbed("No Permissions"))

        exist = await ValorSQL._execute(f"SELECT * FROM id_uuid WHERE discord_id={user.id} LIMIT 1")
        uuid = get_uuid(username)
        if exist:
            await ValorSQL._execute(f"UPDATE id_uuid SET uuid='{uuid}' WHERE discord_id={user.id}")
        else:
            await ValorSQL._execute(f"INSERT INTO id_uuid VALUES ({user.id}, '{uuid}')")

        await LongTextEmbed.send_message(valor, ctx, f"Linking UUID for {username}", f"{user.id} to {uuid}", color=0xFF10)

    @link.error
    async def cmd_error(ctx, error: Exception):
        await ctx.send(embed=ErrorEmbed("<Insert something informative>..."))
        raise error
    
    @valor.help_override.command()
    async def link(ctx: Context):
        await LongTextEmbed.send_message(valor, ctx, "Link", desc, color=0xFF00)
    
    
    
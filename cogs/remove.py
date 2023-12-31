from typing import Optional
from discord.ext import commands
import discord
import asyncio

from .vars import*

# cog
class Remove(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #remove a category or expense
    @commands.command(name='remove', 
                      brief='- removes either an expense or an entire category')
    async def remove(self, ctx: commands.Context, 
                     category: str = commands.parameter(default=None, description='the category to remove'), 
                     index: int = commands.parameter(default=None, description='the expense number')):
        personal_expenses = expenses[ctx.author.id]

        #format help if no arguments are passed
        if not category and not index:
            await ctx.send("```remove [category]``` or ```remove [category] [expense number]```")
            return
        #check if category requested exists
        if not (category in personal_expenses):
            await ctx.send(f'"{category}" is not a category')
            return
        #if only category passed, remove category
        if not index:
            await ctx.send(f'remove {category}? [y]=yes/[any]=no')

            confirmation = ""
            #ask the user to confirm whether or not to remove category
            def confirm(msg):
                nonlocal confirmation
                confirmation = msg.content
                return msg.content != None
            
            resp = None

            try:
                resp: bool = await self.client.wait_for('message', timeout=10, check=confirm)
            except asyncio.TimeoutError:
                await ctx.send('timeout')

            # removes the category
            if resp:
                if confirmation == 'y':
                    del personal_expenses[category]
                    update_db()
                    await ctx.send(f'{category} has been removed.')
                else:
                    await ctx.send('remove cancelled')

        # removes an expense
        category_expenses: list = personal_expenses[category]
        if (index - 1 < len(category_expenses)):
            expense = category_expenses.pop(index - 1)
            update_db()
            await ctx.send(f'removed {expense[2]} from {category}')
        else:
            #expense does not exist
            await ctx.send(f'{index} is not an expense number in "{category}"')


async def setup(client):
    await client.add_cog(Remove(client))

import asyncio
from distutils.dist import command_re
import logging
import threading
import time
from tkinter import BOTTOM
from typing import Any, Optional, Type
from discord import Intents, Object
import MyCommand
from discord.ext import commands

class ControlPingPong(commands.Bot):
    def __init__(self, data, message):
        self.datas = data
        self.messages = message
        super().__init__(
            command_prefix='/',
            intents=Intents.all(),
            sync_command=True,
            application_id=1115760737147687035
        )
            
    async def on_ready(self):
        print("login")
        print(self.user)
        print("===============")
        channel = self.get_channel(1117659491102634055)
        while True:
            if len(self.datas) > 0:
                data = self.datas.pop(0)
                await channel.send(f'> ***{data[0]}***') # type: ignore
                await channel.send(data[1]) # type: ignore
    


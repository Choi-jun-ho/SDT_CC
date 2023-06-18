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
import datetime

class ControlDiscord(commands.Bot):
    def __init__(self, data, message):
        self.datas = data
        self.messages = message
        super().__init__(
            command_prefix='/',
            intents=Intents.all(),
            sync_command=True,
            application_id=1105744571742302249
        )

            
    async def on_ready(self):
        print("login")
        print(self.user)
        print("===============")
            
    async def on_message(self, message):
        
        if message.author == self.user:
            return
        
        print("message: ", message.content)
        if message.author.name == "MessagePingPong":
            if message.content.startswith("/"):
                mss = message.content[1:].split(" ")
                print(mss)
                await MyCommand.show_(message.channel, *mss[1:])
            return
        if message.content.startswith("/"):
            mss = message.content[1:].split(" ")
            print(mss)
            if mss[0] == "show":
                await MyCommand.show_(message.channel, *mss[1:]) # type: ignore
            elif mss[0] == "del":
                await MyCommand._del_(message.channel, mss[1], mss[2]) # type: ignore
            elif mss[0] == "add":
                await MyCommand.add_(message.channel, mss[1], mss[2], *mss[3:]) # type: ignore
            elif mss[0] == "set":
                await MyCommand.set_(message.channel, mss[1], mss[2], *mss[3:]) # type: ignore

        if message.author.name != "MessagePingPong":
            now = datetime.datetime.now()
            hour = now.hour;
            timeType = "오전"
            if hour >= 12:
                timeType = "오후"
                hour -= 12
            time = f"{timeType} {str(hour)}시 {str(now.minute)}분"
            self.messages.append(str(message.author.name) + "," + str(message.content) + "," + str(time))
            
        

        
        
        
        
        print(self.messages)
    


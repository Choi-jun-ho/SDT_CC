import MyCommand
from ControlDiscord import ControlDiscord
from ContorllPingPong import ControlPingPong
import threading

def run_flask(data, ctx):
    MyCommand.data = data
    MyCommand.ctxSave = ctx
    MyCommand.app.run(use_reloader=False)

def run_discord(data, ctx, message):
    MyCommand.data = data
    MyCommand.mesageSave = message
    MyCommand.bot = ControlDiscord(data, message)
    MyCommand.bot.run("MTEwNTc0NDU3MTc0MjMwMjI0OQ.GZ8uLw.ya0eRBbJ-WjvMjFB6TJ76C1tiQPB8Fm2qVpxh4")

def run_discord_pingpong(data, message):
    MyCommand.data = data
    MyCommand.mesageSave = message
    bot = ControlPingPong(data, message)
    bot.run("MTExNTc2MDczNzE0NzY4NzAzNQ.GTaI35.jQOVvbxi6sQd0z3lcmZQNELtwxmE8d34e4CBzI")
    
# from quart import Quart

# app = Quart(__name__)
# 여기에 라우트 및 기타 로직 추가


if __name__ == '__main__':
    data = []
    ctx = []
    message = []
    
    MyCommand.data = data
    MyCommand.ctxSave = ctx

    discord_thread = threading.Thread(target=run_discord, args=(data, ctx, message))
    pingPong_thread = threading.Thread(target=run_discord_pingpong, args=(data, message))
    discord_thread.start()
    pingPong_thread.start()
    MyCommand.app.run(host='192.168.0.21')
    # app.run(use_reloader=False)
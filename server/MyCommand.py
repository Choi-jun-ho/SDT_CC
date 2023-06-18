import asyncio
import datetime
from functools import wraps
import discord
from discord import Interaction, app_commands
from ControlNotion import ControlNotion as Notion
from MakeTable import MakeTable as visaultable
from quart import Quart, request, jsonify, send_file

from discord.ext import commands as cmd
from pprint import pprint
import os

app = Quart(__name__)
notion = Notion()
ctxSave = None
mesageSave = []
bot = None
data = None

# View 테이블 제목 선택 후 속성 제목 선택 : /view 테이블 제목 l 속성 제목 l 속성 제목
# /show [테이블 제목] [속성=제목]
@cmd.command("show")
async def show(ctx, *args):    
    await show_(ctx, *args)

def get_time():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

async def show_(ctx, *args):
    table_title = args[0]
    filters = args[1:]
    print('_____________run : command_show_____________')
    table = await notion.search(table_title)
    print("search Compleate")
    for filter in filters:
        if "=" not in filter:
            await ctx.send(f"filter({filter})에 '='를 입력해주세요".format(filter))
            return False
        key, value = filter.split("=")
        col = -1
        for i, k in enumerate(table['header'].keys()): # type: ignore
            if key == k:
                col = i
                break
        del_li = []
        for i, data in enumerate(table['data']): # type: ignore
            if value not in data[col]:
                del_li.append(i)
                continue
        del_li.reverse()
        for i in del_li:
            del table['data'][i] # type: ignore
    
    print("filter Compleate")
    await gui(ctx, get_time(),  table)

async def show__(time, *args):
    table_title = args[0]
    filters = args[1:]
    print('_____________run : command_show_____________')
    table = await notion.search(table_title)
    print("search Compleate")
    for filter in filters:
        if "=" not in filter:
            return False
        key, value = filter.split("=")
        col = -1
        for i, k in enumerate(table['header'].keys()): # type: ignore
            if key == k:
                col = i
                break
        del_li = []
        for i, data in enumerate(table['data']): # type: ignore
            if value not in data[col]:
                del_li.append(i)
                continue
        del_li.reverse()
        for i in del_li:
            del table['data'][i] # type: ignore

    print("filter Compleate")
    await gui_(time, table)


# Delete 데이터 삭제 : /delete 테이블 제목 l 
# /delete [테이블 제목] [투플=키본키 값]
async def _del_(ctx, table_title:str, page_title:str):
    print('command_delete_run')
    table = await notion.del_page(database_name=table_title, page_name=page_title)
    await gui(ctx, get_time(),  table)

async def _del__(time, table_title:str, page_title:str):
    print('command_delete_run')
    table = await notion.del_page(database_name=table_title, page_name=page_title)
    await gui_(time, table)

# Insert 테이블 선택 후 데이터 입력 : /add or /insert 테이블 제목 l 내용 l 내용
# /add [테이블 제목] [투플=기본키 값] [속성 제목 = 데이터 내용] [속성 제목 = 데이터 내용]
async def add_(ctx, database_name, page_name, *properties):    
    print('command_add')
    table = await notion.create_page(database_name, page_name, properties)
    await gui(ctx, get_time(), table)

async def add__(time, database_name, page_name, *properties):    
    print('command_add')
    table = await notion.create_page(database_name, page_name, properties)
    await gui_(time, table)

# Update 테이블 선택 후 데이터 입력 : /update 테이블 제목 l 내용
# /set [테이블 제목] [투플=기본키 값] [속성 제목 = 데이터 내용]
async def set_(ctx, database_name, page_name, *properties):    
    print('command_set')
    table = await notion.update_page(database_name, page_name, properties)
    await gui(ctx, get_time(), table)

async def set__(time, database_name, page_name, *properties):
    print('command_set')
    table = await notion.update_page(database_name, page_name, properties)
    await gui_(time, table)

# 명령 처리 함수를 따로 생성합니다.
async def handle_command(ctx, name, message):
    await ctx.send(f"{name} : {message}") # await을 사용하여 호출합니다.
    # 이후에 처리하고자 하는 기능들 추가

# ctxSave[0]를 인수로 전달하는 예제 함수입니다.
async def example_call_handler():
    if ctxSave != None:
        if len(ctxSave) > 0:
            ctx = ctxSave[0]
            name = "Some Name"
            message = "Some Message"
            await handle_command(ctx, name, message)  # 비동기적으로 명령을 처리합니다.

@app.route('/addMessage', methods=['GET', 'POST'])
async def addMessage():
    print("addMessage")

    name = request.args.get("name")
    message = request.args.get("message")

    if bot != None:
        channel = bot.get_channel(int(1117659491102634055))
        data.append([name, message])  # type: ignore
        print("data : ", data)
    
        now = datetime.datetime.now()
        hour = now.hour
        timeType = "오전"
        if hour >= 12:
            timeType = "오후"
            hour -= 12
        time = f"{timeType} {str(hour)}시 {str(now.minute)}분"
        mesageSave.append(str(name) + "," + str(message) + "," + str(time))
        print(mesageSave)
        # asyncio.create_task(handle_command(ctxSave[0], name, message)) # 비동기 작업을 생성하고 큐에 추가합니다.
    
    else:
        print("ctxSave is None")
    return {"result": "success"}

@app.route('/command', methods=['GET', 'POST'])
async def command():
    print("command")
    message = str(request.args.get("command")) # type: ignore
    
    print("message : ", message)
    time = get_time()
    if message.startswith("/"):
        mss = message[1:].split(" ") # type: ignore
        print(mss)
        if mss[0] == "show":
            await show__(time, *mss[1:]) # type: ignore
        elif mss[0] == "del":
            await _del__(time, mss[1], mss[2]) # type: ignore
        elif mss[0] == "add":
            await add__(time, mss[1], mss[2], *mss[3:]) # type: ignore
        elif mss[0] == "set":
            await set__(time, mss[1], mss[2], *mss[3:]) # type: ignore
    print(mesageSave)
    # asyncio.create_task(handle_command(ctxSave[0], name, message)) # 비동기 작업을 생성하고 큐에 추가합니다.
    
    # is time.png
    if os.path.isfile(f'{time}.png'):
        print("create ok time.png")
        image_path = f'{time}.png'
    else:
        print("create not result.png")    
    
    image_path = f'{time}.png'    

    # 이미지 파일 전송
    return await send_file(image_path, mimetype='image/png')

@app.route("/getMessages")
def getMessages():
    print("getMessages")
    return {'messageSave':mesageSave}

@app.route('/image')
async def send_image():
    # 이미지 파일 경로
    image_path = 'result.png'

    # 이미지 파일 전송
    return await send_file(image_path, mimetype='image/png')

# @show.error
# async def show_error(ctx, eror):
#     await ctx.send(eror)

async def gui(ctx, time, table):
    visaultable(2, time, table)
    print("gui compleate")
    file = discord.File(f"{time}.png", filename=f"{time}.png")
    print("result make")
    embed = discord.Embed()
    embed.set_image(url=f"attachment://{time}.png")
    print("set_image")
    await ctx.send(file=file, embed=embed)
    print("gui send compleate")

async def gui_(time, table):
    visaultable(2, time, table)
    print("gui compleate")
    print("result make")
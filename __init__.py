# -*- coding: utf-8 -*-
import json

from hoshino import Service
from hoshino.typing import CQEvent

from .solve import solve, path

sv = Service('fgo_weekly_mission', help_='''
[fgo周常规划 特性x个数] 特性x(字母x)个数之间用空格隔开
[fgo特性列表] 查看支持属性
'''.strip())


@sv.on_prefix("fgo周常规划")
async def get_result(bot, ev):
    target = ev.message.extract_plain_text().strip()
    if target == '':
        await bot.send(ev, "\n[fgo周常规划 特性/地形x个数] 特性/地形x个数之间用空格隔开", at_sender=True)
        return
    try:
        target = dict([i.split("x") for i in target.split(" ")])
    except Exception:
        await bot.send(ev, "输入特性格式有误", at_sender=True)
        return
    result = solve(list(target.keys()), [int(i) for i in target.values()])
    msg = ''
    if result:
        for i in list(result.keys())[:-1]:
            msg += f"\n{i} {result[i]}次"
        msg += f'\n总计ap: {result["total"]}'
    else:
        msg += '\n周常规划失败Orz'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch('fgo特性列表')
async def character_list(bot, ev):
    with open(path+"/keywords.json", "r") as f:
        word_list = json.load(f)
    msg = "支持特性列表如下:"
    msg += "\n小怪属性:" + " ".join(word_list["mobs"])
    msg += "\n从者属性:" + " ".join(word_list["servant"])
    msg += "\n地形属性:" + " ".join(word_list["place"])
    await bot.send(ev, msg)

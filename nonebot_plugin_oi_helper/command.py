from nonebot import on_command
from nonebot.rule import to_me

from .query_api import (
    get_today_contests,
    get_tomorrow_contests,
    get_leetcode_daily,
    json2text_for_leetcode_daily_info,
    json2text,
    json2text_for_contest,
)

format_contests = json2text(json2text_for_contest)
format_leetcode = json2text(json2text_for_leetcode_daily_info)

# Commands

today_contest = on_command(
    "今日比赛",
    aliases={"contests", "today_contests"},
    rule=to_me(),
    priority=5,
    block=True,
)


@today_contest.handle()
async def handle_today_contests():
    res = format_contests(await get_today_contests())
    if res == "":
        res = "今天没有比赛哦！"
    res = f"Today's Contest:\n{res}"
    await today_contest.finish(res)


tomorrow_contests = on_command(
    "明日比赛", aliases={"tomorrow_contests"}, rule=to_me(), priority=5, block=True
)


@tomorrow_contests.handle()
async def handle_tomorrow_contests():
    res = format_contests(await get_tomorrow_contests())
    if res == "":
        res = "明天没有比赛哦！"
    res = f"Tomorrow's Contest:\n{res}"
    await tomorrow_contests.finish(res)


leetcode_daily = on_command(
    "每日一题", aliases={"leetcode_daily"}, rule=to_me(), priority=5, block=True
)


@leetcode_daily.handle()
async def handle_leetcode_daily():
    res = format_leetcode(await get_leetcode_daily())
    await leetcode_daily.finish(res)

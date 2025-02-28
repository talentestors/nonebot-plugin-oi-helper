from nonebot import logger
import datetime
from nonebot_plugin_oi_helper import query_api, command


async def test_get_today_contests():
    data = await query_api.get_today_contests()
    logger.trace(data)
    assert data is not None, "Failed to get today contests"
    now = datetime.datetime.now()
    today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second
    )
    tomorrow = today + datetime.timedelta(days=1)
    for contest in data:
        logger.trace(contest)
        start_time = datetime.datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        assert start_time >= today and end_time > now and start_time < tomorrow, (
            f"Failed to get today contests: {start_time}, {end_time}, {today}, {tomorrow}"
        )
    logger.success("test_get_today_contests passed")
    return command.format_contests(data)


async def test_get_towmorrow_contests():
    data = await query_api.get_tomorrow_contests()
    assert data is not None, "Failed to get tomorrow contests"
    logger.trace(data)
    now = datetime.datetime.now()
    today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second
    )
    tomorrow = today + datetime.timedelta(days=1)
    for contest in data:
        logger.trace(contest)
        start_time = datetime.datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        assert start_time >= tomorrow and end_time > now, (
            f"Failed to get tomorrow contests: {start_time}, {end_time}, {today}, {tomorrow}"
        )
    logger.success("test_get_tomorrow_contests passed")

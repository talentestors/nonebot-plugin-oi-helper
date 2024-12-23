from none_plugin_oi_helper import query_api
from nonebot import logger
import datetime


async def test_query_contest():
    _data = await query_api._get_contest_data(
        "../tests/contests/contests.json", lambda start, end, host: True
    )
    assert _data is not None, "Failed to get contest data"
    data = [
        {
            "name": "Szkolne Mistrzostwa W Programowaniu",
            "host": "spoj.com",
            "start_time": "2016-03-19 08:00",
            "end_time": "2025-01-01 08:00",
            "duration": 277344000,
            "link": "https://www.spoj.com/SMWP/",
        }
    ]
    logger.trace(_data)
    assert _data == data, "Failed to get correct contest data"
    logger.success("test_query_contest passed")


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
        assert (
            start_time >= today and end_time > now and start_time < tomorrow
        ), f"Failed to get today contests: {start_time}, {end_time}, {today}, {tomorrow}"
    logger.success("test_get_today_contests passed")


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
        assert (
            start_time >= tomorrow and end_time > now
        ), f"Failed to get tomorrow contests: {start_time}, {end_time}, {today}, {tomorrow}"
    logger.success("test_get_tomorrow_contests passed")


# Old tests

async def test_query_contest_old():
    _data = await query_api._get_contest_data(
        "../tests/contests/contests.json", lambda start, end, host: True
    )
    assert _data is not None, "Failed to get contest data"
    data = [
        {
            "name": "Szkolne Mistrzostwa W Programowaniu",
            "host": "spoj.com",
            "start_time": "2016-03-19 08:00",
            "end_time": "2025-01-01 08:00",
            "duration": 277344000,
            "link": "https://www.spoj.com/SMWP/",
        }
    ]
    logger.trace(_data)
    assert _data == data, "Failed to get correct contest data"
    logger.success("test_query_contest passed")


async def test_get_today_contests_old():
    dir = query_api.get_dirs().contests.value
    data = await query_api._get_today_contests(
        dir, query_api.json2text(query_api.json2text_for_contest)
    )
    logger.trace(data)
    assert data is not None, "Failed to get today contests"
    data = await query_api._get_today_contests(dir)
    now = datetime.datetime.now()
    today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second
    )
    tomorrow = today + datetime.timedelta(days=1)
    for contest in data:
        logger.trace(contest)
        start_time = datetime.datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        assert (
            start_time >= today and end_time > now and start_time < tomorrow
        ), f"Failed to get today contests: {start_time}, {end_time}, {today}, {tomorrow}"
    logger.success("test_get_today_contests passed")


async def test_get_towmorrow_contests_old():
    dir = query_api.get_dirs().contests.value
    data = await query_api._get_tomorrow_contests(
        dir, query_api.json2text(query_api.json2text_for_contest)
    )
    assert data is not None, "Failed to get tomorrow contests"
    logger.trace(data)
    data = await query_api._get_tomorrow_contests(dir)
    now = datetime.datetime.now()
    today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second
    )
    tomorrow = today + datetime.timedelta(days=1)
    for contest in data:
        logger.trace(contest)
        start_time = datetime.datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        assert (
            start_time >= tomorrow and end_time > now
        ), f"Failed to get tomorrow contests: {start_time}, {end_time}, {today}, {tomorrow}"
    logger.success("test_get_tomorrow_contests passed")

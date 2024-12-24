import datetime
from nonebot_plugin_oi_helper import query_api
from nonebot import logger


async def test_get_leetcode_daily():
    data = await query_api.get_leetcode_daily()
    logger.info(data)
    assert data is not None, "data is None"
    assert len(data) > 0, "data is empty"
    assert len(data) == 1, "data length is not 1"
    assert "title" in data[0], "title not in data"
    assert "url" in data[0], "url not in data"
    assert "difficulty" in data[0], "difficulty not in data"
    assert "date" in data[0], "date not in data"
    _date = data[0]["date"]
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(_date, "%Y-%m-%d")
    logger.info(f"now: {now}, date: {date}")
    assert now.year == date.year, "year not match"
    logger.success("test_get_leetcode_daily passed")


# Old tests
async def test_get_leetcode_daily_old():
    data = await query_api._get_leetcode_daily()
    logger.info(data)
    assert data is not None, "data is None"
    assert len(data) > 0, "data is empty"
    assert len(data) == 1, "data length is not 1"
    assert "title" in data[0], "title not in data"
    assert "url" in data[0], "url not in data"
    assert "difficulty" in data[0], "difficulty not in data"
    assert "date" in data[0], "date not in data"
    _date = data[0]["date"]
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(_date, "%Y-%m-%d")
    logger.info(f"now: {now}, date: {date}")
    assert now.year == date.year, "year not match"
    logger.success("test_get_leetcode_daily passed")

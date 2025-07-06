import datetime
from nonebot import logger
from nonebot_plugin_oi_helper import query_api
from nonebot_plugin_oi_helper import api


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
    logger.debug(f"now: {now}, date: {date}")
    assert now.year == date.year, "year not match"
    logger.success("test_get_leetcode_daily passed")


async def test_get_leetcode_daily_api():
    """测试实际的API调用"""
    try:
        data = await api.getLeetcodeDaily()
        logger.info(f"API调用成功: {data}")
        assert data is not None, "API返回数据为None"
        assert "title" in data, "title not in data"
        assert "url" in data, "url not in data"
        assert "difficulty" in data, "difficulty not in data"
        assert "date" in data, "date not in data"
        assert "id" in data, "id not in data"
        assert "content" in data, "content not in data"

        _date = data["date"]
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(_date, "%Y-%m-%d")
        logger.debug(f"now: {now}, date: {date}")
        assert now.year == date.year, "year not match"
        logger.success("test_get_leetcode_daily_api passed")
    except Exception as e:
        logger.error(f"API调用失败: {e}")
        raise e

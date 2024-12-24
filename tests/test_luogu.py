from nonebot_plugin_oi_helper import query_api
from nonebot import logger


async def test_get_luogu_random_news():
    data = await query_api.get_luogu_random_news()
    logger.info(data)
    assert data is not None, "data is None"
    assert len(data) > 0, "data is empty"
    assert len(data) == 1, "data length is not 1"
    assert "title" in data[0], "title not in data"
    assert "url" in data[0], "url not in data"
    logger.success("test_get_luogu_random_news passed")


# Old tests
async def test_get_luogu_random_news_old():
    data = await query_api._get_luogu_random_news()
    logger.info(data)
    assert data is not None, "data is None"
    assert len(data) > 0, "data is empty"
    assert len(data) == 1, "data length is not 1"
    assert "title" in data[0], "title not in data"
    assert "url" in data[0], "url not in data"
    logger.success("test_get_luogu_random_news passed")

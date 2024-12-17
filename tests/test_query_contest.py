from none_plugin_oi_helper import query_api
from nonebot import logger


async def test_query_contest():
    _data = await query_api.get_contest_data(
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
    dir = query_api.get_dirs().contests.value
    data = await query_api.get_today_contests(
        dir, query_api.json2text(query_api.json2text_for_contest)
    )
    assert data is not None, "Failed to get today contests"
    logger.trace(data)
    logger.success("test_get_today_contests passed")

import random
from . import logger
from datetime import datetime, timedelta
from .utils import (
    dirs,
    json2text,
    load_json,
    json2json,
    json2xml,
    json2text_for_leetcode_daily_info,
    json2text_for_contest,
    json2text_for_contest_zh,
    json2text_get_luogu_news_text,
)

__all__ = [
    "dirs",
    "json2text",
    "load_json",
    "json2json",
    "json2xml",
    "json2text_for_contest",
    "json2text_for_contest_zh",
    "json2text_get_luogu_news_text",
    "json2text_for_leetcode_daily_info",
    "get_contests_data",
    "get_today_contests",
    "get_tomorrow_contests",
    "get_upcoming_contests",
    "get_now_contests",
    "get_leetcode_daily",
    "get_luogu_news_condition",
    "get_luogu_newest_news",
    "get_luogu_random_news",
]


#
# ================= OI Helper API =================
#

# Contest


async def get_contests_data(filter):
    """Get contests data.

    Args:
        filter (function): start_time, end_time, host -> bool

    Returns:
        _type_: json

    Example:
        >>> def is_ok(start, end, host):
        ...     return datetime.now() < start
        >>> data = await get_contests_data(is_ok)
        >>> print(data)
    """
    contests = load_json(dirs.contests)
    result = []
    for contest in contests:
        start_time = datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        host = contest["host"]
        if filter(start_time, end_time, host):
            result.append(contest)
            logger.debug(f"Get contest: {contest}")
    logger.trace(f"Get contest data: {result}")
    return result


async def get_today_contests():
    """Get today contest.

    Returns:
        _type_: json

    Example:
        >>> data = await get_today_contests()
        >>> print(data)
    """
    now = datetime.now()
    today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    tomorrow = today + timedelta(days=1)
    return await get_contests_data(
        lambda start, end, host: start >= today and end > now and start < tomorrow
    )


async def get_tomorrow_contests():
    """Get tomorrow contest.

    Returns:
        _type_: json

    Example:
        >>> data = await get_tomorrow_contests()
        >>> print(data)
    """
    now = datetime.now()
    tomorrow = (
        now
        + timedelta(days=1)
        - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    )
    tomorrow_offset = tomorrow + timedelta(days=1)
    return await get_contests_data(
        lambda start, end, host: start >= tomorrow and start < tomorrow_offset
    )


async def get_upcoming_contests():
    """Get upcoming contest.

    Returns:
        _type_: json

    Example:
        >>> data = await get_upcoming_contests()
        >>> print(data)
    """
    now = datetime.now()
    return await get_contests_data(lambda start, end, host: now < start)


async def get_now_contests():
    """Get ongoing contest.

    Returns:
        _type_: json

    Example:
        >>> data = await get_now_contests()
        >>> print(data)
    """
    now = datetime.now()
    return await get_contests_data(lambda start, end, host: now >= start and now < end)


# LeetCode Daily


async def get_leetcode_daily():
    """Get LeetCode daily.

    Returns:
        _type_: json

    Example:
        >>> data = await get_leetcode_daily()
        >>> print(data)
    """
    data = load_json(dirs.leetcode_daily)
    if isinstance(data, list):
        return data
    return [data]


# Luogu News


async def get_luogu_news_condition(year: int = 0, month: int = 0):
    """Get Luogu news with date condition.

    Args:
        year (int): Year. Defaults to 0.
        month (int): Month. Defaults to 0.

    Returns:
        _type_: json
    """
    news = load_json(dirs.luogu_news)
    return [
        new
        for new in news
        if (not year or new["year"] == year) and (not month or new["month"] == month)
    ]


async def get_luogu_newest_news():
    """Get the newest Luogu news.

    Returns:
        _type_: json

    Example:
        >>> news = await get_luogu_newest_news()
        >>> print(news)
    """
    now = datetime.now()
    year = now.year
    month = now.month
    return await get_luogu_news_condition(year=year, month=month)


async def get_luogu_random_news():
    """Get a random Luogu news.

    Returns:
        _type_: json

    Example:
        >>> news = await get_luogu_random_news()
        >>> print(news)
    """
    news: dict = load_json(dirs.luogu_news)
    res = random.choice(list(news.keys()))
    res = [news[res]]
    return res

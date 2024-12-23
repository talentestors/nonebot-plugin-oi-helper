from nonebot import logger
from .api import Dirs, get_available_directories as get_dirs  # noqa: F401
from .utils import (
    json2text,
    load_json,
    json2json,
    json2xml,
    json2text_for_leetcode_daily_info,
    json2text_for_contest,
    json2text_for_contest_zh,
    json2text_get_luogu_news_text,
)
from datetime import datetime, timedelta
import random

__all__ = [
    "json2text",
    "load_json",
    "json2json",
    "json2xml",
    "json2text_for_contest",
    "json2text_for_contest_zh",
    "json2text_get_luogu_news_text",
    "get_dirs",
    "json2text_for_leetcode_daily_info",
    "json2text",
    "get_contests_data",
    "get_today_contests",
    "get_tomorrow_contests",
    "get_upcoming_contests",
    "get_now_contests",
    "get_leetcode_daily",
    "get_luogu_news_condition",
    "get_luogu_newest_news",
    "get_luogu_random_news",
    "_get_contest_data",
    "_get_today_contests",
    "_get_tomorrow_contests",
    "_get_upcoming_contests",
    "_get_now_contests",
    "_get_leetcode_daily",
    "_get_luogu_news_condition",
    "_get_luogu_newest_news",
    "_get_luogu_random_news"
]


dirs = get_dirs()

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
    contests = load_json(dirs.contests.value)
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
    return load_json(dirs.leetcode_daily.value)


# Luogu News


async def get_luogu_news_condition(year: int = 0, month: int = 0):
    """Get Luogu news with date condition.

    Args:
        year (int): Year. Defaults to 0.
        month (int): Month. Defaults to 0.

    Returns:
        _type_: json
    """
    news = load_json(dirs.luogu_daily.value)
    return [
        new
        for new in news.values()
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
    news = load_json(dirs.luogu_daily.value)
    res = random.choice(list(news.keys()))
    res = [news[res]]
    return res


#
# ================= OLD API =================
#


# Contest
async def _get_contest_data(file_name: str, is_ok, format=json2json):
    """Get contest data.

    Args:
        file_name (str|list[str]): File name.
        is_ok (function): A filter function to determine if the data is valid.
        format (function): A format function to format the data. Defaults to json2json.
            Possible values:
                - json2json
                - json2xml
                - json2text

    Returns:
        Any: The formatted data. May be a string or a dict.

    Example:
        >>> from datetime import datetime
        >>> from .api import dirs
        >>> def is_ok(start, end, host):
        ...     return datetime.now() < start
        >>> data = await get_contest_data(dirs["contests"], is_ok, json2json)
        >>> print(data)
    """
    contests = load_json(file_name)
    result = []
    for contest in contests:
        start_time = datetime.strptime(contest["start_time"], "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(contest["end_time"], "%Y-%m-%d %H:%M")
        host = contest["host"]
        if is_ok(start_time, end_time, host):
            result.append(contest)
            logger.debug(f"Get contest: {contest}")
    logger.trace(f"Get contest data: {result}")
    return format(result)


async def _get_today_contests(file_name: str | list[str], format=json2json):
    """Get today contest.

    Args:
        file_name (str|list[str]): File name.
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.

    Example:
        >>> from .api import dirs
        >>> data = await get_today_contest(dirs["contests"], json2text)
        >>> print(data)
    """
    now = datetime.now()
    today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    tomorrow = today + timedelta(days=1)
    if isinstance(file_name, str):
        result = await _get_contest_data(
            file_name,
            lambda start, end, host: start >= today and end > now and start < tomorrow,
        )
        return format(result)
    else:
        result = []
        for file in file_name:
            result.extend(
                await _get_contest_data(
                    file,
                    lambda start, end, host: start >= today
                    and end > now
                    and start < tomorrow,
                )
            )
        return format(result)


async def _get_tomorrow_contests(file_name: str | list[str], format=json2json):
    """Get tomorrow contest.

    Args:
        file_name (str|list[str]): File name.
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.

    Example:
        >>> from .api import dirs
        >>> data = await get_tomorrow_contest(dirs["contests"], json2text)
        >>> print(data)
    """
    now = datetime.now()
    tomorrow = (
        now
        + timedelta(days=1)
        - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    )
    tomorrow_offset = tomorrow + timedelta(days=1)
    if isinstance(file_name, str):
        result = await _get_contest_data(
            file_name,
            lambda start, end, host: start >= tomorrow and start < tomorrow_offset,
        )
        return format(result)
    else:
        result = []
        for file in file_name:
            result.extend(
                await _get_contest_data(
                    file,
                    lambda start, end, host: start >= tomorrow
                    and start < tomorrow_offset,
                )
            )
        return format(result)


async def _get_upcoming_contests(file_name: str | list[str], format=json2json):
    """Get upcoming contest.

    Args:
        file_name (str|list[str]): File name.
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.

    Example:
        >>> from .api import dirs
        >>> data = await get_upcoming_contest(dirs["contests"], json2text)
        >>> print(data)
    """
    now = datetime.now()
    if isinstance(file_name, str):
        result = await _get_contest_data(
            file_name, lambda start, end, host: now < start
        )
        return format(result)
    else:
        result = []
        for file in file_name:
            result.extend(
                await _get_contest_data(file, lambda start, end, host: now < start)
            )
        return format(result)


async def _get_now_contests(file_name: str | list[str], format=json2json):
    """Get ongoing contest.

    Args:
        file_name (str|list[str]): File name.
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.

    Example:
        >>> from .api import dirs
        >>> data = await get_now_contest(dirs["contests"], json2text)
        >>> print(data)
    """
    now = datetime.now()
    if isinstance(file_name, str):
        result = await _get_contest_data(
            file_name, lambda start, end, host: now >= start and now < end
        )
        return format(result)
    else:
        result = []
        for file in file_name:
            result.extend(
                await _get_contest_data(
                    file, lambda start, end, host: now >= start and now < end
                )
            )
        return format(result)


# LeetCode Daily
async def _get_leetcode_daily(format=json2json):
    """Get LeetCode daily.

    Args:
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.

    Example:
        >>> data = await get_leetcode_daily()
        >>> print(data)
    """
    data = [load_json(get_dirs().leetcode_daily.value)]
    return format(data)


# Luogu News
async def _get_luogu_news_condition(year: int = 0, month: int = 0, format=json2json):
    """Get Luogu news with date condition.

    Args:
        year (int): Year. Defaults to 0.
        month (int): Month. Defaults to 0.
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        Any: formatted data. may be a string or a dict.
    """
    news = load_json(get_dirs().luogu_daily.value)
    ret = [
        new
        for new in news.values()
        if (not year or new["year"] == year) and (not month or new["month"] == month)
    ]
    return format(ret)


async def _get_luogu_newest_news(format=json2json):
    """Get the newest Luogu news.

    Args:
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        _types: The newest Luogu news.

    Example:
        >>> news = await get_luogu_newest_news()
        >>> print(news)
    """
    now = datetime.now()
    year = now.year
    month = now.month
    ret = await _get_luogu_news_condition(year=year, month=month, format=json2json)
    return format(ret)


async def _get_luogu_random_news(format=json2json):
    """Get a random Luogu news.

    Args:
        format (function): Format function. Defaults to json2json.
            Possible values:
                    - json2json
                    - json2xml
                    - json2text

    Returns:
        _types: A random Luogu news.

    Example:
        >>> news = await get_luogu_random_news()
        >>> print(news)
    """
    news = load_json(get_dirs().luogu_daily.value)
    res = random.choice(list(news.keys()))
    res = [news[res]]
    return format(res)

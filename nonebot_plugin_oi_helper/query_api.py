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
)

__all__ = [
    "dirs",
    "json2text",
    "load_json",
    "json2json",
    "json2xml",
    "json2text_for_contest",
    "json2text_for_contest_zh",
    "json2text_for_leetcode_daily_info",
    "get_contests_data",
    "get_today_contests",
    "get_tomorrow_contests",
    "get_upcoming_contests",
    "get_now_contests",
    "get_leetcode_daily",
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

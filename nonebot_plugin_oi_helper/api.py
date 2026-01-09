import httpx
from nonebot.log import logger
from datetime import datetime, timedelta
from .utils import leetcode_locale_to_zh, save_json, dirs
from . import api_config


async def getContest():
    apikey = f"&username={api_config.username}&api_key={api_config.user_key}"
    url = f"{str(api_config.req_url)}" + apikey
    logger.info("GET " + str(api_config.req_url))

    try:
        # Use httpx.AsyncClient for async request
        async with httpx.AsyncClient(http2=True, timeout=12.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            logger.info("getContest SUCCESS " + str(response.status_code))
            data = response.json()

        contests = []
        for contest in data["objects"]:
            name = contest["event"]
            host = contest["host"]
            start_time = (
                datetime.strptime(contest["start"], "%Y-%m-%dT%H:%M:%S")
                + timedelta(hours=8)
            ).strftime("%Y-%m-%d %H:%M")
            end_time = (
                datetime.strptime(contest["end"], "%Y-%m-%dT%H:%M:%S")
                + timedelta(hours=8)
            ).strftime("%Y-%m-%d %H:%M")
            new_contest = {
                "name": name,
                "host": host,
                "start_time": start_time,
                "end_time": end_time,
                "duration": contest["duration"],
                "link": contest["href"],
            }
            match host:
                case "leetcode.com":
                    new_contest = leetcode_locale_to_zh(new_contest)
            contests.append(new_contest)
        save_json(dirs.contests, contests)

    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise

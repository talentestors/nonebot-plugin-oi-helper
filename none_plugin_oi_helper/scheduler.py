import asyncio
from nonebot import require
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from . import api


async def init():
    """first load data"""
    await loadContestMsg()
    await loadLuoGuDailyMsg()
    await loadLeetCodeDailyMsg()


def scheduler_constroller():
    """
    scheduler controller
    """
    logger.info("Message data loading...")
    # asyncio.run(init())
    logger.info("Message data loaded.\n")
    require("nonebot_plugin_apscheduler")
    return scheduler


async def loadContestMsg():
    try:
        await api.getContest()
    except Exception:
        logger.error("比赛信息定时更新时遇到错误：")
        logger.info("再次尝试获取比赛信息")
        try:
            await api.getContest()
        except Exception as e:
            logger.exception(e)
            logger.error("再次尝试获取比赛信息时遇到错误：\n")


@scheduler.scheduled_job("cron", hour="2, 14", id="loadContestMsg")
async def loadContestMsgSchedule():
    await loadContestMsg()


async def loadLuoGuDailyMsg():
    try:
        await api.getLuoguDaily()
    except Exception:
        logger.error("洛谷日报定时更新时遇到错误：")
        logger.info("再次尝试获取洛谷日报信息")
        try:
            await api.getLuoguDaily()
        except Exception as e:
            logger.exception(e)
            logger.error("再次尝试获取洛谷日报信息时遇到错误：\n")


@scheduler.scheduled_job("interval", days=1, id="loadLuoGuDailyMsg")
async def loadLuoGuDailyMsgSchedule():
    await loadLuoGuDailyMsg()


async def loadLeetCodeDailyMsg():
    try:
        await api.getLeetcodeDaily()
    except Exception:
        logger.error("力扣每日一题定时更新时遇到错误：")
        logger.info("再次尝试获取力扣每日一题信息")
        try:
            await api.getLeetcodeDaily()
        except Exception as e:
            logger.exception(e)
            logger.error("再次尝试获取力扣每日一题信息时遇到错误：\n")


@scheduler.scheduled_job("interval", days=1, id="loadLeetCodeDailyMsg")
async def loadLeetCodeDailyMsgSchedule():
    await loadLeetCodeDailyMsg()


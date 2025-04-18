from datetime import datetime, timedelta
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
from . import api


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


@scheduler.scheduled_job(
    "interval",
    days=1,
    id="loadLeetCodeDailyMsg",
    next_run_time=(datetime.now() + timedelta(seconds=1)),
)
async def loadLeetCodeDailyMsgSchedule():
    await loadLeetCodeDailyMsg()
    logger.success("力扣每日一题已更新")


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


@scheduler.scheduled_job(
    "cron",
    hour="2, 14",
    id="loadContestMsg",
    next_run_time=(datetime.now() + timedelta(seconds=2)),
)
async def loadContestMsgSchedule():
    await loadContestMsg()
    logger.success("比赛信息已更新")


async def init():
    """first load data"""
    await loadContestMsg()
    await loadLeetCodeDailyMsg()

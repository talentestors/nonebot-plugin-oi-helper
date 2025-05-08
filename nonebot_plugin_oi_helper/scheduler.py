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
            raise Exception("获取力扣每日一题信息失败")


@scheduler.scheduled_job(
    "cron",
    minute=1,
    hour="0,1,12",
    id="loadLeetCodeDailyMsg",
    next_run_time=(datetime.now() + timedelta(seconds=1)),
)
async def loadLeetCodeDailyMsgSchedule():
    try:
        await loadLeetCodeDailyMsg()
        logger.success("力扣每日一题已更新")
    except Exception as e:
        logger.error(f"力扣每日一题更新失败：{e}")


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
            raise Exception("获取比赛信息失败")


@scheduler.scheduled_job(
    "interval",
    hours=6,
    id="loadContestMsg",
    next_run_time=(datetime.now() + timedelta(seconds=2)),
)
async def loadContestMsgSchedule():
    try:
        await loadContestMsg()
        logger.success("比赛信息已更新")
    except Exception as e:
        logger.error(f"比赛信息更新失败：{e}")


async def init():
    """first load data"""
    await loadContestMsg()
    await loadLeetCodeDailyMsg()

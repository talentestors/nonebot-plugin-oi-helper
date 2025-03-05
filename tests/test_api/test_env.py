import os
from nonebot.log import logger
from dotenv import load_dotenv


from nonebot_plugin_oi_helper import config

# Load the environment variables
load_dotenv()


def test_env():
    environment = os.getenv("ENVIRONMENT")
    driver = os.getenv("DRIVER")
    log_level = os.getenv("LOG_LEVEL")
    clist_username = os.getenv("CLIST__USERNAME")
    clist_user_key = os.getenv("CLIST__USER_KEY")

    logger.trace("Print API Config")
    logger.trace(f"ENVIRONMENT: {environment}")
    logger.trace(f"DRIVER: {driver}")
    logger.trace(f"LOG_LEVEL: {log_level}")
    logger.trace(f"CLIST__USERNAME: {clist_username}")
    logger.trace(f"CLIST__USER_KEY: {clist_user_key}")
    logger.trace(f"Require Url: {config.clist.req_url}")

    assert clist_username == config.clist.username, (
        "Username is not equal to the config username"
    )
    assert clist_user_key == config.clist.user_key, (
        "User Key is not equal to the config user key"
    )
    logger.success("test_env passed")

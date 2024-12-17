from nonebot.log import logger
import pytest
import nonebot

# 导入适配器

nonebot.init()
driver = nonebot.get_driver()
env_config = driver.config
env_run_evironment = str(env_config.environment).strip()

# 加载插件
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("none_plugin_oi_helper")
logger.info("Plugin loaded")

if __name__ == "__main__":
    pytest.main(["-v", "-s", "tests"])

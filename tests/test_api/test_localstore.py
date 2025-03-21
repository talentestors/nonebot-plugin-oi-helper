from nonebot import logger
from nonebot_plugin_oi_helper.utils import plugin_cache_dir, dirs, store, Dirs


def test_localstore():
    """
    Test localstore module
    """
    assert plugin_cache_dir.exists()
    logger.info("plugin_cache_dir: " + str(plugin_cache_dir))
    logger.info("dirs: " + str(dirs))


def test_cache_file():
    """
    Test cache file
    """
    for target_file in Dirs.__annotations__.values():
        cache_file = store.get_cache_file("nonebot_plugin_oi_helper", str(target_file))
        assert cache_file.exists(), f"{cache_file} not exists"
        logger.info(f"cache_file: {cache_file}")

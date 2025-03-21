# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "nonebot-plugin-localstore",
#     "nonebot2[aiohttp]",
# ]
# ///
import nonebot
from pathlib import Path
import shutil


def clean_cache() -> Path:
    import nonebot_plugin_localstore as localstore

    cache_path: Path = localstore.get_cache_dir("nonebot_plugin_oi_helper")
    if not cache_path.exists():
        print(f"缓存目录 {cache_path} 不存在。")
        return cache_path
    print(f"开始清理缓存目录 {cache_path}。")

    for entry in cache_path.iterdir():
        try:
            if entry.is_file():
                entry.unlink()
                print(f"已删除文件: {entry}")
            elif entry.is_dir():
                shutil.rmtree(entry)
                print(f"已删除目录: {entry}")
        except Exception as e:
            print(f"删除 {entry} 时发生错误: {e}")
    return cache_path


if __name__ == "__main__":
    nonebot.init()
    nonebot.load_plugin("nonebot_plugin_localstore")
    cache_path = clean_cache()
    shutil.rmtree(cache_path)
    print(f"已删除缓存目录: {cache_path}")

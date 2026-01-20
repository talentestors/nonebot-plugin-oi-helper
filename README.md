<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  </br>
  <p><img src="https://raw.githubusercontent.com/talentestors/nonebot-plugin-oi-helper/main/docs/img/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>
<div align="center">

# nonebot-plugin-OI-helper

_✨ 一个提供 OI/ACM 相关信息的 nonebot2 插件 ✨_

[![license](https://img.shields.io/github/license/talentestors/nonebot-plugin-oi-helper.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-oi-helper.svg)](https://pypi.python.org/pypi/nonebot-plugin-oi-helper)
![python](https://img.shields.io/badge/python-3.12+-blue.svg)
![downloads](https://img.shields.io/pypi/dm/nonebot-plugin-oi-helper)
[![Publish Release](https://github.com/talentestors/nonebot-plugin-oi-helper/actions/workflows/release-publish.yml/badge.svg)](https://github.com/talentestors/nonebot-plugin-oi-helper/actions/workflows/release-publish.yml)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftalentestors%2Fnonebot-plugin-oi-helper.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Ftalentestors%2Fnonebot-plugin-oi-helper?ref=badge_shield)

</div>

> [!WARNING]
>
> v1 版本已重构，基于 HTTP/2
>
> aiohttp 替换为 httpx

## 📖 介绍

一个基于 <https://clist.by> v4 接口，提供 OI/ACM 相关信息查询的 nonebot2 插件。

扩展内容：

- [x] 获取 **LeetCode 每日一题**
- [ ] ...

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>

在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-oi-helper
```

</details>

<details>
<summary>使用包管理器安装</summary>

在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-oi-helper
```

</details>

<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-oi-helper
```

</details>

<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-oi-helper
```

</details>

<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-oi-helper
```

</details>

<details>
<summary>uv</summary>

</br>

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

> Documents: <https://docs.astral.sh/uv/>

```bash
uv add nonebot-plugin-oi-helper
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

```bash
plugins = ["nonebot_plugin_oi_helper"]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的 `.env` 文件中添加下表中的必填配置

> [!TIP]
> 需要使用 aiohttp 的驱动器

|       配置项       | 必填  |                                            默认值                                             |      说明       |
| :----------------: | :---: | :-------------------------------------------------------------------------------------------: | :-------------: |
|  CLIST__USERNAME   |  是   |                                              无                                               | 你的clist用户名 |
|  CLIST__USER_KEY   |  是   |                                              无                                               |    你的 key     |
| CLIST_API__REQ_URL |  否   | <https://clist.by:443/api/v4/contest/?upcoming=true&filtered=true&order_by=start&format=json> |  自定义查询url  |

例如在你的 `.env` 文件里：

```ini
# nonebot-plugin-oi-helper 配置
CLIST__USERNAME=talentestors
CLIST__USER_KEY=b4c1d76de149ef89cf0542b59a567f7c6b4af952
# clist API 地址
# CLIST_API__REQ_URL=
```

### 如何获取 clist 的 key？

<details>
<summary>点击展开</summary>

1. 进入 CLIST 官网：<https://clist.by/>
2. 如果你是新用户，你需要新建一个账户。
3. 前往 <https://clist.by/api/v4/doc/> 页面也可以从这里进去：
    ![api](./docs/img/image.png)
4. 点 _here_ 获取你的 API KEY
    > Accessing the API requires an API key, which is available to authenticated users _here_.

    ![here](./docs/img/guide.png)

</details>

### 关于 Filter

<details>
<summary>点击展开</summary>

默认的 clist 的 url 加入了，`filtered=true` 参数。

这意味着你可以在你的账户里面直接配置规则，而不用设置复杂的 url 请求参数。

<https://clist.by/settings/filters/>

点击 _create_ 去创建一个规则

`Resources` 项，能筛选对应的平台。

![filter](./docs/img/filter.png)

</details>

## 🎉 使用

[See docs](./docs/README.md)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftalentestors%2Fnonebot-plugin-oi-helper.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Ftalentestors%2Fnonebot-plugin-oi-helper?ref=badge_large)

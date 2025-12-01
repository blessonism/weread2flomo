"""
微信读书数据提取工具
"""
import os
import time
import requests
import json
from http.cookies import SimpleCookie
from requests.utils import cookiejar_from_dict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .config_manager import config

# 加载环境变量
load_dotenv()

# 微信读书 API 端点（参考 mcp-server-weread 项目）
WEREAD_URL = "https://weread.qq.com/"
WEREAD_NOTEBOOKS_URL = "https://weread.qq.com/api/user/notebook"
WEREAD_BOOKMARKLIST_URL = "https://weread.qq.com/web/book/bookmarklist"
WEREAD_CHAPTER_INFO = "https://weread.qq.com/web/book/chapterInfos"
WEREAD_READ_INFO_URL = "https://weread.qq.com/web/book/getProgress"
WEREAD_REVIEW_LIST_URL = "https://weread.qq.com/web/review/list"
WEREAD_BOOK_INFO = "https://weread.qq.com/api/book/info"

# 全局 session 对象
_session = None


def parse_cookie_string(cookie_string: str):
    """解析 Cookie 字符串，返回 cookiejar"""
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dict = {}
    cookiejar = None
    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value
        cookiejar = cookiejar_from_dict(
            cookies_dict, cookiejar=None, overwrite=True
        )
    return cookiejar


def get_session():
    """获取已初始化的 session"""
    global _session
    if _session is None:
        raise RuntimeError("Session 未初始化，请先调用 init_session()")
    return _session


def init_session(cookie_string: str):
    """初始化 session 并设置 cookies

    参考 mcp-server-weread 实现：
    - 直接在 headers 中设置 Cookie（而不是 session.cookies）
    - 设置完整的浏览器 headers，模拟真实浏览器行为
    """
    global _session
    _session = requests.Session()

    # 安装带重试的适配器（429/5xx自动重试，指数退避）
    retries = Retry(
        total=config.get_max_retries(),
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    _session.mount("https://", adapter)
    _session.mount("http://", adapter)

    # ⚠️ 关键修改：直接在 headers 中设置 Cookie（mcp-server-weread 的做法）
    _session.headers.update({
        'Cookie': cookie_string,  # 直接设置 Cookie 字符串
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    })

    # 先访问主页建立会话 - 使用完整的浏览器headers（参考MCP的visitHomepage）
    try:
        homepage_headers = {
            'Cookie': cookie_string,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1'
        }
        _session.get(WEREAD_URL, headers=homepage_headers, timeout=30)
    except Exception as e:
        print(f"⚠️ 访问主页失败: {e}")

    return _session


def _refresh_session_cookie() -> str:
    """刷新会话并获取最新的 cookie
    
    这个函数会：
    1. 访问主页建立会话
    2. 获取笔记本列表预热
    3. 提取最新的 wr_skey
    4. 返回更新后的 cookie 字符串
    
    Returns:
        更新后的 cookie 字符串（包含最新的 wr_skey）
    """
    session = get_session()
    cookie_string = session.headers.get('Cookie', '')
    
    try:
        # 1. 访问主页
        homepage_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        session.get(WEREAD_URL, headers=homepage_headers, timeout=30)
        
        # 2. 获取笔记本列表
        params = {'_': int(time.time() * 1000)}
        session.get(WEREAD_NOTEBOOKS_URL, params=params, timeout=30)
        
        # 3. 提取最新的 wr_skey
        new_wr_skey = None
        for cookie in session.cookies:
            if cookie.name == 'wr_skey':
                new_wr_skey = cookie.value
                break
        
        # 4. 更新 cookie 字符串中的 wr_skey
        if new_wr_skey:
            import re
            cookie_string = re.sub(
                r'wr_skey=[^;]+',
                f'wr_skey={new_wr_skey}',
                cookie_string
            )
    except Exception as e:
        print(f"⚠️ 刷新会话失败: {e}")
    
    return cookie_string


def get_bookmark_list(bookId: str) -> List[Dict]:
    """获取书籍的划线列表
    
    注意：此 API 需要会话预热和最新的 wr_skey
    """
    try:
        session = get_session()
        
        # 刷新会话并获取最新 cookie
        print(f"→ 刷新会话并获取最新 cookie...")
        fresh_cookie = _refresh_session_cookie()
        
        # 使用最新的 cookie 请求
        headers = {
            'Cookie': fresh_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        params = {
            "bookId": bookId,
            "_": int(time.time() * 1000)
        }
        
        print(f"→ 请求划线列表: {WEREAD_BOOKMARKLIST_URL}")
        response = session.get(
            WEREAD_BOOKMARKLIST_URL,
            params=params,
            headers=headers,
            timeout=30
        )
        
        print(f"✓ 响应状态: {response.status_code}")
        
        if response.ok:
            data = response.json()
            
            # 检查错误码
            if 'errCode' in data and data['errCode'] != 0:
                print(f"❌ API 返回错误: {data.get('errMsg')} (code: {data.get('errCode')})")
                return []
            
            bookmarks = data.get("updated", [])
            print(f"✓ API 返回 {len(bookmarks)} 条原始划线")
            
            # 过滤掉无效的划线
            valid_bookmarks = [bm for bm in bookmarks if bm.get("markText") and bm.get("chapterUid")]
            if len(valid_bookmarks) != len(bookmarks):
                print(f"✓ 过滤后剩余 {len(valid_bookmarks)} 条有效划线")
            
            return valid_bookmarks
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 获取划线列表失败: {e}")
        import traceback
        traceback.print_exc()
    return []


def get_chapter_info(bookId: str) -> List[Dict]:
    """获取书籍章节信息

    **关键发现**：MCP 项目在 getChapterInfo 中绕过了 axiosInstance，
    直接使用原始 axios，并完全重新设置 headers！

    参考 mcp-server-weread 的实现（WeReadApi.ts:428-548）：
    1. 先访问主页建立会话
    2. 获取笔记本列表预热会话
    3. 添加随机延迟模拟真实用户
    4. **使用 session 而不是独立请求，保持会话连贯性**
    5. 使用正确的请求头和请求体格式
    """
    try:
        session = get_session()
        
        # 刷新会话并获取最新 cookie（与 get_bookmark_list 保持一致）
        fresh_cookie = _refresh_session_cookie()
        
        # 使用正确的请求体格式
        params = {'_': int(time.time() * 1000)}  # 时间戳避免缓存
        body = {'bookIds': [bookId]}
        
        # 使用最新的 cookie 请求
        api_headers = {
            'Cookie': fresh_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://weread.qq.com',
            'Referer': f'https://weread.qq.com/web/reader/{bookId}',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        print(f"→ 请求章节信息: {WEREAD_CHAPTER_INFO}")
        response = session.post(
            WEREAD_CHAPTER_INFO,
            params=params,
            headers=api_headers,
            json=body,
            timeout=60
        )

        print(f"✓ 响应状态: {response.status_code}")

        if response.ok:
            data = response.json()

            # 7. 处理多种可能的响应格式（参考 MCP 项目的处理逻辑）
            chapters = None

            # 格式1: {data: [{bookId: "xxx", updated: []}]}
            if isinstance(data.get('data'), list) and len(data['data']) > 0:
                chapters = data['data'][0].get('updated', [])
            # 格式2: {updated: []}
            elif 'updated' in data and isinstance(data['updated'], list):
                chapters = data['updated']
            # 格式3: 直接是数组
            elif isinstance(data, list) and len(data) > 0:
                if 'updated' in data[0]:
                    chapters = data[0]['updated']
                elif 'chapterUid' in data[0]:
                    chapters = data

            if chapters is not None:
                print(f"✓ 获取到 {len(chapters)} 个章节")
                # 添加"点评"特殊章节
                chapters.append({
                    'chapterUid': 1000000,
                    'chapterIdx': 1000000,
                    'updateTime': 1683825006,
                    'readAhead': 0,
                    'title': '点评',
                    'level': 1
                })
                return chapters

            # 检查错误码
            if 'errcode' in data or 'errCode' in data:
                errcode = data.get('errcode') or data.get('errCode')
                errmsg = data.get('errmsg') or data.get('errMsg', 'Unknown error')
                print(f"❌ API 返回错误: {errmsg} (code: {errcode})")
                return []

            print(f"⚠️ 获取章节信息失败: 返回格式不符合预期")
            print(f"响应数据: {data}")
            return []
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            return []

    except Exception as e:
        print(f"❌ 获取章节信息失败: {e}")
        import traceback
        traceback.print_exc()
    return []


def get_bookinfo(bookId: str) -> Optional[Dict]:
    """获取书籍详细信息"""
    params = {
        "bookId": bookId,
        "_": int(time.time() * 1000)  # 添加时间戳避免缓存
    }
    try:
        session = get_session()
        response = session.get(
            WEREAD_BOOK_INFO,
            params=params,
            timeout=30
        )
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"获取书籍信息失败: {e}")
    return None


def get_notebooklist() -> List[Dict]:
    """获取笔记本列表

    注意：
    - MCP 项目在所有 GET 请求中添加时间戳参数避免缓存
    - 返回的是完整的 data 对象，包含 books 数组
    """
    try:
        session = get_session()
        # 添加时间戳参数避免缓存（MCP 项目的做法）
        params = {'_': int(time.time() * 1000)}
        response = session.get(WEREAD_NOTEBOOKS_URL, params=params, timeout=30)
        if response.ok:
            data = response.json()
            # MCP 项目的 API 返回格式可能不同，需要兼容处理
            # 可能是 {books: [...]} 或者直接是数组
            if isinstance(data, dict):
                return data.get("books", [])
            elif isinstance(data, list):
                return data
    except Exception as e:
        print(f"获取笔记本列表失败: {e}")
    return []


def get_review_list(bookId: str) -> List[Dict]:
    """获取书籍的笔记列表

    参考 weread-mcp 项目的参数设置
    关键参数: listType=11, mine=1
    注意：此 API 需要会话预热和最新的 wr_skey
    """
    try:
        session = get_session()
        
        # 刷新会话并获取最新 cookie
        fresh_cookie = _refresh_session_cookie()
        
        # 使用最新的 cookie 请求
        headers = {
            'Cookie': fresh_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        params = {
            "bookId": bookId,
            "listType": 11,  # weread-mcp 使用 11
            "mine": 1,        # weread-mcp 添加了 mine=1
            "syncKey": 0,
            "_": int(time.time() * 1000)
        }
        
        response = session.get(
            WEREAD_REVIEW_LIST_URL,
            params=params,
            headers=headers,
            timeout=30
        )
        
        if response.ok:
            data = response.json()
            
            # 检查错误码
            if 'errCode' in data and data['errCode'] != 0:
                print(f"❌ API 返回错误: {data.get('errMsg')} (code: {data.get('errCode')})")
                return []
            
            reviews = data.get("reviews", [])

            # MCP 项目的处理方式：提取 review 对象
            reviews = [r.get("review") for r in reviews if r.get("review")]

            # 为书评添加 chapterUid（MCP 项目的逻辑）
            for review in reviews:
                if review.get("type") == 4:
                    review["chapterUid"] = 1000000

            return reviews
    except Exception as e:
        print(f"获取笔记列表失败: {e}")
    return []


def try_get_cloud_cookie(cc_url: str, cc_id: str, cc_password: str) -> Optional[str]:
    """从 Cookie Cloud 获取 Cookie

    参考 mcp-server-weread 实现:
    - 获取 weread.qq.com 域名的 cookie
    - 正确处理数组格式（Cookie Cloud标准格式）
    - 提供 fallback 到 weread 域名
    - **新增：也获取 qq.com 域名下的通用 cookie (RK, ptcz 等)**
    """
    try:
        cc_url = cc_url.rstrip('/')
        url = f"{cc_url}/get/{cc_id}"

        response = requests.post(
            url,
            json={"password": cc_password},
            timeout=10
        )

        if not response.ok:
            print(f"⚠️ Cookie Cloud请求失败: HTTP {response.status_code}")
            return None

        data = response.json()
        cookie_data = data.get("cookie_data", {})
        
        all_cookies = []

        # 方式1: 尝试从 weread.qq.com 域名获取（标准格式是数组）
        cookies = cookie_data.get("weread.qq.com")

        if isinstance(cookies, list) and len(cookies) > 0:
            # 正确的格式：数组对象 [{name: "xxx", value: "yyy"}, ...]
            for cookie in cookies:
                if isinstance(cookie, dict) and cookie.get("name") and cookie.get("value"):
                    all_cookies.append(f"{cookie['name']}={cookie['value']}")

        # 方式2: 尝试从 qq.com 域名获取通用 cookie (RK, ptcz, pgv_pvid 等)
        qq_cookies = cookie_data.get("qq.com")
        if isinstance(qq_cookies, list) and len(qq_cookies) > 0:
            for cookie in qq_cookies:
                if isinstance(cookie, dict) and cookie.get("name") and cookie.get("value"):
                    # 只获取与微信读书相关的通用 cookie
                    name = cookie.get("name")
                    if name in ["RK", "ptcz", "pgv_pvid", "fs_uid", "_clck"]:
                        all_cookies.append(f"{name}={cookie['value']}")

        # 方式3: Fallback - 尝试从 weread 域名获取（验证domain属性）
        if not all_cookies:
            cookies_alt = cookie_data.get("weread")
            if isinstance(cookies_alt, list) and len(cookies_alt) > 0:
                # 验证cookie的domain是否为weread.qq.com
                for cookie in cookies_alt:
                    if isinstance(cookie, dict):
                        domain = cookie.get("domain", "")
                        if domain in [".weread.qq.com", "weread.qq.com", ".qq.com", "qq.com"]:
                            if cookie.get("name") and cookie.get("value"):
                                all_cookies.append(f"{cookie['name']}={cookie['value']}")

        if all_cookies:
            print(f"✅ 从Cookie Cloud获取到 {len(all_cookies)} 个cookie")
            return "; ".join(all_cookies)

        print("⚠️ Cookie Cloud中未找到微信读书的有效cookie")
        return None

    except requests.exceptions.Timeout:
        print("⚠️ Cookie Cloud请求超时")
        return None
    except Exception as e:
        print(f"⚠️ Cookie Cloud获取失败: {e}")
        return None


def get_cookie() -> str:
    """获取微信读书 Cookie

    返回值:
        str: Cookie 字符串

    异常:
        ValueError: 未找到有效的 Cookie 配置

    注意:
        此函数只负责获取 cookie，不初始化 session
        请在获取 cookie 后手动调用 init_session()
        
    优先级调整说明:
        由于 Cookie Cloud 可能缺少 qq.com 域名下的关键 cookie (RK, ptcz 等),
        现在优先使用环境变量中的完整 cookie
    """
    # 1. 优先使用环境变量（包含完整的 cookie）
    env_cookie = os.getenv("WEREAD_COOKIE")
    if env_cookie:
        print("✓ 使用环境变量中的 WEREAD_COOKIE")
        return env_cookie

    # 2. 降级到 Cookie Cloud
    cc_url = os.getenv("CC_URL")
    cc_id = os.getenv("CC_ID")
    cc_password = os.getenv("CC_PASSWORD")

    if all([cc_url, cc_id, cc_password]):
        print("→ 尝试从 Cookie Cloud 获取...")
        cookie_string = try_get_cloud_cookie(cc_url, cc_id, cc_password)
        if cookie_string:
            # 检查是否包含关键 cookie
            if 'wr_skey' in cookie_string:
                print("⚠️ Cookie Cloud 返回的 cookie 可能不完整（缺少 RK, ptcz 等）")
                print("   建议在 .env 中设置完整的 WEREAD_COOKIE")
            return cookie_string

    # 3. 未找到任何配置
    raise ValueError(
        "未找到 Cookie 配置，请设置以下任一方式：\n"
        "1. 环境变量: WEREAD_COOKIE (推荐，包含完整 cookie)\n"
        "2. Cookie Cloud: CC_URL, CC_ID, CC_PASSWORD"
    )


def initialize_api() -> bool:
    """初始化微信读书 API

    这是推荐的初始化方式，会自动获取 cookie 并初始化 session

    返回值:
        bool: 初始化是否成功
    """
    try:
        cookie = get_cookie()
        init_session(cookie)
        return True
    except Exception as e:
        print(f"初始化失败: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    if not initialize_api():
        print("❌ 初始化失败")
        exit(1)

    books = get_notebooklist()
    print(f"✅ 获取到 {len(books)} 本书")

    if books:
        book = books[0]
        print(f"\n📖 书名: {book.get('book', {}).get('title', '未知')}")
        print(f"👤 作者: {book.get('book', {}).get('author', '未知')}")

        bookId = book.get("bookId")
        if bookId:
            bookmarks = get_bookmark_list(bookId)
            print(f"📝 划线数量: {len(bookmarks)}")


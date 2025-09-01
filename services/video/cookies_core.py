import asyncio
from playwright.async_api import async_playwright
import json
from pathlib import Path
from flask import current_app
from models import db, PlatformCookies, User
from flask_jwt_extended import get_jwt_identity

async def get_cookies_with_playwright(url: str, platform_name: str, user_id: int):
    """获取并存储网站Cookies到数据库
    
    Args:
        url: 登录页面URL
        platform_name: 平台名称 ('xiaohongshu', 'douyin', 'shipinhao')
        user_id: 用户ID
    Returns:
        dict: {'success': bool, 'message': str}
    """
    async with async_playwright() as p:
        # 启动浏览器（保留原有UI模式方便扫码）
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )
        
        # 创建上下文（隔离环境）
        context = await browser.new_context(
            viewport=None,  # 最大化窗口
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        )
        
        page = await context.new_page()
        
        try:
            # 导航到目标URL
            await page.goto(url, timeout=120000)
            print(f"请扫码登录（等待60秒）...")
            
            # 获取初始URL
            initial_url = page.url
            
            # 等待URL变化（表示登录成功跳转）
            await page.wait_for_function(
                """initialUrl => {
                    return location.href !== initialUrl;
                }""",
                arg=initial_url,
                timeout=60000
            )
            
            print("检测到页面跳转，登录成功")
            
            # 获取Cookies（包含所有安全属性）
            cookies = await context.cookies()
            
            # 标准化Cookie格式
            processed_cookies = []
            for cookie in cookies:
                processed_cookies.append({
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie["domain"],
                    "path": cookie["path"],
                    "expires": cookie.get("expires"),
                    "httpOnly": cookie["httpOnly"],
                    "secure": cookie["secure"],
                    "sameSite": cookie.get("sameSite", "Lax")
                })

            # 更新或创建数据库中的cookies记录
            platform_cookies = PlatformCookies.query.filter_by(
                user_id=user_id,
                platform_name=platform_name
            ).first()

            if platform_cookies:
                platform_cookies.cookies = processed_cookies
                platform_cookies.is_valid = True
            else:
                platform_cookies = PlatformCookies(
                    user_id=user_id,
                    platform_name=platform_name,
                    cookies=processed_cookies,
                    is_valid=True
                )
                db.session.add(platform_cookies)

            db.session.commit()
            return {'success': True, 'message': 'Cookies已成功保存到数据库'}
            
        except Exception as e:
            error_msg = f"获取Cookie失败: {str(e)}"
            print(error_msg)
            return {'success': False, 'message': error_msg}
        finally:
            await browser.close()

def check_cookies_validity(user_id: int, platform_name: str) -> bool:
    """检查指定平台的cookies是否有效
    
    Args:
        user_id: 用户ID
        platform_name: 平台名称
    
    Returns:
        bool: cookies是否有效
    """
    platform_cookies = PlatformCookies.query.filter_by(
        user_id=user_id,
        platform_name=platform_name,
        is_valid=True
    ).first()
    
    return bool(platform_cookies)

def get_platform_cookies(user_id: int, platform_name: str) -> dict:
    """获取指定平台的cookies
    
    Args:
        user_id: 用户ID
        platform_name: 平台名称
    
    Returns:
        dict: cookies数据，如果不存在则返回None
    """
    platform_cookies = PlatformCookies.query.filter_by(
        user_id=user_id,
        platform_name=platform_name,
        is_valid=True
    ).first()
    
    return platform_cookies.cookies if platform_cookies else None

def invalidate_cookies(user_id: int, platform_name: str):
    """将指定平台的cookies标记为无效
    
    Args:
        user_id: 用户ID
        platform_name: 平台名称
    """
    platform_cookies = PlatformCookies.query.filter_by(
        user_id=user_id,
        platform_name=platform_name
    ).first()
    
    if platform_cookies:
        platform_cookies.is_valid = False
        db.session.commit()

PLATFORM_LOGIN_URLS = {
    'xiaohongshu': 'https://creator.xiaohongshu.com/login',
    'douyin': 'https://creator.douyin.com/',
    'shipinhao': 'https://channels.weixin.qq.com/'
}
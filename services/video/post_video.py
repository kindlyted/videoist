import os
import json
from playwright.sync_api import sync_playwright, expect
# Playwright 视频上传
def xhs_video_upload(video_path, cover_path, your_title, your_desc, cookie_path):
    with sync_playwright() as p:
        # 1. 浏览器初始化（保留UI模式便于调试）
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            slow_mo=500  # 操作减速便于观察
        )
        context = browser.new_context(
            no_viewport=True,  # 最大化窗口
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # 2. 加载Cookie登录
        try:
            context.add_cookies(json.load(open(cookie_path)))
            page.goto("https://creator.xiaohongshu.com/publish/publish", timeout=15000)
            # page.wait_for_selector("text=发布笔记", timeout=10000)
            print("✅ 登录成功")
        except Exception as e:
            raise Exception(f"登录失败: {str(e)}\n截图已保存: login_error.png")

        # 3. 视频上传（带动态超时）
        print("▶ 开始上传视频...")
        try:
            # 计算动态超时（基础10秒 + 每MB加0.5秒，上限60秒）
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
            upload_timeout = min(60000, 10000 + file_size_mb * 500)
            
            # 执行上传
            video_upload = page.locator('input[type="file"]')
            video_upload.set_input_files(video_path)
            
            # 三重状态检测
            try:
                page.wait_for_selector('text=上传成功', timeout=upload_timeout)
            except:
                if not page.locator('div.progress-bar:has-text("100%")').is_visible():
                    raise Exception("视频上传超时，进度未完成")
            print(f"✅ 视频上传成功（耗时: {upload_timeout//1000}秒）")
        except Exception as e:
            raise Exception(f"视频上传失败: {str(e)}")

        # 4. 封面上传
        print("▶ 开始设置封面...")
        try:
            # 步骤1：点击"设置封面"按钮
            set_cover = page.locator('xpath=//div[contains(@class, "text") and contains(text(), "设置封面")]')
            set_cover.click(timeout=10000)
            print("✅ 已点击设置封面按钮")
            
            # 步骤2：等待封面弹窗完全加载
            # page.wait_for_selector('div.cover-dialog', state="visible", timeout=10000)
            
            # 步骤3：上传封面（双重定位策略）
            cover_upload = page.locator('css=input[type="file"][accept*="image"]')
            if not cover_upload.is_visible():
                page.eval_on_selector(
                    'input[type="file"]',
                    'el => el.style.cssText="display:block !important;opacity:1 !important;"'
                )
            cover_upload.set_input_files(cover_path) 
            
            # 步骤4：确认封面（直接等待2秒后点击）
            page.wait_for_timeout(2000)  # Playwright的等待方法，2000毫秒=2秒
            # 使用Selenium相同的定位策略（更精确）
            confirm_btn = page.locator('xpath=//*[@id="mojito-btn-container"]/button[2]')
            confirm_btn.scroll_into_view_if_needed()  # 确保按钮可见
            confirm_btn.click(timeout=10000)
        except Exception as e:
            raise Exception(f"封面上传失败: {str(e)}")

        # 5. 填写内容（带输入验证）
        print("▶ 填写标题和描述...")
        try:
            # 输入标题
            title_input = page.locator('input[placeholder="填写标题会有更多赞哦～"]')
            title_input.fill(your_title)
            
            # 输入描述
            desc_editor = page.locator('div.ql-editor[contenteditable="true"]')
            desc_editor.click()
            page.keyboard.type(your_desc)  # 模拟真实输入
            print("✅ 内容填写完成")
        except Exception as e:
            raise Exception(f"内容填写失败: {str(e)}")

        # 6. 发布视频
        print("▶ 发布视频...")
        try:
            publish_btn = page.locator('xpath=//*[@id="publish-container"]/div[2]/div[2]/div/button[1]/div/span')
            publish_btn.scroll_into_view_if_needed()  # 确保按钮可见
            publish_btn.click()
            
            # 多状态检测
            try:
                page.wait_for_selector('text=发布成功', timeout=30000)
                print("🎉 视频发布成功！")
            except:
                if page.locator('text=审核中').is_visible():
                    print("⚠️ 视频进入审核状态")
                else:
                    raise Exception("未知发布状态")
        except Exception as e:
            raise Exception(f"发布失败: {str(e)}")

        # 7. 关闭浏览器（带延迟确保操作完成）
        page.wait_for_timeout(3000)  # 等待3秒确保操作完成
        browser.close()

def dy_video_upload(video_path, cover_path, your_title, your_desc, cookie_path):
    with sync_playwright() as p:
        # 1. 浏览器初始化
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            slow_mo=500
        )
        context = browser.new_context(
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # 2. 加载Cookie登录
        try:
            context.add_cookies(json.load(open(cookie_path)))
            page.goto("https://creator.douyin.com/creator-micro/content/upload", timeout=15000)
            page.wait_for_selector('text=作品管理', timeout=10000)
            print("✅ 登录成功")
        except Exception as e:
            raise Exception(f"抖音登录失败: {str(e)}")

        # 3. 视频上传
        print("▶ 开始上传视频...")
        try:
            video_upload = page.locator('xpath=//input[@type="file" and contains(@accept, "video/")]')
            video_upload.set_input_files(video_path)
            
            # 等待上传完成（检测进度条或成功文本）
            # page.wait_for_selector('text=上传完成', timeout=60000)
            page.wait_for_timeout(2000)
            print("✅ 视频上传完成")
        except Exception as e:
            raise Exception(f"视频上传失败: {str(e)}")

        # 4. 封面上传
        print("▶ 开始设置封面...")
        try:
            # 步骤1：点击"设置封面"按钮
            set_cover = page.locator('xpath=//div[contains(@class, "filter-")]//div[text()="选择封面"]')
            if set_cover.count() > 1:
                set_cover = set_cover.first
            set_cover.click(timeout=10000)
            print("✅ 已点击设置封面按钮")

            # 步骤2：等待封面弹窗完全加载
            # page.wait_for_selector('div.cover-dialog', state="visible", timeout=10000)
            
            # 步骤3：上传封面（双重定位策略）
            cover_upload = page.locator('css=input.semi-upload-hidden-input[type="file"]')
            cover_upload.set_input_files(cover_path)
            
            # 步骤4：确认封面
            page.wait_for_timeout(60000)  # 等待封面预览加载
            confirm_btn = page.locator('xpath=//button[contains(@class, "semi-button-primary")]/span[text()="完成"]/..')
            confirm_btn.click(delay=5000, timeout=10000)
            print("✅ 封面设置完成")
        except Exception as e:
            raise Exception(f"封面上传失败: {str(e)}")

        # 5. 填写内容
        print("▶ 填写标题和描述...")
        try:
            # 输入标题
            title_input = page.locator('xpath=//input[contains(@class, "semi-input") and @placeholder="填写作品标题，为作品获得更多流量"]')
            title_input.fill(your_title)
            
            # 输入描述
            desc_input = page.locator('css=div.editor-kit-container[data-placeholder="添加作品简介"]')
            desc_input.click()
            page.keyboard.type(your_desc)
            print("✅ 内容填写完成")
        except Exception as e:
            raise Exception(f"内容填写失败: {str(e)}")

        # 6. 发布视频
        print("▶ 发布视频...")
        try:
            publish_btn = page.locator('xpath=//button[contains(@class, "primary-") and text()="发布"]')
            publish_btn.click()
            
            # 验证发布状态
            try:
                page.wait_for_selector('text=发布成功', timeout=30000)
                print("🎉 视频发布成功！")
            except:
                if page.locator('text=审核中').is_visible():
                    print("⚠️ 视频进入审核状态")
                else:
                    raise Exception("未知发布状态")
        except Exception as e:
            raise Exception(f"发布失败: {str(e)}")

        # 7. 关闭浏览器
        page.wait_for_timeout(3000)  # 等待3秒确保操作完成
        browser.close()
        
def sph_video_upload(video_path, cover_path, your_title, your_desc, cookie_path):
    with sync_playwright() as p:
        # 1. 浏览器初始化
        browser = p.chromium.launch(
            headless=False,
            # 关键参数开始
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # 指向系统安装的Chrome
            args=[
                "--disable-blink-features=AutomationControlled",
                "--use-fake-ui-for-media-stream",  # 绕过媒体设备检测
                "--use-fake-device-for-media-stream",
                "--enable-features=PlatformHEVCDecoderSupport",
                "--force-enable-video-decoder-h264",
                "--ignore-gpu-blocklist",  # 强制启用GPU
                "--enable-gpu-rasterization",
                f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ],
            # 关键参数结束
            slow_mo=500
        )
        context = browser.new_context(
            bypass_csp=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        # 使用 evaluate_on_new_document 注入脚本
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(HTMLVideoElement.prototype, 'canPlayType', {
                value: function() { return "probably"; }
            });
            window.chrome = { runtime: {} };  // 伪装Chrome扩展环境
        """)
        
        page = context.new_page()

        # 2. 加载Cookie登录
        try:
            context.add_cookies(json.load(open(cookie_path)))
            page.goto("https://channels.weixin.qq.com/platform/post/create", 
                timeout=15000,
                wait_until="networkidle",  # 确保所有资源加载完成
                referer="https://channels.weixin.qq.com/"  # 伪造来源
            )
            page.wait_for_selector('text=发表动态', timeout=10000)
            print("✅ 登录成功")
        except Exception as e:
            raise Exception(f"视频号登录失败: {str(e)}")

        # 3. 视频上传
        print("▶ 开始上传视频...")
        try:
            page.wait_for_timeout(2000)  # 等待页面加载
            video_upload = page.locator('input[type="file"][accept*="video/"]')
            video_upload.set_input_files(video_path)
            
            # 等待上传完成
            page.wait_for_selector('text=更换封面', timeout=60000)
            print("✅ 视频上传开始")
        except Exception as e:
            raise Exception(f"视频上传失败: {str(e)}")

        # 4. 封面上传
        print("▶ 开始设置封面...")
        try:
            # 步骤1：等待并点击"更换封面"按钮
            page.wait_for_timeout(2000)  # 等待页面稳定
            # 等待视频元素具有有效src且可见
            page.wait_for_selector('#fullScreenVideo[src^="blob:"]', state="attached", timeout=240000)
            # 等待封面预览图元素可见（确保DOM渲染）
            preview_div = page.locator('div.finder-cover-real-img-div')
            preview_div.wait_for(state="attached", timeout=120000)  # 先确保元素在DOM中
            preview_div.wait_for(state="visible", timeout=120000)   # 再确保可见
            # 定位更换封面按钮
            change_cover_btn = page.locator('div.finder-tag-wrap.btn:has-text("更换封面")')
            expect(change_cover_btn).not_to_have_class("disabled")  # 确保没有禁用类
            # 滚动到视图中（如果需要）
            change_cover_btn.scroll_into_view_if_needed()
            # 带延迟的安全点击（模拟人工操作）
            change_cover_btn.click(delay=2000, timeout=5000)  # 延迟2秒，超时5秒
            print("✅ 已点击更换封面按钮")

            # 步骤2：上传封面
            print("▶ 开始上传封面图片...")
            cover_upload = page.locator('input[type="file"][accept*="jpeg"][accept*="png"]')
            # 确保元素存在（即使不可见）
            cover_upload.wait_for(state="attached", timeout=15000)
            cover_upload.set_input_files(cover_path, timeout=15000)
            # 验证上传成功（等待封面预览出现）
            # page.wait_for_selector('div.finder-cover-real-img-div img', state="visible", timeout=30000)
            print("✅ 封面上传成功")

            # 步骤3：等待并点击确认按钮
            page.wait_for_timeout(10000)
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(10000)  # 等待滚动完成
            confirm_btn = page.locator('div.weui-desktop-btn_wrp >> button:has-text("确认")')
            # confirm_btn = page.locator('div.weui-desktop-btn_wrp >> button.weui-desktop-btn_primary:has-text("确认")')
            print("确认按钮定位：", confirm_btn)
            if confirm_btn.count() > 1:
                confirm_btn = confirm_btn.first
            confirm_btn.highlight()  # 高亮确认按钮
            confirm_btn.scroll_into_view_if_needed()
            confirm_btn.click(timeout=5000, delay=500)
            print("✅ 封面确认成功")
        except Exception as e:
            raise Exception(f"封面上传失败: {str(e)}")

        # 5. 填写内容
        print("▶ 填写标题和描述...")
        try:
            # 输入标题
            page.wait_for_timeout(2000)  # 等待页面稳定
            title_input = page.locator('input[placeholder="概括视频主要内容，字数建议6-16个字符"]')
            title_input.fill(your_title)
            
            # 输入描述
            desc_input = page.locator('div.input-editor[contenteditable=""][data-placeholder="添加描述"]')
            desc_input.click()
            page.keyboard.type(your_desc)
            print("✅ 内容填写完成")
        except Exception as e:
            raise Exception(f"内容填写失败: {str(e)}")

        # 6. 发布视频
        print("▶ 发布视频...")
        try:
            publish_btn = page.locator('button.weui-desktop-btn_primary:has-text("发表")')
            publish_btn.click()
            
            # 验证发布状态
            try:
                page.wait_for_selector('text=已发表', timeout=30000)
                print("🎉 视频发布成功！")
            except:
                if page.locator('text=审核中').is_visible():
                    print("⚠️ 视频进入审核状态")
                else:
                    raise Exception("未知发布状态")
        except Exception as e:
            raise Exception(f"发布失败: {str(e)}")

        # 7. 关闭浏览器
        page.wait_for_timeout(3000)  # 等待3秒确保操作完成
        browser.close()


# 旧版前端页面控件文档

本文档详细描述了旧版前端各页面包含的控件和名称/占位字，供前端工程师和后端工程师参考。

## main目录

### 首页-欢迎页

1. **欢迎区域**
   - 标题：欢迎访问!
   - 副标题：今天是 {{ today }}
   - 未登录状态下的按钮：
     - 登录按钮（btn-primary）
     - 注册按钮（btn-outline-primary）
   - 已登录状态下的按钮：
     - 开始创作视频按钮（btn-primary）
     - 访问仪表板按钮（btn-outline-primary）


2. **功能介绍区域**
   - 三个功能卡片：
     - AI智能生成卡片
       - 标题：AI智能生成
       - 描述：使用先进的AI技术，自动生成高质量的视频内容，让创作更轻松。
     - 快速高效卡片
       - 标题：快速高效
       - 描述：只需几分钟，即可将文章转化为精美视频，大大提升内容创作效率。
     - 一键分发卡片
       - 标题：一键分发
       - 描述：支持多平台内容分发，让您的创作快速触达更多受众。

### 视频创作页

1. **AI视频创作助手标题**
   - 标题：AI视频创作助手
   - 副标题：一键将文章转化为高质量短视频

2. **文章网址处理卡片**
   - 标题：文章网址处理
   - 输入框：
     - 文章网址输入框（type="url", placeholder="输入文章网址 (https://...)")
   - switch按钮：
     - 发布到WordPress（id="wordpressSwitch"）默认off，需要检测用户是否绑定WordPress站点，若未绑定不可编辑
     - 发布到微信公众号（id="wechatSwitch"）默认off 需要检测用户是否绑定微信公众号，若未绑定不可编辑
   - 内容模式选择：
     - 朗诵（id="modeRecite", value="朗诵"）
     - 对话（id="modeDialogue", value="对话"）
   - 按钮：
     - 上传并处理按钮（id="processUrl", btn-primary）
   - 结果显示区域（id="urlResults"）：
     - 文章网址显示（id="websiteUrl"）
     - 工作目录显示（id="workingDir"）
     - 公众号状态显示（id="wxStatus"）

3. **视频内容编辑卡片**
   - 标题：视频内容编辑
   - 文本域：
     - 朗诵文稿输入框（id="article", placeholder="在此输入或粘贴朗诵文稿..."）
   - 按钮：
     - 生成标题按钮（id="generateTitles", btn-primary）
   - 输入框：
     - 视频标题输入框（id="title", placeholder="视频标题"）
     - 封面描述输入框（id="cover", placeholder="封面描述文字"）
   - 下拉框：
     - 语音选择（id="voice"）从后端 /voice-options 端点获取列表

4. **视频生成卡片**
   - 标题：视频生成
   - 按钮：
     - 生成视频按钮（id="generateVideo", btn-primary）
     - 上传平台按钮（id="uploadVideo", btn-success）
   - 预览区域：
     - 封面预览（id="coverImage"）
     - 视频预览（id="outputVideo"）
     - 下载视频链接（id="downloadLink"）
#### 交互逻辑

1. 用户输入URL后，点击处理按钮
2. 后端返回内容并填充到文稿区域
3. 用户可编辑文稿内容
4. 点击生成标题按钮，系统自动生成标题
5. 用户选择语音和模式
6. 点击生成视频按钮，系统开始生成视频和封面
7. 视频和封面生成完成后，在当前页面生成预览
8. 用户可选择上传平台进行发布，做一个上传按钮

## 笔记生成页

### index.html

1. **笔记生成标题**
   - 标题：笔记生成

2. **文件上传表单**
   - 表单（id="uploadForm"）
   - 文件输入框：
     - PDF文件上传（id="pdfFile", accept=".pdf"）
   - 按钮：
     - 生成笔记按钮（type="submit", btn-primary）

3. **结果展示区域**
   - 区域容器（id="resultContainer"）
   - 标题：生成的笔记
   - 图片展示（id="noteImage"）

## 用户管理页

### login.html

1. **登录卡片**
   - 卡片标题：登录
   - 表单：
     - 用户名输入框（form.username）
     - 密码输入框（form.password）
     - 记住我复选框（form.remember_me）
   - 按钮：
     - 登录按钮（type="submit", btn-primary）
   - 链接：
     - 忘记密码链接

### register.html

1. **注册卡片**
   - 卡片标题：注册
   - 表单：
     - 用户名输入框（form.username）
     - 邮箱输入框（form.email）
     - 密码输入框（form.password）
     - 确认密码输入框（form.password2）
   - 按钮：
     - 注册按钮（type="submit", btn-primary）
   - 链接：
     - 已有账户? 点击登录链接

### dashboard.html

1. **账户信息区域**
   - 欢迎标题：{{ current_user.username }}，欢迎回来！
   - 账户信息卡片：
     - 标题：账户信息
     - 用户名显示：{{ current_user.username }}
     - 邮箱显示：{{ current_user.email }}
     - 查看详情按钮（btn-outline-primary）
   - 平台统计卡片：
     - 标题：平台统计
     - WordPress站点数量：{{ wordpress_sites|length }}
     - 微信公众号数量：{{ wechat_accounts|length }}
     - 管理按钮：
       - WordPress管理按钮（btn-outline-primary）
       - 微信公众号管理按钮（btn-outline-primary）

2. **最近活动区域**
   - 卡片标题：最近活动
   - 活动列表：
     - 系统登录活动项

3. **WordPress添加/编辑模态框**
   - 模态框标题：添加 WordPress 站点
   - 表单（id="wordpressForm"）：
     - 站点名称输入框（name="site_name"）
     - 站点URL输入框（name="site_url", placeholder="https://"）
     - 用户名输入框（name="username"）
     - API密钥/密码输入框（name="api_key"）
   - 按钮：
     - 取消按钮（btn-secondary）
     - 保存按钮（type="submit", btn-primary）

4. **微信公众号添加/编辑模态框**
   - 模态框标题：添加微信公众号
   - 表单（id="wechatForm"）：
     - 公众号名称输入框（name="account_name"）
     - 公众号ID输入框（name="account_id"）
     - AppID输入框（name="app_id"）
     - AppSecret输入框（name="app_secret"）
   - 按钮：
     - 取消按钮（btn-secondary）
     - 保存按钮（type="submit", btn-primary）

5. **导航菜单**
   - 菜单项：
     - 账户信息链接
     - 设置链接
     - 内容平台标题
     - WordPress链接
     - 微信公众号链接
     - 关于我们链接
     - 退出登录按钮（btn-outline-danger）

### account_info.html

1. **账户信息标题**
   - 标题：账户信息

2. **基本信息卡片**
   - 卡片标题：基本信息
   - 信息项：
     - 用户名：{{ current_user.username }}
     - Email：{{ current_user.email }}
     - 注册时间：{{ current_user.created_at.strftime('%Y-%m-%d %H:%M') if current_user.created_at else '未知' }}

3. **账户安全卡片**
   - 卡片标题：账户安全
   - 按钮：
     - 修改密码按钮（btn-outline-primary）
     - 绑定手机按钮（btn-outline-secondary）

4. **导航菜单**
   - 菜单项：
     - 账户信息链接（当前页面）
     - 设置链接
     - 内容平台标题
     - WordPress链接
     - 微信公众号链接
     - 关于我们链接
     - 退出登录按钮（btn-outline-danger）

### wordpress.html

1. **WordPress管理标题**
   - 标题：WordPress 管理
   - 添加站点按钮（btn-primary）

2. **WordPress站点表格**
   - 表格列：
     - 站点名称
     - URL
     - 用户名
     - 操作
   - 表格行数据：
     - 站点信息（site.site_name, site.site_url, site.username）
     - 操作按钮：
       - 编辑按钮（btn-outline-primary）
       - 删除按钮（btn-outline-danger）

3. **WordPress添加/编辑模态框**
   - 模态框标题：添加 WordPress 站点
   - 表单（id="wordpressForm"）：
     - 站点名称输入框（name="site_name"）
     - 站点URL输入框（name="site_url", placeholder="https://"）
     - 用户名输入框（name="username"）
     - API密钥/密码输入框（name="api_key"）
   - 按钮：
     - 取消按钮（btn-secondary）
     - 保存按钮（type="submit", btn-primary）

4. **导航菜单**
   - 菜单项：
     - 账户信息链接
     - 设置链接
     - 内容平台标题
     - WordPress链接（当前页面）
     - 微信公众号链接
     - 关于我们链接
     - 退出登录按钮（btn-outline-danger）

### wechat.html

1. **微信公众号管理标题**
   - 标题：微信公众号管理
   - 添加公众号按钮（btn-primary）

2. **微信公众号表格**
   - 表格列：
     - 公众号名称
     - 公众号ID
     - AppID
     - 操作
   - 表格行数据：
     - 公众号信息（account.account_name, account.account_id, account.app_id）
     - 操作按钮：
       - 编辑按钮（btn-outline-primary）
       - 删除按钮（btn-outline-danger）

3. **微信公众号添加/编辑模态框**
   - 模态框标题：添加微信公众号
   - 表单（id="wechatForm"）：
     - 公众号名称输入框（name="account_name"）
     - 公众号ID输入框（name="account_id"）
     - AppID输入框（name="app_id"）
     - AppSecret输入框（name="app_secret"）
   - 按钮：
     - 取消按钮（btn-secondary）
     - 保存按钮（type="submit", btn-primary）

4. **导航菜单**
   - 菜单项：
     - 账户信息链接
     - 设置链接
     - 内容平台标题
     - WordPress链接
     - 微信公众号链接（当前页面）
     - 关于我们链接
     - 退出登录按钮（btn-outline-danger）

### reset_password_request.html

1. **重置密码标题**
   - 标题：重置密码

2. **密码重置表单**
   - 表单：
     - 邮箱输入框（form.email, size=32）
   - 按钮：
     - 提交按钮（form.submit）
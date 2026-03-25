from enum import Enum

class ErrorCode(Enum):
    # 用户认证相关错误
    USERNAME_OR_PASSWORD_ERROR = "USER_001"
    USER_NOT_FOUND = "USER_002"
    CURRENT_PASSWORD_ERROR = "USER_003"
    MISSING_REQUIRED_FIELDS = "USER_004"
    MISSING_USERNAME_OR_PASSWORD = "USER_005"
    USERNAME_EXISTS = "USER_006"
    EMAIL_EXISTS = "USER_007"
    
    # WordPress相关错误
    WORDPRESS_SITE_NOT_FOUND = "WP_001"
    WORDPRESS_SITE_EXISTS = "WP_002"
    
    # 微信公众号相关错误
    WECHAT_ACCOUNT_NOT_FOUND = "WX_001"
    WECHAT_APPID_EXISTS = "WX_002"
    
    # 密码重置相关错误
    MISSING_EMAIL = "RESET_001"
    MISSING_PASSWORD = "RESET_002"
    
    # 验证码相关错误
    INVALID_VERIFICATION_CODE = "VERIFY_001"
    EXPIRED_VERIFICATION_CODE = "VERIFY_002"

    # 邮件相关错误
    EMAIL_SEND_FAILED = "EMAIL_001"

    # OAuth相关错误
    INVALID_TOKEN = "OAUTH_001"

    # 系统错误
    SYSTEM_ERROR = "SYS_001"
    
    # 通用错误
    UNKNOWN_ERROR = "COMMON_001"
    INVALID_PLATFORM = "COMMON_002"
    
    # 登出相关错误
    LOGOUT_SUCCESS = "LOGOUT_001"
    
    # 文件处理相关错误
    NO_FILE_SELECTED = "FILE_001"
    FILE_TYPE_NOT_SUPPORTED = "FILE_002"
    FILE_PROCESSING_SUCCESS = "FILE_003"
    FILE_PROCESSING_ERROR = "FILE_004"
    
    # 视频处理相关错误
    COVER_DESCRIPTION_REQUIRED = "VIDEO_001"
    WORDPRESS_PUBLISH_SKIPPED = "VIDEO_002"
    IMAGE_PROCESSING_SKIPPED = "VIDEO_003"
    WECHAT_PUBLISH_SKIPPED = "VIDEO_004"
    WECHAT_PUBLISH_SUCCESS = "VIDEO_005"
    WECHAT_PUBLISH_FAILED = "VIDEO_006"
    VIDEO_GENERATION_SUCCESS = "VIDEO_007"
    VIDEO_GENERATION_ERROR = "VIDEO_008"
    VIDEO_DELETION_SUCCESS = "VIDEO_009"
    VIDEO_NOT_FOUND = "VIDEO_010"
    VIDEO_ACCESS_DENIED = "VIDEO_011"
    VIDEO_DELETION_DENIED = "VIDEO_012"
    
    # 笔记处理相关错误
    NOTE_DELETION_SUCCESS = "NOTE_001"
    NOTE_NOT_FOUND = "NOTE_002"
    NOTE_ACCESS_DENIED = "NOTE_003"
    NOTE_DELETION_DENIED = "NOTE_004"
    
    # 平台登录相关错误
    USER_NOT_LOGGED_IN = "PLATFORM_001"
    PLATFORM_NOT_SPECIFIED = "PLATFORM_002"
    INVALID_PLATFORM_NAME = "PLATFORM_003"
    COOKIES_INVALID = "PLATFORM_004"

# 中文错误信息映射表
ERROR_MESSAGES_ZH = {
    ErrorCode.USERNAME_OR_PASSWORD_ERROR: "用户名或密码错误",
    ErrorCode.USER_NOT_FOUND: "用户不存在",
    ErrorCode.CURRENT_PASSWORD_ERROR: "当前密码错误",
    ErrorCode.MISSING_REQUIRED_FIELDS: "缺少必要字段",
    ErrorCode.MISSING_USERNAME_OR_PASSWORD: "必须提供用户名和密码",
    ErrorCode.USERNAME_EXISTS: "用户名已存在",
    ErrorCode.EMAIL_EXISTS: "邮箱已被注册",
    ErrorCode.WORDPRESS_SITE_NOT_FOUND: "站点不存在或无权访问",
    ErrorCode.WORDPRESS_SITE_EXISTS: "该站点URL已存在",
    ErrorCode.WECHAT_ACCOUNT_NOT_FOUND: "公众号不存在或无权访问",
    ErrorCode.WECHAT_APPID_EXISTS: "该AppID已存在",
    ErrorCode.MISSING_EMAIL: "必须提供邮箱地址",
    ErrorCode.MISSING_PASSWORD: "必须提供新密码",
    ErrorCode.INVALID_VERIFICATION_CODE: "验证码无效",
    ErrorCode.EXPIRED_VERIFICATION_CODE: "验证码已过期",
    ErrorCode.EMAIL_SEND_FAILED: "发送邮件失败",
    ErrorCode.INVALID_TOKEN: "令牌无效",
    ErrorCode.SYSTEM_ERROR: "系统错误",
    ErrorCode.UNKNOWN_ERROR: "未知错误",
    ErrorCode.INVALID_PLATFORM: "必须指定平台名称",
    
    # 登出相关错误
    ErrorCode.LOGOUT_SUCCESS: "成功登出",
    
    # 文件处理相关错误
    ErrorCode.NO_FILE_SELECTED: "未选择文件",
    ErrorCode.FILE_TYPE_NOT_SUPPORTED: "仅支持PDF文件",
    ErrorCode.FILE_PROCESSING_SUCCESS: "文件处理成功",
    ErrorCode.FILE_PROCESSING_ERROR: "服务器内部错误",
    
    # 视频处理相关错误
    ErrorCode.COVER_DESCRIPTION_REQUIRED: "请补充封面描述",
    ErrorCode.WORDPRESS_PUBLISH_SKIPPED: "WordPress发布已跳过",
    ErrorCode.IMAGE_PROCESSING_SKIPPED: "图片处理已跳过",
    ErrorCode.WECHAT_PUBLISH_SKIPPED: "公众号发布已跳过",
    ErrorCode.WECHAT_PUBLISH_SUCCESS: "公众号发布成功",
    ErrorCode.WECHAT_PUBLISH_FAILED: "公众号发布失败",
    ErrorCode.VIDEO_GENERATION_SUCCESS: "视频生成成功",
    ErrorCode.VIDEO_GENERATION_ERROR: "生成视频时出错",
    ErrorCode.VIDEO_DELETION_SUCCESS: "视频删除成功",
    ErrorCode.VIDEO_NOT_FOUND: "用户不存在",
    ErrorCode.VIDEO_ACCESS_DENIED: "无权访问此视频",
    ErrorCode.VIDEO_DELETION_DENIED: "无权删除此视频",
    
    # 笔记处理相关错误
    ErrorCode.NOTE_DELETION_SUCCESS: "笔记删除成功",
    ErrorCode.NOTE_NOT_FOUND: "用户不存在",
    ErrorCode.NOTE_ACCESS_DENIED: "无权访问此笔记",
    ErrorCode.NOTE_DELETION_DENIED: "无权删除此笔记",
    
    # 平台登录相关错误
    ErrorCode.USER_NOT_LOGGED_IN: "用户未登录",
    ErrorCode.PLATFORM_NOT_SPECIFIED: "未指定平台",
    ErrorCode.INVALID_PLATFORM_NAME: "无效的平台",
    ErrorCode.COOKIES_INVALID: "cookies无效"
}

# 英文错误信息映射表
ERROR_MESSAGES_EN = {
    ErrorCode.USERNAME_OR_PASSWORD_ERROR: "Username or password error",
    ErrorCode.USER_NOT_FOUND: "User not found",
    ErrorCode.CURRENT_PASSWORD_ERROR: "Current password error",
    ErrorCode.MISSING_REQUIRED_FIELDS: "Missing required fields",
    ErrorCode.MISSING_USERNAME_OR_PASSWORD: "Username and password are required",
    ErrorCode.USERNAME_EXISTS: "Username already exists",
    ErrorCode.EMAIL_EXISTS: "Email already registered",
    ErrorCode.WORDPRESS_SITE_NOT_FOUND: "Site not found or access denied",
    ErrorCode.WORDPRESS_SITE_EXISTS: "Site URL already exists",
    ErrorCode.WECHAT_ACCOUNT_NOT_FOUND: "WeChat account not found or access denied",
    ErrorCode.WECHAT_APPID_EXISTS: "AppID already exists",
    ErrorCode.MISSING_EMAIL: "Email address is required",
    ErrorCode.MISSING_PASSWORD: "New password is required",
    ErrorCode.INVALID_VERIFICATION_CODE: "Invalid verification code",
    ErrorCode.EXPIRED_VERIFICATION_CODE: "Expired verification code",
    ErrorCode.EMAIL_SEND_FAILED: "Failed to send email",
    ErrorCode.INVALID_TOKEN: "Invalid token",
    ErrorCode.SYSTEM_ERROR: "System error",
    ErrorCode.UNKNOWN_ERROR: "Unknown error",
    ErrorCode.INVALID_PLATFORM: "Platform name is required",
    
    # 登出相关错误
    ErrorCode.LOGOUT_SUCCESS: "Logout successful",
    
    # 文件处理相关错误
    ErrorCode.NO_FILE_SELECTED: "No file selected",
    ErrorCode.FILE_TYPE_NOT_SUPPORTED: "Only PDF files are supported",
    ErrorCode.FILE_PROCESSING_SUCCESS: "File processing successful",
    ErrorCode.FILE_PROCESSING_ERROR: "Internal server error",
    
    # 视频处理相关错误
    ErrorCode.COVER_DESCRIPTION_REQUIRED: "Please provide cover description",
    ErrorCode.WORDPRESS_PUBLISH_SKIPPED: "WordPress publishing skipped",
    ErrorCode.IMAGE_PROCESSING_SKIPPED: "Image processing skipped",
    ErrorCode.WECHAT_PUBLISH_SKIPPED: "WeChat publishing skipped",
    ErrorCode.WECHAT_PUBLISH_SUCCESS: "WeChat publishing successful",
    ErrorCode.WECHAT_PUBLISH_FAILED: "WeChat publishing failed",
    ErrorCode.VIDEO_GENERATION_SUCCESS: "Video generation successful",
    ErrorCode.VIDEO_GENERATION_ERROR: "Error generating video",
    ErrorCode.VIDEO_DELETION_SUCCESS: "Video deleted successfully",
    ErrorCode.VIDEO_NOT_FOUND: "User not found",
    ErrorCode.VIDEO_ACCESS_DENIED: "Access denied to this video",
    ErrorCode.VIDEO_DELETION_DENIED: "Deletion denied for this video",
    
    # 笔记处理相关错误
    ErrorCode.NOTE_DELETION_SUCCESS: "Note deleted successfully",
    ErrorCode.NOTE_NOT_FOUND: "User not found",
    ErrorCode.NOTE_ACCESS_DENIED: "Access denied to this note",
    ErrorCode.NOTE_DELETION_DENIED: "Deletion denied for this note",
    
    # 平台登录相关错误
    ErrorCode.USER_NOT_LOGGED_IN: "User not logged in",
    ErrorCode.PLATFORM_NOT_SPECIFIED: "Platform not specified",
    ErrorCode.INVALID_PLATFORM_NAME: "Invalid platform",
    ErrorCode.COOKIES_INVALID: "Invalid cookies"
}
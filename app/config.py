import os
from dotenv import load_dotenv


class Config:
    
    
    # 应用行为配置
    MAX_INPUT_LENGTH = 100  # 用户输入最大字符数
    
    # 安全配置
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB文件上传限制

# 可选的多环境配置继承
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True


import os
from dotenv import load_dotenv

API_KEY_0 = "sk-b8e09876066e40aab6ee92ba4a12629b"
API_KEY_1 = "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo"
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


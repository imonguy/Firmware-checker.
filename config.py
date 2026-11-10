import os
from dotenv import load_dotenv

# Load biến môi trường từ tệp .env (nếu chạy local)
load_dotenv()

class Config:
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "sk-ant-api03-placeholder-key")
    APP_VERSION = "Pre-Alpha 2"
    ENVIRONMENT = "production" # hoặc development

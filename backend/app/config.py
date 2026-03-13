from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./chat.db")

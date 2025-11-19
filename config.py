from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).resolve().parent

_base_config = SettingsConfigDict(
    env_file=PROJECT_DIR / ".env",
    env_ignore_empty=True,
    extra="ignore",
)


class AppSettings(BaseSettings):
    APP_NAME: str = "FastPOC"
    APP_DOMAIN: str = "localhost:8000"

    model_config = _base_config  # 명시적 추가 (기존 없음)


class DatabaseSettings(BaseSettings):
    # MySQL 연결 설정 (기본값: 테스트 계정 및 poc DB)
    MYSQL_HOST: str = Field(default="localhost")
    MYSQL_PORT: int = Field(default=3306)
    MYSQL_USER: str = Field(default="test")
    MYSQL_PASSWORD: str = Field(default="")  # 환경변수에서 로드
    MYSQL_DB: str = Field(default="poc")

    # Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = _base_config

    @property
    def MYSQL_URL(self) -> str:
        """비동기 MySQL URL 생성 (aiomysql 드라이버 사용, SQLAlchemy 통합 최적화)"""
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    def REDIS_URL(self, db: int = 0) -> str:
        """Redis URL 생성 (db 인수로 기본값 지원)"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"


class SecuritySettings(BaseSettings):
    JWT_SECRET: str = "your-jwt-secret-key"  # 기본값 추가 (필수 필드 안전)
    JWT_ALGORITHM: str = "HS256"  # 기본값 추가 (필수 필드 안전)

    model_config = _base_config


class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str = "your-email@example.com"  # 기본값 추가
    MAIL_PASSWORD: str = "your-email-password"  # 기본값 추가
    MAIL_FROM: str = "your-email@example.com"  # 기본값 추가
    MAIL_PORT: int = 587  # 기본값 추가
    MAIL_SERVER: str = "smtp.gmail.com"  # 기본값 추가
    MAIL_FROM_NAME: str = "FastPOC App"  # 기본값 추가
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    TWILIO_SID: str = "your-twilio-sid"  # 기본값 추가
    TWILIO_AUTH_TOKEN: str = "your-twilio-token"  # 기본값 추가
    TWILIO_NUMBER: str = "+1234567890"  # 기본값 추가

    model_config = _base_config


app_settings = AppSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()

templates_dir = PROJECT_DIR / "app" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))
print(f"templates path : {templates}")

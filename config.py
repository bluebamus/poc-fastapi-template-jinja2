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


class ProjectSettings(BaseSettings):
    PROJECT_NAME: str = Field(default="POC FastAPI Template Jinja2")
    PROJECT_DOMAIN: str = Field(default="localhost:8000")
    VERSION: str = Field(default="0.1.0")
    DESCRIPTION: str = Field(default="FastAPI 기반 POC 템플릿 프로젝트")
    ADMIN_BASE_URL: str = Field(default="/admin")

    model_config = _base_config


class CORSSettings(BaseSettings):
    # CORS (Cross-Origin Resource Sharing) 설정

    # 요청을 허용할 출처(Origin) 목록
    # ["*"]: 모든 출처 허용 (개발 환경용, 프로덕션에서는 구체적인 도메인 지정 권장)
    # 예: ["https://example.com", "https://app.example.com"]
    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    # 자격 증명(쿠키, Authorization 헤더 등) 포함 요청 허용 여부
    # True: 클라이언트가 credentials: 'include'로 요청 시 쿠키/인증 정보 전송 가능
    # 주의: CORS_ALLOW_ORIGINS가 ["*"]일 때는 보안상 False 권장
    CORS_ALLOW_CREDENTIALS: bool = True

    # 허용할 HTTP 메서드 목록
    # ["*"]: 모든 메서드 허용 (GET, POST, PUT, DELETE, PATCH, OPTIONS 등)
    # 구체적 지정 예: ["GET", "POST", "PUT", "DELETE"]
    CORS_ALLOW_METHODS: list[str] = ["*"]

    # 클라이언트가 요청 시 사용할 수 있는 HTTP 헤더 목록
    # ["*"]: 모든 헤더 허용
    # 구체적 지정 예: ["Content-Type", "Authorization", "X-Custom-Header"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # 브라우저의 JavaScript에서 접근 가능한 응답 헤더 목록
    # []: 기본 안전 헤더(Cache-Control, Content-Language, Content-Type,
    #     Expires, Last-Modified, Pragma)만 접근 가능
    # 추가 노출 필요 시: ["X-Total-Count", "X-Request-Id", "X-Custom-Header"]
    CORS_EXPOSE_HEADERS: list[str] = []

    # Preflight 요청(OPTIONS) 결과를 캐시하는 시간(초)
    # 600: 10분간 캐시 (이 시간 동안 동일 요청에 대해 preflight 생략)
    # 0으로 설정 시 매번 preflight 요청 발생
    CORS_MAX_AGE: int = 600

    model_config = _base_config


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
        """비동기 MySQL URL 생성 (asyncmy 드라이버 사용, SQLAlchemy 통합 최적화)"""
        return f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

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


prj_settings = ProjectSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()
cors_settings = CORSSettings()

templates_dir = PROJECT_DIR / "app" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))
print(f"templates path : {templates}")

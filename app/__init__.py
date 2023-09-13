from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import config


engine = create_engine(
    f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_DATABASE}?charset=utf8",
    pool_pre_ping=True,
    echo=False,
    pool_recycle=500,
    pool_size=30,
    max_overflow=20,
)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


def create_app():
    app = FastAPI(title="I.GPT API에 오신 걸 환영합니다!", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    from app.router.user_router import user_router
    from app.router.interview_router import interview_router

    app.include_router(user_router)
    app.include_router(interview_router)

    return app

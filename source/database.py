from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Дополнительно: можно скрыть логин и пароль от БД, поместив их в переменные окружения .env.
# Посколькув тестовом задании используется локально развернутая БД, в этом нет необходимости.

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
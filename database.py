from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    is_active = Column(Boolean, default=False)
    subscription_end = Column(String)  # Дата окончания подписки
    config_uuid = Column(String)       # Уникальный UUID для конфига

# Подключение к БД
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db():
    return Session()
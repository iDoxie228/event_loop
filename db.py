import asyncio
import asyncpg
import os
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv('POSTGRES_DB', 'asyncdb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'sema')
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

DSN = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
engine = create_async_engine(DSN)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
    
    
class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name= Column(String(50))
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(String(50))
    mass = Column(String(50))
    skin_color = Column(String(50))
    homeworld = Column(String(50))
    films = Column(Text)
    species = Column(Text)
    starships = Column(Text)
    vehicles = Column(Text)
    url = Column(Text)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_people(people):
    async with Session() as session:
        session.add_all([People(**p) for p in people])
        await session.commit()




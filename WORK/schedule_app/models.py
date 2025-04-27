# models.py
from sqlalchemy import Column, Integer, String, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from db import Base

class RoleEnum(enum.Enum):
    student = 'Ученик'
    parent  = 'Родитель'
    admin   = 'Администратор'

class User(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True)
    username      = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role          = Column(Enum(RoleEnum), nullable=False)

class Schedule(Base):
    __tablename__ = 'schedules'
    id         = Column(Integer, primary_key=True)
    subject    = Column(String, nullable=False)
    teacher    = Column(String, nullable=False)
    date       = Column(Date,   nullable=False)   # <-- теперь дата, а не день недели
    start_time = Column(Time,   nullable=False)
    end_time   = Column(Time,   nullable=False)
    room       = Column(String)
    type       = Column(String)

    homeworks = relationship(
        "Homework", back_populates="schedule", cascade="all, delete-orphan"
    )

class Homework(Base):
    __tablename__ = 'homeworks'
    id          = Column(Integer, primary_key=True)
    title       = Column(String, nullable=False)
    description = Column(String)
    due_date    = Column(Date)
    status      = Column(String, default='Не начато')
    attachment  = Column(String)
    schedule_id = Column(Integer, ForeignKey('schedules.id'))

    schedule = relationship("Schedule", back_populates="homeworks")

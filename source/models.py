from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base, SessionLocal, engine


class Tnved1(Base):
    __tablename__ = "TNVED1"
    id = Column(Integer, primary_key=True, name='id', nullable=False)
    section = Column(Integer, name='RAZDEL', nullable=False)  # Разделы ТН ВЭД
    name = Column(String, name='NAIM')  # Наименование
    comment = Column(String, name='PRIM')  # Примечание
    start_date = Column(Date, name='DATA', nullable=False)  # Дата начала действия раздела
    finish_date = Column(Date, name='DATA1')  # Дата окончания действия раздела


class Tnved2(Base):
    __tablename__ = "TNVED2"
    id = Column(Integer, primary_key=True, name='id', nullable=False)
    parent_id = Column(Integer, ForeignKey('TNVED1.id'), name='parent_id')
    tnved1 = relationship(Tnved1)  # указываем на родителя
    section = Column(Integer, name='RAZDEL', nullable=False)  # Разделы
    group = Column(Integer, name='GRUPPA', nullable=False)  # Группы ТН ВЭД
    name = Column(String, name='NAIM')  # Наименование
    comment = Column(String, name='PRIM')  # Примечание
    start_date = Column(Date, name='DATA', nullable=False)  # Дата начала действия раздела
    finish_date = Column(Date, name='DATA1')  # Дата окончания действия раздела


class Tnved3(Base):
    __tablename__ = "TNVED3"
    id = Column(Integer, primary_key=True, name='id', nullable=False)
    parent_id = Column(Integer, ForeignKey('TNVED2.id'), name='parent_id')
    tnved2 = relationship(Tnved2)
    group = Column(Integer, name='GRUPPA', nullable=False)  # Группы ТН ВЭД
    position = Column(Integer, name='TOV_POZ', nullable=False)  # Товарные позиции
    name = Column(String, name='NAIM')  # Наименование
    start_date = Column(Date, name='DATA', nullable=False)  # Дата начала действия раздела
    finish_date = Column(Date, name='DATA1')  # Дата окончания действия раздела


class Tnved4(Base):
    __tablename__ = "TNVED4"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TNVED3.id'), name='parent_id')
    tnved2 = relationship(Tnved3)
    group = Column(Integer, name='GRUPPA', nullable=False)  # Группы ТН ВЭД
    position = Column(Integer, name='TOV_POZ', nullable=False)  # Товарные позиции
    sub_position = Column(Integer, name='SUB_POZ', nullable=False)  # Товарные позиции
    short_name = Column(String, name='KR_NAIM', nullable=False)  # Товарные позиции
    start_date = Column(Date, name='DATA', nullable=False)  # Дата начала действия раздела
    finish_date = Column(Date, name='DATA1')  # Дата окончания действия раздела


if __name__ == "__main__":
    Base.metadata.create_all(engine)

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Integer
from database.main import Base

class Pet(Base):
    __tablename__ = "pets"

    owner_id = Column(BigInteger, nullable=False)

    pet_id = Column(BigInteger, primary_key=True, index=True)
    pet_name = Column(String, nullable=False)
    pet_type = Column(String, nullable=False)

    pet_birthday = Column(DateTime, nullable=False)

    pet_hunger = Column(Integer, default=100)
    pet_happiness = Column(Integer, default=100)
    pet_health = Column(Integer, default=100)
    pet_lvl = Column(BigInteger, default=1)
    pet_xp = Column(BigInteger, default=0)



    pet_escaped = Column(Boolean, default=False)
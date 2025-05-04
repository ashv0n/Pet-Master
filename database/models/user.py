from sqlalchemy import Column, BigInteger, String, Boolean
from database.main import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String)

    user_pet_id = Column(BigInteger, nullable=True)

    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)  


from sqlalchemy import Column, BigInteger, String, Boolean, Date
from database.main import Base

class Issue(Base):
    __tablename__ = "issues"
    
    issue_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    issue_date = Column(Date, nullable=False)

    user_id = Column(BigInteger, nullable=False)

    issue_text = Column(String, nullable=False)
    issue_status = Column(String, default="open")

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class League(Base):
    __tablename__ = "championship_links"  # Replace with your actual table name
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    sport = Column(String, nullable=False)
    country = Column(String, nullable=False)
    league = Column(String, nullable=False)

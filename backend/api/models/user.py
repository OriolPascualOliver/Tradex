from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from backend.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    device_id = Column(String, nullable=True)

    # Registration fields
    license = Column(String, nullable=True)
    team_members = Column(Integer, nullable=True)
    telephone = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    surname1 = Column(String, nullable=True)
    surname2 = Column(String, nullable=True)
    nif = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    terms_accepted = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    sign_in_date = Column(DateTime, nullable=True)

    tasks = relationship("Task", back_populates="owner")


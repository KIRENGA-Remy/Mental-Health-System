# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from ..database import Base
# from datetime import datetime

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     firstName = Column(String, nullable=False)
#     lastName = Column(String, nullable=False)
#     role = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)  







from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  
    
    # Custom to_dict method
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'role': self.role,
            'created_at': self.created_at.isoformat()  # Convert datetime to string format
        }

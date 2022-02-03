from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# https://stackoverflow.com/questions/15175339/sqlalchemy-what-is-declarative-base
Base = declarative_base()


class DBUser(Base):
    __tablename__ = 'users'
    # index = True generates index automatically
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    # password will be hashed
    password = Column(String)
    # to DBArticle, backpopulate user
    items = relationship("DBArticle", back_populates='user')


class DBArticle(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String, nullable=True)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    # to DBUser, backpopulate items
    user = relationship("DBUser", back_populates='items')

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	"""docstring for User object"""

	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))


class Genre(Base):
	"""docstring for Genre object"""

	__tablename__ = 'genre'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name': self.name,
			'id': self.id,
		}


class Book(Base):
	"""docstring for Book object"""

	__tablename__ = 'book'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(8))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	genre_id = Column(Integer, ForeignKey('genre.id'))
	genre = relationship(Genre)

	@property
	def serialize(self):
		# Returns object data in easily serializeable format
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
		}


engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)

# SQLAlchemy-related Imports
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

# MySQL-related Imports
from typing import List, Dict
import mysql.connector


def test_table() -> List[Dict]:
    config = {
        "user": "root",
        "password": "root",
        "host": "db",
        "port": "3306",
        "database": "02db",
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test_table")
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results


class ImageSQL:
    Base = declarative_base()

    class Image(Base):
        __tablename__ = 'Image'
        ID = db.Column(db.INTEGER, primary_key=True)
        name = db.Column(db.VARCHAR(255))
        image_url = db.Column(db.VARCHAR(255))
        caption = db.Column(db.VARCHAR(255))

    def __init__(self, username, password, ip, port, database_name):
        inner_engine = db.create_engine(
            "mysql+pymysql://%s:%s@%s:%s/%s" % (username, password, ip, port, database_name))
        self.Session = sessionmaker(bind=inner_engine)
        self.session = self.Session()

    def get_all(self):
        """
        Returns Image Table in List Form
        """
        result = self.session.query(self.Image.ID, self.Image.name, self.Image.image_url, self.Image.caption).all()
        return result

    def doesImageNameExist(self, name):
        """
        Returns Count of Name
        """
        result = self.session.query(self.Image.name).filter(self.Image.name == name).count()
        return result

    def findById(self, ID):
        """
        Prints Image ID
        """
        result = self.session.query(self.Image.name, self.Image.image_url, self.Image.caption).filter(
            self.Image.ID == ID).one()
        print(result)

    def updateImageURL(self, ID, new_URL):
        try:
            statement = select(self.Image).where(self.Image.ID == ID)
            retrievedImage = self.session.scalars(statement).one()
            retrievedImage.image_url = new_URL
            self.session.commit()
        except Exception as e:
            print(e)

    def delete_image(self, ID):
        statement = self.session.query(self.Image).filter(self.Image.ID == ID).delete()
        self.session.commit()

    def insertNoCaption(self, image_url):
        self.session.add(self.Image(image_url=image_url))
        self.session.commit()

    def insertWithCaption(self, image_url, caption):
        self.session.add(self.Image(image_url=image_url, caption=caption))
        self.session.commit()

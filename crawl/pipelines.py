# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, BLOB)
from scrapy.utils.project import get_project_settings


# class CrawlPipeline:
#     def process_item(self, item, spider):
#         return item

Base=declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)


class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True)
    status=Column(String(3))
    pairid=Column(Integer)
    url=Column(String(255))
    language=Column(String(2))
    text=Column(Text)
    image=Column(BLOB)
    english=Column(Text)
    french=Column(Text)
    spanish=Column(Text)
    bertscoreenglish=Column(Float)
    bertscorefrench=Column(Float)
    bertscorespanish=Column(Float)

class SaveDBPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session=self.Session()
        page=Source()
        page.status=item['status']
        page.pairid=item['pairid']
        page.url=item['url']
        page.image=item['image']
        # page.alturl=item['altURL']
        page.language=item['language']
        page.text=item['text']

        try:
            session.add(page)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()
        print("Item saved to database")
        return item
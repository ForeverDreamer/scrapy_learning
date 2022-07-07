# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from sqlalchemy.orm import Session

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from .models import db_connect, create_table, Quote, Author, Tag
from .items import SynopsisItem, AuthorItem


# class DuplicatesPipeline:
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker.
#         Creates tables.
#         """
#         engine = db_connect()
#         create_table(engine)
#         self.Session = sessionmaker(bind=engine)
#         logging.info("****DuplicatesPipeline: database connected****")
#
#     def process_item(self, item, spider):
#         session = self.Session()
#         quote = session.query(Quote).filter_by(text=item["text"]).first()
#         session.close()
#         if quote:  # the current quote exists
#             raise DropItem("Duplicate item found: %s" % item["quote_content"])
#         else:
#             return item


class SaveQuotesPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        if isinstance(item, SynopsisItem):
            return self.handle_synopsis(item, spider)
        if isinstance(item, AuthorItem):
            return self.handle_author(item, spider)

    def handle_synopsis(self, item, spider):  # needed self added
        # 先执行去重逻辑
        # function to pipe it to database table
        # self.db_handle_synopsis(item)
        return item

    def handle_author(self, item, spider):  # needed self added
        # 先执行去重逻辑
        # function to pipe it to database table
        # self.db_handle_author(item)
        return item

    # def process_item(self, item, spider):
    #     """Save quotes in the database
    #     This method is called for every item pipeline component
    #     """
    #     session = self.Session()
    #     quote = Quote()
    #     author = Author()
    #     tag = Tag()
    #     author.name = item["name"]
    #     author.birthday = item["birthday"]
    #     author.bornlocation = item["bornlocation"]
    #     author.bio = item["bio"]
    #     quote.quote_content = item["text"]
    #
    #     # check whether the author exists
    #     exist_author = session.query(Author).filter_by(name=author.name).first()
    #     if exist_author is not None:  # the current author exists
    #         quote.author = exist_author
    #     else:
    #         quote.author = author
    #
    #     # check whether the current quote has tags or not
    #     if "tags" in item:
    #         for tag_name in item["tags"]:
    #             tag = Tag(name=tag_name)
    #             # check whether the current tag already exists in the database
    #             exist_tag = session.query(Tag).filter_by(name=tag.name).first()
    #             if exist_tag is not None:  # the current tag exists
    #                 tag = exist_tag
    #             quote.tags.append(tag)
    #
    #     try:
    #         session.add(quote)
    #         session.commit()
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()
    #
    #     return item


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class AlicrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item


class TruncateTitle(object):

    def process_item(self, item, spider):
        try:
            item['title'] = item['title'][:10]
        except KeyError:
            print(item)
            raise
        return item


class ProductPipeline(object):
    def process_item(self, item, spider):
        item.save()  # 数据将会自动添加到指定的表

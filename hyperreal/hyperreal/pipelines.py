# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import os
# 行得通但是不推荐的写法，因为每次都要打开文件，关闭文件，效率低
# class HyperrealPipeline:
#     def process_item(self, item, spider): # item就是从Hyper_Drug里面的yield传递过来的数据, spider就是Hyper_DrugSpider
#         with open("./1.csv", mode="a", encoding="utf-8") as f:
#             f.write(f"{item['title']},{item['link']}\n")
#         return item # 返回给引擎，引擎会将数据传递给管道
# 记住，管道默认是关闭的，需要在settings.py中开启


"""
存储数据的方案:
    1. 数据要存储在csv文件中
    2. 数据存储在mysql数据库中
    3. 数据存储在mongodb数据库中
    4. 文件的存储
"""


# 以下是存为CSV文件的例子
# ------------------------------------------------------------------------------------------------------------------------
#     """
#     我们希望的是, 在爬虫开始的时候. 打开这个文件
#     在执行过程中. 不断的往里存储数据
#     在执行完毕时, 关掉这个文件
#     """
# class HyperrealPipeline:
#     def open_spider(self, spider):
#         self.f = open("./1.csv", mode="a", encoding="utf-8")
#         #a的意思是append. 也就是说，如果文件不存在，就创建文件，如果文件存在，就在文件的末尾追加内容.
#         #如何mode ="w", 那么就是覆盖写入，也就是说，如果文件不存在，就创建文件，如果文件存在，就覆盖文件内容.

#     def close_spider(self,  spider):
#         if self.f:
#             self.f.close()

#     def process_item(self, item, spider): # item就是从Hyper_Drug里面的yield传递过来的数据, spider就是Hyper_DrugSpider
#         self.f.write(f"{item['title']},{item['link']}\n")
#         return item
# ------------------------------------------------------------------------------------------------------------------------

# 以下是存为txt文件的例子


class HyperrealPipeline:
    def __init__(self):
        self.file_number = 1
        self.folder_name = "Knajpa pod Przychodnią"

# Ensure folder exists
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def process_item(self, item, spider):
        # Create new file for each item
        filename = os.path.join(self.folder_name, f"{self.file_number}.txt")
        with open(filename, "w") as f:
            f.write(f"{item['title']}\n{item['link']}\n\n{item['file']}\n")
        self.file_number += 1
        return item


# ------------------------------------------------------------------------------------------------------------------------

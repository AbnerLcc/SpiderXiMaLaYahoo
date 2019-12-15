# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy import Request
from scrapy.exceptions import DropItem      # 停止执行任务
from scrapy.pipelines.files import FilesPipeline
from .settings import FILES_STORE



class XiMaPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        music_name=request.meta['item']['music_name']+'.m4a'
        file_name1=request.meta['item']['file_name']
        file_path=os.path.join(FILES_STORE,file_name1,music_name)
        return file_path

        # 图片下载完毕后这个方法会被调用
    def get_media_requests(self, item, info):
        '''
            根据文件的url逐一发送请求
        '''
        path=os.path.join(FILES_STORE,item["file_name"])
        if not os.path.exists(path):
            os.mkdir(path)
        for music_url in item['music_urls']:
            yield Request(url=music_url, meta={'item': item})




    # def item_completed(self, results, item, info):
    #     '''
    #         处理请求结果
    #     '''
    #     file_paths = [x['path'] for ok, x in results if ok]
    #     if not file_paths:
    #         raise DropItem("Item contains no files")
    #
    #     for i in range(0, len(item['music_name'])):
    #         old_name = file_paths[i]
    #         new_name = FILES_STORE +  '\\' + item['music_name'][
    #             i] + '.m4a'
    #
    #         os.rename(old_name, new_name)

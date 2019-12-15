# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import XiMaItem

class QtSpider(scrapy.Spider):
    name = 'xima'
    allowed_domains = ['www.ximalaya.com']

    # 直接通过数字爬取当前页面数据，当然也可以通过查看方式，
    start_urls = ['https://www.ximalaya.com/youshengshu/updates/p1/',]
    def parse(self, response):
        """
            第一次进到评书种类，需要再次进入到具体的某一本书，因此需要再次发送请求
        """

        total_list=response.xpath('//div[@class="content"]/ul/li')
        for item1 in total_list:
            title=item1.xpath('.//div/a[@class="album-title line-1 lg bold _bkf"]/@title').extract_first()
            vol_url_entrance="https://www.ximalaya.com" + item1.xpath('.//div/a[@class="album-title line-1 lg bold _bkf"]/@href').extract_first()
            yield scrapy.Request(url=vol_url_entrance,callback=self.search_vol_url,meta={"file_name":title})

    def search_vol_url(self,response):
        '''
            进到具体页面后，我们发现获取音频的url需要再次发送请求
                https://www.ximalaya.com/revision/play/v1/audio?id=151349437&ptype=1
            通过上面url，可以获取音频url，因此需要再一次发送url，每一个音频的不点是id，因此需要找到id
        '''
        file_name=response.meta["file_name"]
        vol_url_label=response.xpath('//div[@class="sound-list _c2"]/ul/li')
        for label in  vol_url_label:
            a_label=label.xpath('./div[@class="text _c2"]/a')
            title=a_label.xpath('./@title').extract_first()
            vol_href_id=a_label.xpath('./@href').extract_first().rsplit("/",maxsplit=1)[1]
            vol_url="https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1".format(vol_href_id)
            yield scrapy.Request(vol_url,callback=self.vol_callback,meta={"title":title,"file_name":file_name})

    def vol_callback(self,response):
        """
            第二次请求发送的数据响应的数据如下：
           data={
                albumIsSample: false
                canPlay: true
                firstPlayStatus: true
                hasBuy: true
                isBaiduMusic: false
                isPaid: false
                sampleDuration: 0
                src: "https://fdfs.xmcdn.com/group67/M05/9B/45/wKgMd13fN7Wzqj_dAJdu6eqyPd4577.m4a"
                trackId: 232261534
                ret: 200
           }
        """
        file_name = response.meta["file_name"]
        vol_title = response.meta["title"]

        try:
            url=response.text.rsplit('"src":"',maxsplit=1)[1].rsplit('","albumIsSample":',maxsplit=1)[0]

            item=XiMaItem()
            item["file_name"]=file_name
            item["music_name"]=vol_title
            item['music_urls'] = [url, ]
            yield item
        except Exception as e:
            pass

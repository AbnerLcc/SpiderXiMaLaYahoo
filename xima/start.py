#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from scrapy.cmdline import execute


if __name__ == '__main__':
    execute(["scrapy", 'crawl', "xima","--nolog"])  # 注意列表内的字符串就是在终端中的命令拆分
    # execute(["scrapy", 'crawl', "xima"])  # 注意列表内的字符串就是在终端中的命令拆分

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:09:14 2020

@author: smokha
"""


# https://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'scrapy_img'

SPIDER_MODULES = ['scrapy_img.spiders']
NEWSPIDER_MODULE = 'scrapy_img.spiders'


ROBOTSTXT_OBEY= True

ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}

IMAGES_STORE = '/Users/smokha/Projects/DCGAN/web_images'
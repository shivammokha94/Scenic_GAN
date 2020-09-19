#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:16:31 2020

@author: smokha
"""

import scrapy


class item(scrapy.item):
    
    images = scrapy.Field()
    image_urls = scrapy.Field()
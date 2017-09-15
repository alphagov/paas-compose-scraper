# -*- coding: utf-8 -*-
import os

BOT_NAME = 'compose'
SPIDER_MODULES = ['compose.spiders']
NEWSPIDER_MODULE = 'compose.spiders'
ROBOTSTXT_OBEY = True
CHECK_INTERVAL_SECONDS = int(os.environ.get('CHECK_INTERVAL_SECONDS', 600))

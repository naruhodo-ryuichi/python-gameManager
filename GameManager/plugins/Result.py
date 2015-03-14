# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = "naruhodo-ryuichi"


class Result:
    """
    Container for web scraping results
    """
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.link = None
        self.platform = None
        self.score = 0
        self.year = None
        self.genre = None
        self.style = None
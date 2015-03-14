# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
from sqlalchemy import Column, Integer, String, Boolean, Float
from helpers import Base, metadata
from helpers import cleanup

__author__ = "naruhodo-ryuichi"


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    year = Column(Integer)
    saga = Column(String(40))
    played = Column(Boolean)
    downloaded = Column(Boolean)
    notes = Column(String)
    platform = Column(String(40))
    genre = Column(String(40))
    style = Column(String(40))
    score = Column(Float)
    route = Column(String)

    def __init__(self, routegame=None):
        self.saga = ""
        self.played = False
        self.downloaded = False
        self.notes = ""
        self.name = ""
        self.platform = ""
        self.route = routegame
        self.name = self.parse(os.path.basename(self.route))
        self.year = 0
        self.genre = ""
        self.style = ""
        self.score = 0

    @staticmethod
    def parse(title):
        title = cleanup(title, titulo=True)
        title = re.sub("(?i)cd\d", "", title)
        title = re.sub("\d{4} - ", "", title)
        title = re.sub(" - ", ": ", title)
        title = re.sub("\(.*?\)", "", title)
        title = re.sub("\[.*?\]", "", title)
        return title

    def __repr__(self):
        return "%s (%s) %s %s %s%% %s" % (self.name, self.year, self.genre, self.style, self.score, self.platform)

metadata.create_all()
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from helpers import session
from DB import Game


def add(ggame):
    success = False
    try:
        session.query(Game).filter(Game.name == ggame.name).one()
    except NoResultFound:
        j = Game()
        j.route = ggame.route
        j.saga = ggame.saga
        j.played = ggame.played
        j.downloaded = ggame.downloaded
        j.notes = ggame.notes
        j.name = ggame.name
        j.platform = ggame.platform
        j.year = ggame.year
        j.genre = ggame.genre
        j.style = ggame.style
        j.score = ggame.score
        session.add(j)
        session.commit()
        success = True
    return success


def modify(id, ggame):
    j = session.query(Game).get(id)
    j.route = ggame.route
    j.saga = ggame.saga
    j.played = ggame.played
    j.downloaded = ggame.downloaded
    j.notes = ggame.notes
    j.name = ggame.name
    j.platform = ggame.platform
    j.year = ggame.year
    j.genre = ggame.genre
    j.style = ggame.style
    j.score = ggame.score
    session.add(j)
    session.commit()


def delete(id):
    game = session.query(Game).get(id)
    session.delete(game)
    session.commit()


def search(terms, word=None, strict_term=False):
    result = Game()
    if terms == "all":
         result = session.query(Game).order_by(Game.score.desc()).all()
    elif terms == "id":
        result = session.query(Game).get(word)
    elif terms == "name":
        if strict_term:
            result = session.query(Game).filter(func.lower(Game.name) == word.lower()).order_by(Game.score.desc()).all()
        else:
            result = session.query(Game).filter(func.lower(Game.name).contains('%s' % word.lower())).order_by(Game.score.desc()).all()
    elif terms == "genre":
        result = session.query(Game).filter(Game.genre.contains('%s' % word)).order_by(
            Game.score.desc()).all()
    return result


def searchnew(mypath):
    # look for new files by platform folder
    platforms = ['dreamcast', 'gba', 'gc', 'n64', 'nds', 'pc', 'ps2', 'psp', 'psx', 'saturn', 'snes']
    newfiles = set()
    games = session.query(Game).all()
    routes = [os.path.normpath(j.route) for j in games]
    names = [j.name for j in games]
    for platform in platforms:
        routegames = os.path.join(mypath, platform)
        results = os.listdir(routegames)
        for result in results:
            if result not in newfiles and result not in names:
                newfiles.add(result)
    return newfiles

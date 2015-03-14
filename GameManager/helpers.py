# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import StringIO
import logging
import re
import socket
import urllib2
from xml import etree

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

__author__ = "naruhodo-ryuichi"

db = create_engine("mydb.sqlite")
Base = declarative_base(db)
metadata = Base.metadata
Session = scoped_session(sessionmaker(bind=db))
session = Session()


def cleanup(name, title=False):
    """
    Tries to cleanup names removing dots, multiple spaces, underscores, etc
    :param name: text to clean
    :param title: Capitalize words
    :return: Hopefully clean name
    """
    from collections import Counter
    cnt = Counter()
    for s in name:
        cnt[s] += 1
    garbage = "_*+\\/|=-<>."
    for b in garbage:
        for s, n in cnt.most_common(len(name)*20/100):
            if s == b:
                name = name.replace(b, " ")
    if title:
        words = []
        for x in name.split():
            if re.match("(?i)^[ixv]+\.?$", x):
                words.append(x.upper())
            else:
                words.append(x.title())
        name = " ".join(words)
    else:
        name = " ".join(name.split())
    name.strip()
    return name


def pagedownload(url):
    data = None
    try:
        socket.setdefaulttimeout(10)
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101")
        data = urllib2.urlopen(request).read()
    except urllib2.HTTPError as inst:
        logging.error("Error : %s - %s" % (url, inst))
    except urllib2.URLError as inst:
        logging.error("TimeOut : %s" % inst)
    except socket.timeout as inst:
        logging.error("TimeOut : %s" % inst)
    except socket.error as inst:
        logging.error("Socket Error : %s" % inst)
    finally:
        return data


def xmldownload(url):
    mytree = None
    try:
        data = pagedownload(url)
        mytree = etree.parse(StringIO(data), etree.HTMLParser())
    except TypeError:
        logging.error("No data received")
    finally:
        return mytree
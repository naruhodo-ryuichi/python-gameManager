# -*- coding: utf-8 -*-

import logging
import re
import urllib
from helpers import xmldownload
from plugins import Result


def busca(name):
    lres = list()
    base_url = "http://www.gamerankings.com"
    url = "%s/browse.html?site=&cat=0&year=0&numrev=3&sort=0&letter=&search=%s" % (base_url, urllib.quote_plus(name.encode("utf-8")))
    logging.info("Gamerankings: searching %s" % url)
    results = xmldownload(url).xpath(".//div[@id='main_col']/div[@class='pod']/div[@class='body']/table/tr")

    for r in results:
        res = Result()
        sys = r.xpath("./td[2]/text()")
        res.platform = sys[0] if len(sys) > 0 else None
        tit = r.xpath("./td[3]/a/text()")
        res.name = tit[0] if len(tit) > 0 else None
        link = r.xpath("./td[3]/a/@href")
        res.link = base_url + link[0] if len(link) > 0 else None
        year = r.xpath("./td[3]/text()")
        ryear = re.findall(".*(\d{4}).*", year[0]) if len(year) > 0 else None
        res.year = ryear[0] if len(ryear) > 0 else 0
        scor = r.xpath("./td[4]/span/b/text()")
        rscor = re.findall("(\d?\d\d\.\d\d)%", scor[0]) if len(scor) > 0 else None
        res.score = rscor[0] if len(rscor) > 0 else 0
        lres.append(res)
    return lres


def searchgenre(res):
    game = xmldownload(res.link)
    data = game.xpath(".//div[@class='crumbs']")
    if len(data) > 0:
        data = data[0]
        s = data.xpath("./a[1]/text()")
        g = data.xpath("./a[2]/text()")
        e = data.xpath("./a[3]/text()")
        n = game.xpath(".//h1/text()")
        p = game.xpath(".//div[@class='pod']/div[@class='body']/table/tbody/tr/td/span/b/text()")
        res.platform = s[0] if len(s) > 0 and not res.platform else res.platform
        res.genre = g[0] if len(g) > 0 and not res.genre else res.genre
        res.style = e[0] if len(e) > 0 and not res.style else res.style
        res.name = n[0] if len(n) > 0 and not res.name else res.name
        res.score = p[0] if len(p) > 0 and not res.score else res.score
    return res

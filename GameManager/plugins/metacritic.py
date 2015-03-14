#!/usr/bin/python
import logging
import re
from bs4 import BeautifulSoup
from helpers import pagedownload

TYPES = ['all', 'movie', 'game', 'album', 'tv', 'person', 'video', 'company']


class MetacriticInfo:
    def __init__(self):
        self.id = None
        self.title = None
        self.type = None
        self.link = None
        self.boxart = None
        self.system = None
        self.publisher = None
        self.publisher_link = None
        self.release_date = None
        self.metascore = None
        self.metascore_count = None
        self.metascore_desc = None
        self.user_score = None
        self.user_count = None
        self.user_score_desc = None
        self.summary = None
        self.esrb = None
        self.official_site = None
        self.developer = None
        self.genres = None
        self.num_players = None
        self.esrb_reason = None
        self.sound = None
        self.connectivity = None
        self.resolution = None
        self.num_online = None
        self.customization = None


def search(query, type="all"):
    url = get_search_url(query, type)
    logging.debug("metacritic: buscando %s" % url)
    html = pagedownload(url)
    if not html:
        return None
    soup = BeautifulSoup(html)
    i = 0
    page = 0
    allresults = []
    results = soup.findAll("li", "result")
    from plugins import Result
    for result in results:
        res = Result()
        result_type = result.find("div", "result_type")
        if result_type:
            strong = result_type.find("strong")
            if strong:
                res.type = strong.text.strip()
            span = result.find("span", "platform")
            if span:
                res.platform = span.text.strip()
        product_title = result.find("h3", "product_title")
        if product_title:
            a = product_title.find("a")
            if a:
                res.link = "http://www.metacritic.com" + a["href"]
                res.id = a["href"][1:].replace("/", "_")
                res.name = a.text.strip()
        metascore = result.find("span", "metascore_w")
        if metascore:
            res.score = metascore.text.strip()
        ryear = re.findall(".*(\d{4}).*", get_li_span_data(result, "release_date"))
        if ryear:
            res.year = int(ryear[0])
        res.esrb = get_li_span_data(result, "maturity_rating")
        res.publisher = get_li_span_data(result, "publisher")
        res.index = i
        res.page = page
        allresults.append(res)
        i += 1
    return allresults


def get_info(id):
    url = get_details_url(id)
    html = pagedownload(url)
    if not html:
        return None
    soup = BeautifulSoup(html)
    prod = MetacriticInfo()
    prod.id = id
    og_type = soup.find("meta", attrs={"name":"og:type"})
    if og_type:
        prod.type = og_type["content"].strip()
    og_image = soup.find("meta", attrs={"name":"og:image"})
    if og_image:
        prod.boxart = og_image["content"].strip()
    product_title = soup.find("div", "product_title")
    if product_title:
        a = product_title.find("a")
        if a:
            prod.link = "http://www.metacritic.com" + a["href"]
            prod.title = a.text.strip()
    platform = soup.find("span", "platform")
    if platform:
        a = platform.find("a")
        if a:
            prod.system = a.text.strip()
    publisher = soup.find("li", "publisher")
    if publisher:
        a = publisher.find("a")
        if a:
            prod.publisher = a.text.strip()
            prod.publisher_link = "http://www.metacritic.com" + a["href"]
    prod.release_date = get_li_span_data(soup, "release_data")
    metascore = soup.find("div", "feature_metascore")
    if metascore:
        score_value = metascore.find("span", "score_value")
        if score_value:
            prod.metascore = score_value.text.strip()
        count = metascore.find("span", "count")
        if count:
            a = count.find("a")
            if a:
                span = a.find("span")
                if span:
                    prod.metascore_count = span.text.strip()
        desc = metascore.find("span", "desc")
        if desc:
            prod.metascore_desc = desc.text.strip()
    avguserscore = soup.find("div", "feature_userscore")
    if avguserscore:
        score_value = avguserscore.find("span", "score_value")
        if score_value:
            prod.user_score = score_value.text.strip()
        count = avguserscore.find("span", "count")
        if count:
            a = count.find("a")
            if a:
                prod.user_count = a.text[:a.text.find(" ")]
        desc = avguserscore.find("span", "desc")
        if desc:
            prod.user_score_desc = desc.text.strip()
    product_summary = soup.find("div", "product_summary")
    if product_summary:
        data = product_summary.find("span", "data")
        if data:
            prod.summary = data.text.strip()
    product_details = soup.findAll("div", "product_details")
    for pd in product_details:
        table = pd.find("table")
        if table:
            trs = table.findAll("tr")
            for tr in trs:
                th = tr.find("th")
                td = tr.find("td")
                th_val = th.text.replace(":", "").strip()
                td_val = td.text.strip()
                if th_val == "Rating":
                    prod.esrb = td_val
                elif th_val == "Official Site":
                    prod.official_site = td_val
                elif th_val == "Developer":
                    prod.developer = td_val
                elif th_val == "Genre(s)":
                    prod.genres = td_val
                elif th_val == "Number of Players":
                    prod.num_players = td_val
                elif th_val == "ESRB Descriptors":
                    prod.esrb_reason = td_val
                elif th_val == "Sound":
                    prod.sound = td_val
                elif th_val == "Connectivity":
                    prod.connectivity = td_val
                elif th_val == "Resolution":
                    prod.resolution = td_val
                elif th_val == "Number of Online Players":
                    prod.num_online = td_val
                elif th_val == "Customization":
                    prod.customization = td_val
    return prod


def get_li_span_data(node, data_name):
    li = node.find("li", data_name)
    if li:
        data = li.find("span", "data")
        if data:
            return data.text.strip()
    return None


def get_search_url(query, type="all"):
    return "http://www.metacritic.com/search/%s/%s/results?sort=relevancy" % (type, query.replace(":", "").replace("-", "").replace("_", "").replace(" ", "+"))


def get_details_url(id):
    return "http://www.metacritic.com/%s/details" % id.replace("_", "/")

#! /user/bin/env python3

import requests
from bs4 import BeautifulSoup
import re


def gethtmltext(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsehtml(html):
    if len(html) < 10:
        return
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    lst = []
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue
    return lst

def parsestock(stock):
    url = "https://gupiao.baidu.com/stock/" + stock + ".html"
    html = gethtmltext(url)
    soup = BeautifulSoup(html, "html.parser")
    stockInfo = soup.find('div', attrs={'class': 'stock-bets'})
    infodict = {}
    try:
        name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
        infodict.update({'stock name': name.text.split()[0]})
        infodict['id'] = stock
        keylst = stockInfo.find_all('dt')
        valuelst = stockInfo.find_all('dd')
        for i in range(len(keylst)):
            key = keylst[i].text
            val = valuelst[i].text
            infodict[key] = val
        return infodict
    except:
        return None


if __name__ == "__main__":
    lst = parsehtml(gethtmltext("http://quote.eastmoney.com/stocklist.html"))
    for stock in lst:
        stockinfo = parsestock(stock)
        if stockinfo:
            with open("/Users/emc/Documents/python3.git/records", 'a', encoding='utf-8') as f:
                f.write(str(stockinfo) + "\\n")


from numpy.testing._private.utils import tempdir
import requests
import re

import pandas as pd
def get_html(url):

    # ua = UserAgent()

    headers = {'User-Agent':"FireFox"}
    response = requests.get(url)
    if response.status_code ==200:
        response.encoding='utf-8'

        return response.text
    else:
        return
def GDP_people_info(html):
    pat ='<p>(\d+.*?)</p>'
    #处凰提欣的当游，以[(城市，GDP，人.....]形式保存
    infos = re.findall(pat,html,re.S)
    datas=[]
    for info in infos:

        pat1=r".*?(\d+)万?）"
        people = re.findall(pat1,info)
        # GDP
        pat2=r'(\d+)亿元，'
        GDP=re.findall(pat2,info)
        # 城市
        pat3=r"\d+\.(.*?)\d+亿元，"
        city=re.findall(pat3,info)
        city = city[0].split("（")[0]

        try:
            datas.append((city,GDP[0],people[0]))
        except:
            print(city, GDP, people)
            pass
        
    return datas
def run():
    url ="http://caifuhao.eastmoney.com/news/20190201115604564011000"
    html=get_html(url)
    data = GDP_people_info(html)
    pd.DataFrame(data).to_csv("GDP_100.csv")
    return pd.DataFrame(data)
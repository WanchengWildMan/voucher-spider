# -*- coding:UTF-8 -*-
from sklearn.cluster import KMeans
from urllib.request import urlopen, quote
import time
import getGDP
import getGDP_peo
import requests
from lxml import etree
import pandas as pd
import numpy as np
import os
from numpy import *
import re
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
url_back = "news/xiaofeiquan/"
url_root = "http://www.bendibao.com/"
url_index = "http://www.bendibao.com/index.htm"
xpath_cityurl = '//*[@id="city-list"]/div/div/div[3]/dl[{}]/dd/a'
xpath_province = '//*[@id="city-list"]/div/div/div[3]/dl/dt'
r = requests.get(url=url_index, headers=headers)
r.encoding = r.apparent_encoding
html_index = etree.HTML(r.text)

df = pd.DataFrame(columns=["url", "城市", "省份", "领取方式",
                           "发放时间", "发放金额", "领取数量", "领取规则"])
provinces = list(map(lambda x: x.text, html_index.xpath(xpath_province)))
citys_info = ndarray((1, 3))
for i, pro in enumerate(provinces):
    print(pro, i)
    citys_ = list(
        map(lambda x: x.text, html_index.xpath(xpath_cityurl.format(i + 1))))
    citys_a = html_index.xpath(xpath_cityurl.format(i + 1))
    citys_url = html_index.xpath((xpath_cityurl + "/@href").format(i + 1))

    citys_info = np.concatenate(
        [citys_info, array([citys_url, citys_, [pro] * len(citys_)]).T])

citys_info = citys_info[1:, :]
# %%
df_citys_info = pd.DataFrame(citys_info, columns=df.columns[:3])
df_quan_info = pd.DataFrame(columns=df.columns[3:])
# df_gdp_1 = pd.read_excel("GDP_100.xlsx")
df_gdp_1 = getGDP_peo.run()

# df_gdp_2 = pd.read_csv("上半年中国城市GDP排名.csv", encoding="gbk").iloc[:, 1:]
df_gdp_2 = getGDP.run()
df_gdp_1 = df_gdp_1.rename(columns={0: "城市", 1: "2019年gdp", 2: "人口"})
df_gdp = pd.merge(df_gdp_1, df_gdp_2, on='城市', how="outer")


# 多次运行反爬

df_gdp["lon"] = nan
df_gdp["lat"] = nan

while sum((isnan(df_gdp["lon"])) | (isnan(df_gdp["lon"]) | isnan(df_gdp["lon"]))) > 0:
    lon = []
    lat = []

    def getlonla(address):

        #         response = requests.get('http://api.map.baidu.com/geocoder?address={}&output=json&key=dAmhROmqNEtVvKar7uetVbGCn5d5xZeI'.format(quote(address)))
        response = requests.get("http://api.map.baidu.com/geocoding/v3/?address=" + quote(address) +
                                "&output=json" +
                                "&ak=dAmhROmqNEtVvKar7uetVbGCn5d5xZeI")
        response.encoding = response.apparent_encoding
        try:
            answer = response.json()
            print(response.text)
            print(address)
            print(response.url)
            if int(answer["status"]) == 2:
                lon.append(0)
                lat.append(0)
            else:
                lon.append(float(answer['result']['location']['lng']))
                lat.append(float(answer['result']['location']['lat']))

        except:
            lon.append(NaN)
            lat.append(NaN)
            return

        time.sleep(0)

    df_gdp.loc[(isnan(df_gdp["lon"])) | (isnan(df_gdp["lon"])
                                         | isnan(df_gdp["lon"])), "城市"].apply(getlonla)
    # print(len(lon), len(lat))
    df_gdp.loc[isnan(df_gdp["lon"]), "lon"] = lon
    df_gdp.loc[isnan(df_gdp["lat"]), "lat"] = lat

# %%
for CITY_INDEX in range(0, shape(df_citys_info)[0], 10):
    for i, row in df_citys_info.iloc[CITY_INDEX:min(CITY_INDEX+10, shape(df_citys_info)[0]), :].iterrows():
        # print(i, row["城市"])
        try:
            r = requests.get(row["url"] + url_back, headers=headers)
        except:
            continue
        r.encoding = r.apparent_encoding
        if r.status_code != 200:
            continue
        xpath_quan_info = "/html/body/div[3]/div[2]/div[1]/ul/li[1]/div[2]/div/span[2]"
        html = etree.HTML(r.text)
        l = list(map(lambda x: x.text, html.xpath(xpath_quan_info)))
        print(l)
        if len(l) == 0:
            continue

        df_quan_info = df_quan_info.append(pd.DataFrame([concatenate([row.values, l])], columns=df.columns),
                                           ignore_index=True)

    df_quan_info_bak = df_quan_info

    # %%

    df_quan_info.to_csv("消费券信息_gbk.csv", index=False)
    df_quan_info_tidy = df_quan_info.copy()
    df_quan_info_tidy.columns

    pat_date = re.compile('(?P<month>\d+)月(?P<day>\d*)日')
    pat_date_sted = re.compile(
        '(?P<month_st>\d*)月(?P<day_st>\d*)日[^\n]*(?P<month_end>\d*)月(?P<day_end>\d*)日')
    pat_money = re.compile('(?P<money>\d*(万|亿))[元]*')
    pat_num = re.compile("(?P<num>\d*)[万]*(张|个)")
    cols_process = ["发放时间", "发放时间", "发放金额", "领取数量"]

    # %%

    df_tmp = df_quan_info_tidy.copy()
    df_quan_info_tidy_bak = df_quan_info_tidy.copy()
    for pat, col in zip([pat_date, pat_date_sted, pat_money, pat_num], cols_process):
        new_cols = []
        l = df_quan_info.apply(
            lambda row, pat, col: pat.search(row[col]).groupdict() if None != row[col] and None != pat.search(
                row[col]) else {}, axis=1, args=[pat, col]).to_list()
        #     print(l)
        df_tmp = (pd.concat([df_tmp, pd.DataFrame(l)], axis=1))

    # %%
    df_tmp.fillna(value=0, inplace=True)
    # pat_date.search(df_quan_info["发放时间"].iloc[1])
    df_quan_info_tidy = df_tmp
    df_quan_info_tidy.to_csv("df_quan_info_tidy.csv", index=False)
    df_quan_info_tidy = pd.read_csv("df_quan_info_tidy.csv")

    # df_quan_info_tidy = pd.read_csv("消费券信息_日期.csv")
    df_quan_info_tidy["money"] = df_quan_info_tidy["money"].apply(
        lambda x: NaN if str(x).isspace() else x)

    # %%

    def repair(x):
        if len(x) == 0:
            return x
        if len(x) == 1:
            x = "1" + x
        if x[-1] == '亿':
            if int(x[:-1]) > 30:
                x = "1." + x
        return x

    # %%

    # df_quan_info_tidy["money"].fillna(method='pad', inplace=True)
    df_quan_info_tidy["money"] = df_quan_info_tidy["money"].apply(repair)
    df_quan_info_tidy["money_digit"] = df_quan_info_tidy["money"].apply(
        lambda x: float(x[:-1]) * 10000 if x[-1] == "万" else float(x[:-1]) * 1e8)

    # df_quan_info_tidy = pd.read_excel("消费券信息_处理金额缺失.xlsx")
    df_quan_info_tidy["是否为摇号"] = False
    for col in df_quan_info_tidy.columns[:5]:
        df_quan_info_tidy["是否为摇号"] = df_quan_info_tidy["是否为摇号"] | df_quan_info_tidy[col].astype('str').str.contains("摇号") | \
            df_quan_info_tidy[col].astype('str').str.contains(
                "抽") | df_quan_info_tidy[col].astype('str').str.contains("随机")
    # df_quan_info_tidy[col].astype('str').str.contains("摇号")

    # %%

    df_quan_info_tidy["是否为抢券"] = False
    for col in df_quan_info_tidy.columns[:5]:
        df_quan_info_tidy["是否为抢券"] = df_quan_info_tidy["是否为抢券"] | df_quan_info_tidy[col].astype('str').str.contains(
            "抢")
    # df_quan_info_tidy[col].astype('str').str.contains("摇号")

    df_quan_info_tidy["发放方式0领取1摇号2抢券"] = df_quan_info_tidy["是否为抢券"] * \
        2 + df_quan_info_tidy["是否为摇号"]
    df_quan_allinfo = df_quan_info_tidy

    # %%

    df_all_info = pd.merge(df_gdp, df_quan_allinfo, on="城市", how="right")
    df_all_info[isnan(df_all_info["发放方式0领取1摇号2抢券"])]
    # 赋值部分

    # %%
    df_all_info.loc[:, "2019年gdp"].fillna(value=0, inplace=True)
    kmeans = KMeans(n_clusters=5).fit(df_all_info[["2019年gdp"]])

    # %%

    df_all_info[["城市经济分级_2019年gdp"]] = (kmeans.labels_)
    df_all_info["城市经济分级_2019年gdp"] = df_all_info["城市经济分级_2019年gdp"].map(
        dict(zip(range(5), floor(6 - pd.Series(kmeans.cluster_centers_.squeeze()).rank()))))

    df_imp = df_all_info[
        ["城市", "省份", "2019年gdp", "城市经济分级_2019年gdp", "人口", "lon", "lat"] + ["money_digit", "发放方式0领取1摇号2抢券", "领取方式", "发放时间", "发放金额", "领取数量", "领取规则", "url"]].fillna(value="")
    df_imp = df_imp.rename(columns={"城市": "city", "省份": "province", "2019年gdp": "gdp19", "城市经济分级_2019年gdp": "gdpStage19", "人口": "peo", "发放方式0领取1摇号2抢券": "giveOutMethod",
                                    "领取方式": "methodDescribe", "发放时间": "giveTimeDescribe", "发放金额": "moneyDescribe", "领取数量": "numDescribe", "领取规则": "ruleDescribe", "url": "url", "money_digit": "moneyDigit"})
    df_imp["giveOutMethod"] = df_imp["giveOutMethod"].map(
        {0: "领取", 1: "摇号", 2: "抢券"})
    df_imp.to_csv("df_important.csv", index=False)
    conn = pymysql.connect(
        user="test",
        port=3306,
        passwd="test",
        db="test",
        host="127.0.0.1",
        charset='utf8'
    )
    cursor = conn.cursor()
    insert_sql = "INSERT INTO `voucher` VALUES( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')"
    create_table_sql = open("voucher.sql").read()
    update_sql = "UPDATE `voucher` SET `gdp19` = {},`province`='{}', `gdpStage19` = '{}', `peo` = '{}', `lon` = '{}', `lat` = '{}', `moneyDigit` = '{}', `giveOutMethod` = '{}', `methodDescribe` = '{}', `giveTimeDescribe` = '{}', `moneyDescribe` = '{}', `numDescribe` = '{}', `ruleDescribe` = '{}', `url` = '{}' WHERE `city` = '{}'"
    cursor.execute(create_table_sql)

    def ins(row):
        cursor = conn.cursor()
        l = list(row.values)
        print(insert_sql.format(*l))
        try:
            cursor.execute(insert_sql.format(*l))
            conn.commit()
        except:
            print("插入失败:", l)
            try:
                print("尝试更新:", l)
                cursor.execute(update_sql.format(*l))
                conn.commit()
            except:
                print("插入失败:", l)
                conn.rollback()
    df_imp.apply(ins, axis=1)

    cursor.close()
    # 关闭数据库连接
    conn.close()

# %%

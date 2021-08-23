import requests
from lxml import etree
import pandas as pd
def run():
    #爬取2019年上半年中国前10名城市
    #伪装爬虫
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
    url =  "http://www.860816.com/aricle.asp?id=1785"
    r = requests.get(url,headers = headers) #发送get请求
    r.encoding=r.apparent_encoding
    #构建一个xpath解析对象
    html = etree.HTML(r.text) #利用etree.HTML()将html字符串转化为element对象,element对象是xpath语法的使用对象，element对象可由html字符串转化
    table = html.xpath("//table[@class='ke-zeroborder']/tbody")
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    lt=[]
    for td in table:

        number = td.xpath(".//td[@class='et2'][1]/text()")[1:]
        name = td.xpath(".//td[@class='et2'][2]/text()")[1:]
        s2019GDP = td.xpath(".//td[@class='et2'][3]/text()")[1:] #2019上半年GDP（亿元）
        s2018GDP = td.xpath(".//td[@class='et2'][4]/text()")[1:]
        increase1_3 = td.xpath(".//td[@class='et2'][5]/text()")[1:]
        increase2_10 = td.xpath(".//td[@class='et3']/text()")[0:]
        print(name)
        for i in range(len(number)):
            a.append(number[i].strip())#用append生成多维数组
            b.append(name[i].strip())
            c.append(s2019GDP[i].strip())
            d.append(s2018GDP[i].strip())
        for i in range(len(increase1_3)):
            e.append(increase1_3[i].strip())
        for i in range(len(increase2_10)):
            e.append(increase2_10[i].strip())

    e[2],e[1] = e[1],e[2]

    lt=[]
    for i in range(len(a)):
        lt.append([a[i],b[i],c[i],d[i],e[i]])


    df=pd.DataFrame(lt,columns=["排名","城市","2019上半年GDP","2018上半年GDP","名义增速"])
    print(df)
    df.to_csv('上半年中国城市GDP排名.csv',encoding = 'gbk') #保存文件，数据持久化
    return df

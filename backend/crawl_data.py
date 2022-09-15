import re
import time
import pandas as pd
import requests
from lxml import etree
from selenium.webdriver.common.by import By
from selenium import webdriver
import os

test_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_4.shtml'
first_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
part_url = 'http://www.nhc.gov.cn'
first_kid_url = 'http://www.nhc.gov.cn/xcs/yqtb/202209/78ea88c5c23e41c391376ee9b103cfec.shtml'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}

filename = 'web_location.txt'
province_list = [
    '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽',
    '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
    '四川', '贵州', '云南', '陕西', '甘肃', '青海', '北京', '天津',
    '上海', '重庆', '内蒙古', '广西', '西藏', '宁夏', '新疆'
]

#获取每一天疫情报告的网址存在web_location中
def get_child_page():
    for i in range(1, 42):
        #当第一页时，为first_url
        if (i == 1):
            re_url = first_url;
        else:
            next_url = '/xcs/yqtb' + f'/list_gzbd_{i}'  #:
            re_url = part_url + next_url + '.shtml'
        res = requests.get(url=re_url, headers=headers)
        res_text = res.text
        tree = etree.HTML(res_text)
        location_part_url = tree.xpath('/html/body/div[3]/div[2]/ul//li/a/@href')
        while (len(location_part_url) == 0):  # 没有得到正常网页,重复请求
            res = requests.get(url=re_url, headers=headers)
            res_text = res.text
            tree = etree.HTML(res_text)
            location_part_url = tree.xpath('/html/body/div[3]/div[2]/ul//li/a/@href')

        with open(filename, 'a') as ob:
            for j in location_part_url:
                print(j + 'was Crawled!')
                ob.write(part_url + j + '\n')
        print(f'Get Page {i} !\n')



def get_detailed():
    raw_path = r'D:\软工\软工个人作业\个人作业1\修订版本\data_of_html'

    dir_list = os.listdir(raw_path)

    dir_list.sort(reverse=True)  # 获取有序的文件
    for li in dir_list:
        filePath = r'D:\软工\软工个人作业\个人作业1\修订版本\raw2' + '\\' + li  # 所存txt绝对路径
        with open(filePath, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            news = ''.join(contents)  # 生成 可以用来匹配的文本

            all_dict = {}
            gat_dict = {}
            sfbt_dict = {}
            sfwzz_dict = {}
            '''我国31个省（自治区、直辖市）和新疆生产建设兵团（不包括港澳台）'''
            if(re.search('截至(.*?)24时', news) == None):
                all_dict['day'] = ''
            else:
                all_dict['day'] = re.search('截至(.*?)24时', news).group(1)  # group(1)代表括号里的内容
            # 新增确诊
            if(re.search('新增确诊病例.*?本土病例(\d+)例', news) == None):
                all_dict['confirm_add'] = ''
            else:
                all_dict['confirm_add'] = re.search('新增确诊病例.*?本土病例(\d+)例', news).group(1)
            # 新增无症状
            if(re.search('新增无症状感染者(\d+)例，', news) == None):
                all_dict['wuzhengzhuang'] = None
            else:
                all_dict['wuzhengzhuang'] = re.search('新增无症状感染者(\d+)例，', news).group(1)
            print(all_dict)

            '''港澳台'''
            # 香港累计确诊
            if(re.search('香港特别行政区(\d+)例', news) == None):
                gat_dict['香港'] = ''
            else:
                gat_dict['香港'] = re.search('香港特别行政区(\d+)例', news).group(1)

            # 澳门累计确诊
            if(re.search('澳门特别行政区(\d+)例', news) == None):
                gat_dict['澳门'] = ''
            else:
                gat_dict['澳门'] = re.search('澳门特别行政区(\d+)例', news).group(1)

            # 台湾累计确诊
            if(re.search('台湾地区(\d+)例', news) == None):
                gat_dict['台湾'] = ''
            else:
                gat_dict['台湾'] = re.search('台湾地区(\d+)例', news).group(1)

            # for k,v in gat_dict.items():
            #     print(k,v)
            print(gat_dict)
            # with open()
            for i in province_list:
                res = re.search('新增确诊病例.*?本土病例.*?' + i + '(\d+)例', news)
                if (res == None):
                    sfbt_dict[i] = '0'
                else:
                    sfbt_dict[i] = res.group(1)
                # print(res)
            print(sfbt_dict)

            # 各省份新增无症状病例
            for i in province_list:
                res = re.search('新增无症状感染者.*?本土.*?' + i + '(\d+)例', news)
                if (res == None):
                    sfwzz_dict[i] = '0'
                else:
                    sfwzz_dict[i] = res.group(1)
            print(sfwzz_dict)
            write_in_each_excel(all_dict,sfbt_dict,sfwzz_dict,gat_dict)



def write_in_each_excel(all_dict,sfbt_dict,sfwzz_dict,gat_dict):

# sheet1 用来存时间、大陆新增病例以及大陆新增无症状

    # 提取字典中的两列值key是键值，value是cont【key】对应的值
    column1 = list(all_dict.keys())
    column2 = list(all_dict.values())

    result_excel1 = pd.DataFrame()
    result_excel1["大陆"] = column1
    result_excel1["大陆数据"] = column2

    y = all_dict['day']
    result_excel1.to_excel(y + '.xlsx', sheet_name='Sheet1', index=False)

# sheet2 用来存31个省份的新增确诊和无症状
    column1 = list(sfbt_dict.keys())
    column2 = list(sfbt_dict.values())
    column3 = list(sfwzz_dict.values())

    # 利用pandas模块先建立DateFrame类型，然后将两个上面的list存进去
    result_excel2 = pd.DataFrame()
    result_excel2["省份"] = column1
    result_excel2["新增确诊"] = column2
    result_excel2["新增无症状"] = column3

    # 写入excel
    # result_excel2.to_excel(y + '.xlsx',sheet_name='Sheet2', index=False)
    with pd.ExcelWriter(y + '.xlsx', mode='a') as writer:
        result_excel2.to_excel(writer, sheet_name='Sheet2', index=False)

# sheet3 用于存港澳台的累计确诊人数
    column1 = list(gat_dict.keys())
    column2 = list(gat_dict.values())
    result_excel3 = pd.DataFrame()
    result_excel3["港澳台"] = column1
    result_excel3["港澳台累计确诊"] = column2

    # 写入excel
    # result_excel3.to_excel(y + '.xlsx', sheet_name='Sheet3', index=False)

    with pd.ExcelWriter(y + '.xlsx', mode='a') as writer:
        result_excel3.to_excel(writer, sheet_name='Sheet3', index=False)

if __name__ == '__main__':
    #get_child_page() # 获取web_location.txt
    get_detailed()  # 解析数据
    #get_Raw_data_by_selenium()

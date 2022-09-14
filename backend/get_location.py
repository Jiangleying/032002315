url2= 'http://www.nhc.gov.cn/xcs/yqtb/202209/cb9e0c28d4b2467fac0ca2871bbfd95b.shtml'
first_kid = 'http://www.nhc.gov.cn/xcs/yqtb/202209/78ea88c5c23e41c391376ee9b103cfec.shtml' # 第一个子网页

from selenium import webdriver
from lxml import etree
from time import sleep

from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True  # 设置不弹出浏览器

filename = './raw2/' # .html

i = 976
with open('web_location.txt', 'r') as file_obj:
    for line in file_obj: # 访问每个子链接

        driver = webdriver.Firefox(options=options)  #
        driver.get(line)
        page_text = driver.page_source
        tree = etree.HTML(page_text)
        while ('疫情通报' not in page_text): # 是否获得正常页面
            driver.get(line)
            page_text = driver.page_source
            tree = etree.HTML(page_text)
            sleep(2)
        driver.quit()
        tits = tree.xpath('//div[@class="tit"]/text()')
        paras = tree.xpath('//div[@class="con"]//text()')

        for tit in tits:
            fname = filename + str(i) + tit + '.html'
            with open(fname, 'a', encoding='utf-8') as f:
                f.write(tit)
                for para in paras:
                    f.write(para)
            print(str(i)+tit+'.html is done! ')
            i = i-1
print(type(page_text))


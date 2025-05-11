from selenium import webdriver
from selenium.webdriver.chrome.service import Service  
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
from lxml import html

def db_hanime_info(NY,id,LF_NAME_JP, LF_NAME_CN, LF_ZZGS, LF_FSRQ, LF_NR, LF_IMG, LF_TAG):
    # 创建数据库连接
    conn = sqlite3.connect('hanime1.db')
    cursor = conn.cursor()
    # 创建表
    cursor.execute('''CREATE TABLE IF NOT EXISTS '{}'
                    (ID INT PRIMARY KEY NOT NULL, -- 里番ID
                    name_jp TEXT COMMENT '日文名称',
                    name_cn TEXT COMMENT '中文名称',
                    company TEXT COMMENT '制作公司',
                    release_date TEXT COMMENT '发行日期',
                    content TEXT COMMENT '内容',
                    img_url TEXT COMMENT '图片URL',
                    tags TEXT COMMENT '标签',
                    sfxz TEXT COMMENT '是否下载')'''.format(str(NY)))

    for i in range(len(LF_NAME_JP)):
        lf_id=id[i]
        name_jp = LF_NAME_JP[i]
        name_cn = LF_NAME_CN[i]
        company = LF_ZZGS[i]
        release_date = LF_FSRQ[i]
        content = LF_NR[i]
        img_url = LF_IMG[i]
        tags = ','.join(LF_TAG[i])  # 将标签列表转换为逗号分隔字符串
    
        # 参数化查询，防止SQL注入
        try:
            cursor.execute('''INSERT INTO '{}' 
                            (id,name_jp, name_cn, company, release_date, content, img_url, tags)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''.format(str(NY)),
                        (lf_id,name_jp, name_cn, company, release_date, content, img_url, tags))

        except sqlite3.IntegrityError:
            # 如果插入失败，说明ID已经存在，可以选择更新或跳过
            print(f"ID {lf_id} 已存在，跳过插入。")  

    # 提交事务
    conn.commit()

    # 关闭连接
    conn.close()


def html_info_to_db(NY,html_content):

    tree = html.fromstring(html_content)
    # 使用XPath查询匹配所有具有ID属性的div元素
    div_elements = tree.xpath('//div[@id]')

    pure_digit_ids = []
    for div in div_elements:
        element_id = div.get('id')
        if element_id is not None and element_id.isdigit():
            pure_digit_ids.append(element_id)

    # 输出结果
    print(f"已成功获取里番id：{pure_digit_ids}")
    #里番日文名
    LF_NAME_JP=[]
    #里番中文名
    LF_NAME_CN=[]
    #制作公司
    LF_ZZGS=[]
    #里番发行日期
    LF_FSRQ =[]
    #里番内容
    LF_NR =[]
    #里番图片
    LF_IMG =[]
    #里番标签
    LF_TAG =[]

    for id in pure_digit_ids:
        #print("ID:", id)
        # 使用XPath查询匹配具有特定ID的div元素
        LF_NAME_JP_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/h3/text()')
        LF_NAME_CN_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/div/h4/text()')
        LF_ZZGS_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/div/h5[1]/a/text()') 
        LF_FSRQ_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/div/h5[2]/text()')
        LF_NR_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/div/h5[3]/text()')
        LF_IMG_XP = tree.xpath(f'//*[@id="{id}"]/div/div[1]/img')
        LF_TAG_XP = tree.xpath(f'//*[@id="{id}"]/div/div[2]/div/h5[5]/div/a/text()')

                                    
        LF_NAME_JP.append(LF_NAME_JP_XP[0])
        LF_NAME_CN.append(LF_NAME_CN_XP[0])
        LF_ZZGS.append(LF_ZZGS_XP[0])
        LF_FSRQ.append(LF_FSRQ_XP[0])
        LF_NR.append(LF_NR_XP[0])
        LF_IMG.append(LF_IMG_XP[0].get('src'))
        LF_TAG.append(LF_TAG_XP)

    #print(LF_NAME_JP)
    #print(LF_NAME_CN)
    #print(LF_ZZGS)
    #print(LF_FSRQ)
    #print(LF_NR)
    #print(LF_IMG)
    #print(LF_TAG[8]) 

    db_hanime_info(NY,pure_digit_ids,LF_NAME_JP, LF_NAME_CN, LF_ZZGS, LF_FSRQ, LF_NR, LF_IMG, LF_TAG)

# 设置Chrome浏览器驱动程序的路径
def get_hanime_xfyg_info(NY):
    service = Service('./chromedriver.exe')  
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--window-size=400,300')
    options.add_argument('log-level=3')
    options.add_argument("--ignore-certificate-errors")  # 忽略 SSL 证书错误
    # 初始化Chrome浏览器
    browser =  webdriver.Chrome(service=service, options=options)


    # 打开百度网页
    try:
        browser.get("https://hanime1.me/previews/"+str(NY))
        browser.implicitly_wait(45)
        page = browser.page_source
        browser.quit()
        #打印源码，防止乱码加上编码格式；
        #print(page)
        if 'Server Error' in page:
            print(f"无{NY}里番页面,请检测输入是否正确")  
        else:
            f=open('./html/'+str(NY)+'.html',mode="w",encoding="utf-8")
            f.write(page)
            f.close()
            html_info_to_db(NY,page)
    except Exception as e:
        print(f"打开网页时发生错误,请检测网页https://hanime1.me/previews/{NY}是否能打开")  
        browser.quit()
        return
  

 








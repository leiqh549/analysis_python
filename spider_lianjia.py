# -*- coding: utf-8 -*-

import urllib.request as request
from bs4 import BeautifulSoup
import json
import openpyxl


def get_soup(url):
    response = request.urlopen(url=url)
    page_source = response.read().decode("UTF-8")
    soup = BeautifulSoup(page_source, "html.parser")
    return soup


def ershou_list(city, district, page):
    url = "https://%s.lianjia.com/ershoufang/%s/pg%s" % (city, district, page)
    return get_soup(url)


def beijing_ershou():
    city = "bj"
    # district_list = [
    #     "dongcheng", "xicheng", "chaoyang", "haidian", "fengtai",
    #     "shijingshan", "tongzhou", "changping", "daxing", "yizhuangkaifaqu",
    #     "shunyi", "fangshan", "mentougou", "pinggu", "huairou", "miyun",
    #     "yanqing"
    # ]
    district_list = ["changping"]
    for district in district_list:
        getResult(city, district)


def writeListHtml(district, soup):
    with open("/Users/guoyankui/study/python/analysis/file/page_%s.html" % district, "w") as file:
        file.write(soup.prettify())


def writeHouseHtml(soup):
    with open("/Users/guoyankui/study/python/analysis/file/page_house_2.html", "w") as file:
        file.write(soup.prettify())


def getResult(city, district):
    data = []
    for page in range(0, 100):
        soup = ershou_list(city, district, page + 1)
        print("正在解析第%s页" % page)
        a_list = soup.find_all("a", attrs={"class", "title"})
        for a in a_list:
            house_code = a["data-housecode"]
            house_url = a["href"]
            house_soup = get_soup(house_url)
            total = house_soup.find("span", attrs={"class", "total"})
            try:
                shoufu_json = house_soup.find("div", attrs={"class", "new-calculator VIEWDATA"})["data-shoufu"]
                shoufu_dic = json.loads(shoufu_json)
            except:
                total_shoufu = "0"
                pure_shoufu = "0"
                total_tax = "0"
            else:
                total_shoufu = shoufu_dic["totalShoufuDesc"]
                pure_shoufu = shoufu_dic["pureShoufuDesc"]
                try:
                    total_tax = shoufu_dic["taxResult"]["taxTotalDesc"]
                except TypeError:
                    total_tax = "0"
            house_data = [a.text, total.text, total_shoufu, pure_shoufu, total_tax, house_code, house_url]
            print(house_data)
            data.append(house_data)
    return data


def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.cell(row=i+1, column=j+1, value=str(value[i][j]))
    workbook.save(path)
    print("xlsx格式表格写入数据成功！")


if __name__ == "__main__":
    data = getResult("bj", "changping")
    path = "/Users/guoyankui/study/python/analysis/file/page_bj_changping_result.xlsx"
    write_excel_xlsx(path, "数据", data)

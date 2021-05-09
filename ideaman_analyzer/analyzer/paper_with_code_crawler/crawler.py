import time
import random
import re
import requests as r
import xml.etree.ElementTree as ET
from ideaman_util.Logger import Log
from bs4 import BeautifulSoup

ARXIV_BASE_URL = 'https://arxiv.org'
ARXIV_API_URL = 'https://export.arxiv.org'
logger = Log("ideaman_analyzer/analyzer/paper_with_code_crawler/crawler.py").logger


def get_header():
    '''
    获取随机的headers,避免被arxiv ban
    :return:
    '''
    a = random.randint(12, 18)
    b = random.randint(0, 10)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_' + str(a) + '_' + str(
            b) + ') AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }
    return headers


def get_one_page(url):
    '''
    获得一个页面的内容
    :param url:
    '''
    num = 0
    while num < 10:  # 尝试十次
        try:
            response = r.get(url, headers=get_header())
            logger.info("访问" + url + "返回码:" + str(response.status_code))
            while response.status_code == 403:
                logger.error("访问" + url + "返回码:" + str(response.status_code), "访问错误")
                time.sleep(500 + random.uniform(0, 500))
                response = r.get(url, headers=get_header())
                logger.info("访问" + url + "返回码:" + str(response.status_code))
            if response.status_code == 200:
                return response.text
            return None
        except:
            logger.error("打开页面" + url + "失败,次数" + str(num))
            num += 1

def crawler_arxiv_id_lists(list_ids, num_of_papers_today,filename):
    '''
    根据arxiv_id的列表,通过api 下载论文相关信息
    :param list_ids:
    :param num_of_papers_today:
    :return:
    '''

    response = r.get(ARXIV_API_URL + '/api/query', params={
        'max_results': num_of_papers_today + 5,
        'id_list': ','.join(list_ids)
    }, headers=get_header())
    dom = ET.fromstring(response.text)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom'
    }
    num = 0  # 计数
    f = open(filename,"a+")
    for item in dom.findall('atom:entry', ns):
        title = item.find('atom:title', ns).text
        summary = item.find('atom:summary', ns).text.replace('\n', ' ').strip()
        text = title+"."+summary
        text = text.replace("\n"," ")
        f.write(text)
        f.write("\n")
    f.close()
def qa():
    for page_num in range(6,20):
        url = "https://www.paperswithcode.com/task/question-generation?page="+str(page_num)
        html = get_one_page(url)
        soup = BeautifulSoup(html, features='html.parser')
        img_list = soup.find_all(class_ = 'item-image')
        id_list = []
        for i in img_list:
            bg_image_url = str(i['style'])
            re_res = re.search("\d{4}\.\d{5}", bg_image_url)
            if re_res:
                start = re_res.span()[0]
                end = re_res.span()[1]
                id = bg_image_url[start:end]
                id_list.append(id)
        crawler_arxiv_id_lists(id_list,len(id_list),filename="./QA_papers.txt")
def nlp():
    urls = [
        "https://www.paperswithcode.com/task/emotion-recognition",
        "https://www.paperswithcode.com/task/semantic-parsing",
        "https://www.paperswithcode.com/task/semantic-textual-similarity",
        "https://www.paperswithcode.com/task/dependency-parsing",
        "https://www.paperswithcode.com/task/information-retrieval",
        "https://www.paperswithcode.com/task/natural-language-inference",
        "https://www.paperswithcode.com/task/relation-extraction",
        "https://www.paperswithcode.com/task/reading-comprehension",
        "https://www.paperswithcode.com/task/text-summarization",
        "https://www.paperswithcode.com/task/named-entity-recognition-ner",
        "https://www.paperswithcode.com/task/text-generation",
        "https://www.paperswithcode.com/task/data-augmentation",
        "https://www.paperswithcode.com/task/sentiment-analysis",
        "https://www.paperswithcode.com/task/topic-models",
        "https://www.paperswithcode.com/task/text-classification",
        "https://www.paperswithcode.com/task/language-modelling",
        "https://www.paperswithcode.com/task/machine-translation",
        "https://www.paperswithcode.com/task/chinese-word-segmentation",
        "https://www.paperswithcode.com/task/cross-lingual-transfer",
        "https://www.paperswithcode.com/task/part-of-speech-tagging"

    ]

    for page_num in range(5, 25):
        for a in urls:
            url = a+"?page=" + str(page_num)
            html = get_one_page(url)
            soup = BeautifulSoup(html, features='html.parser')
            img_list = soup.find_all(class_='item-image')
            id_list = []
            for i in img_list:
                bg_image_url = str(i['style'])
                re_res = re.search("\d{4}\.\d{5}", bg_image_url)
                if re_res:
                    start = re_res.span()[0]
                    end = re_res.span()[1]
                    id = bg_image_url[start:end]
                    id_list.append(id)
            crawler_arxiv_id_lists(id_list, len(id_list), filename="./NLP_papers.txt")
def rec():
    for page_num in range(7,40):
        url = "https://www.paperswithcode.com/task/recommendation-systems?page="+str(page_num)
        html = get_one_page(url)
        soup = BeautifulSoup(html, features='html.parser')
        img_list = soup.find_all(class_ = 'item-image')
        id_list = []
        for i in img_list:
            bg_image_url = str(i['style'])
            re_res = re.search("\d{4}\.\d{5}", bg_image_url)
            if re_res:
                start = re_res.span()[0]
                end = re_res.span()[1]
                id = bg_image_url[start:end]
                id_list.append(id)
        crawler_arxiv_id_lists(id_list,len(id_list),filename="./REC_papers.txt")
if __name__ == '__main__':
    nlp()







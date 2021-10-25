import async_timeout
from bs4 import BeautifulSoup
from datetime import datetime
import aiohttp
import sqlite3
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

BASE_URL = cfg['web']['base_url']
DATABASE = cfg['db']['database']
TABLE = cfg['db']['table-name']

async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()
    
async def soup_d(html, display_result=False):
    soup = BeautifulSoup(html, 'html.parser')
    if display_result:
        print(soup.prettify())
    return soup

def get_tag_href(obj):
    tag = str(obj).split('>')[1].split('<')[0]
    link = obj['href']
    item = [tag, link]
    return item

def persist_data(data):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(TABLE))
    cursor.execute('''CREATE TABLE IF NOT EXISTS {} 
    (manufacturer TEXT, 
    category TEXT, 
    model TEXT, 
    part TEXT, 
    part_category TEXT)'''.format(TABLE))
    print ('Table created successfully')
    try:
        for row in data:
            cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(TABLE), (row))
        connection.commit()
        print ("{} records added successfully".format(len(data)))
    except:
        print ("Error in query execution")
        connection.rollback()
        connection.close()

async def main(url):
    try:
        async with aiohttp.ClientSession() as session:
            # Crawl web
            start = datetime.now()
            print(datetime.now().strftime("%d.%b.%Y.%H.%M.%S"),'Commenced web crawling')
            html = await fetch(session, url)
            soup = await soup_d(html, display_result=False)
            results = soup.find(id = 'content')
            elements = []
            for result in results.find_all('a', href=True):
                item = get_tag_href(result)
                elements.append(item)
            category_ele = []
            for ele in elements:
                html = await fetch(session, BASE_URL+ele[1])
                soup = await soup_d(html, display_result=False)
                res = soup.find(id = 'content')
                for result in res.find_all('a', href=True):
                    category = get_tag_href(result)
                    category_ele.append([ele[0],category[0],category[1]])
            model_ele = []
            for ele in category_ele:
                html = await fetch(session, BASE_URL+ele[2])
                soup = await soup_d(html, display_result=False)
                res = soup.find(class_ = "c_container allmodels")
                for result in res.find_all('a', href=True):
                    model = get_tag_href(result)
                    model_ele.append([ele[0],ele[1],model[0],model[1]])
            part_ele = []
            for ele in model_ele:
                try:
                    html = await fetch(session, BASE_URL+ele[3])
                    soup = await soup_d(html, display_result=False)
                    res = soup.find(class_ = "c_container allparts")
                    for result in res.find_all('a', href=True):
                        span = str(result.find_all('span')).split('>')[1].split('<')[0]
                        part = get_tag_href(result)
                        part_ele.append([ele[0].strip(),ele[1].strip(),ele[2].strip(),part[0].strip('- '),span])
                except Exception:
                    pass 
            print(datetime.now().strftime("%d.%b.%Y.%H.%M.%S"), 'Concluded web crawling')
            #persist data
            persist_data(part_ele)
            print('Duration: {}'.format(datetime.now() - start))
    except Exception:
        pass 
    

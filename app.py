import asyncio
import uvicorn
from datetime import datetime
from fastapi import FastAPI
import sqlalchemy as db
import pandas as pd
import crawl 
import yaml


with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

URL = cfg['web']['url']
DATABASE = cfg['db']['database']
TABLE = cfg['db']['table-name']
HOST = cfg['server']['host']
PORT = cfg['server']['port']


app = FastAPI()
engine = db.create_engine('sqlite:///{}'.format(DATABASE))
 
try:
    check = pd.read_sql('select count(*) from {}'.format(TABLE), engine)
except:
    print(datetime.now().strftime("%d.%b.%Y.%H.%M.%S"),'Populating Database')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(crawl.main(URL))
        engine = db.create_engine('sqlite:///{}'.format(DATABASE))
    except:
        print('Error Loading DB')
        


@app.get('/find-by-manufacturer')
async def find_manufacturer(manufacturer: str):
    query = pd.read_sql('select manufacturer,category,model,part,part_category from {} where manufacturer = "{}"'.format(TABLE, manufacturer.strip()), engine)
    return query.to_dict('index')

@app.get('/find-by-category')
async def find_category(category: str):
    query = pd.read_sql('select manufacturer,category,model,part,part_category from {} where category = "{}"'.format(TABLE, category.strip()), engine)
    return query.to_dict('index')

@app.get('/find-by-model')
async def find_model(model: str):
    query = pd.read_sql('select manufacturer,category,model,part,part_category from {} where model = "{}"'.format(TABLE, model.strip()), engine)
    return query.to_dict('index')

@app.get('/find-by-part')
async def find_part(part: str):
    query = pd.read_sql('select manufacturer,category,model,part,part_category from {} where part = "{}"'.format(TABLE, part.strip()), engine)
    return query.to_dict('index')

@app.get('/find-by-part-category')
async def find_part_category(part_category: str):
    query = pd.read_sql('select manufacturer,category,model,part,part_category from {} where part_category = "{}"'.format(TABLE, part_category.strip()), engine)
    return query.to_dict('index')

if __name__ == '__main__':
    uvicorn.run('app:app', port=PORT, host=HOST)
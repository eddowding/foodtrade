import requests
from datetime import datetime
from multiprocessing import Process
from math import ceil
from menu.mongo_models import *


API_BASE = 'http://api.ratings.food.gov.uk'
API_HEADER = {'x-api-version': 2}
API_LIMIT = 10
API_CALL_POOL_SIZE = 4

ENTITY_API_MAPPING = {
    'regions': {'part': 'Regions', 'model': Region},
    'authorities': {'part': 'Authorities', 'model': Authority},
    'businessTypes': {'part': 'BusinessTypes', 'model': BusinessType},
    'countries': {'part': 'Countries', 'model': Country},
    'establishments': {'part': 'Establishments/basic', 'model': Establishment}
}

class FSAAPI(object):
    def _get_page_urls(self, entity_type):
        entity = ENTITY_API_MAPPING.get(entity_type)
        pager = requests.get(url='%s/%s/1/1' % (API_BASE, entity['part']), headers=API_HEADER).json()
        total_count = pager.get('meta').get('totalCount')
        pages = int(ceil(total_count / float(API_LIMIT)))
        urls = []
        for x in range(1, pages+1):
            urls.append('%s/%s/%d/%d' % (API_BASE, entity['part'], x, API_LIMIT))
        return urls

    def _fetch_and_store(self, entity_type, url):
        print 'Processing url: %s started.......' % url
        entity = ENTITY_API_MAPPING.get(entity_type)
        model_class = entity.get('model')
        data = requests.get(url=url, headers=API_HEADER).json()
        insert_list = []
        for obj in data.get(entity_type):
            if entity_type == 'establishments': #TODO: fix this
                obj = requests.get(url='%s/Establishments/%d' % (API_BASE, obj['FHRSID']), headers=API_HEADER).json()
            if 'id' in obj:
                obj['fsa_id'] = obj['id']
                del obj['id']
            if obj.get('geocode') and obj.get('geocode').get('latitude') and obj.get('geocode').get('longitude'):
                obj['geocode'] =[float(obj.get('geocode').get('longitude')), float(obj.get('geocode').get('latitude'))]
            else:
                del obj['geocode']
            obj['added_on'] = datetime.now()
            insert_list.append(model_class(**obj))
        model_class.objects.insert(insert_list)
        print '....Done processing url: %s' % url

    def process(self, entity_type):
        for url in self._get_page_urls(entity_type):
            p = Process(target=self._fetch_and_store, args=(entity_type, url))
            p.start()
            p.join()

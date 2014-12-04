import requests
from datetime import datetime
from math import ceil
from menu.mongo_models import Region


API_BASE = 'http://api.ratings.food.gov.uk'
API_HEADER = {'x-api-version': 2}
API_LIMIT = 10

ENTITY_API_MAPPING = {
    'regions': {'part': 'Regions', 'page': False, 'model': Region},
    'authorities': {'parts': ['Authorities'], 'page': False}
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
        entity = ENTITY_API_MAPPING.get(entity_type)
        model_class = entity.get('model')
        data = requests.get(url=url, headers=API_HEADER).json()
        insert_list = []
        for obj in data.get(entity_type):
            if 'id' in obj:
                obj['fsa_id'] = obj['id']
                del obj['id']
            obj['added_on'] = datetime.now()
            insert_list.append(model_class(**obj))
        return model_class.objects.insert(insert_list, load_bulk=True)

    def process(self, entity_type):
        for url in self._get_page_urls(entity_type):
            self._fetch_and_store(entity_type, url)

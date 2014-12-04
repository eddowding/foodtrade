import requests


API_BASE = 'http://api.ratings.food.gov.uk'
API_HEADER = {'x-api-version': 2}

ENTITY_API_MAPPING = {
    'regions': {'parts': ['Regions'], 'page': False}
}

class FSAAPI(object):
    def _get_url(self, entity_type):
        entity = ENTITY_API_MAPPING.get(entity_type)
        if entity == None:
            raise Exception('Entity not mapped')
        url_parts = [API_BASE]
        url_parts += entity['parts']
        return '/'.join(url_parts)

    def _request(self, entity_type):
        url = self._get_url(entity_type)
        return requests.get(url=url, headers=API_HEADER)

    def _get_json(self, entity_type):
        return self._request(entity_type).json()

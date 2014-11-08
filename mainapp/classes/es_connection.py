from elasticutils import get_es
from django.conf import settings


ES_MAPPING = {
    'mappings': {
        'userprofile': {
            'properties': {
                'useruid': {'type': 'integer', 'store': True, 'index': 'not_analyzed'},
                'username': {'type': 'string', 'store': True, 'index': 'no'},
                'name': {'type': 'string', 'store': True, 'index': 'analyzed'},
                'description': {'type': 'string', 'store': True, 'index': 'analyzed'},
                'sign_up_as': {'type': 'string', 'store': True, 'index': 'not_analyzed'},
                'address': {'type': 'string', 'store': True, 'index': 'analyzed'},
                'profile_img': {'type': 'string', 'store': True, 'index': 'no'},
                'profile_banner_url': {'type': 'string', 'store': True, 'index': 'no'},
                'latlng': {'type': 'geo_point', 'store': True, 'index': 'analyzed'}
            }
        }
    }
}

class ESConnection(object):
"""
Elastic search CRUD operations.
"""

    def __init__(self):
        """
        Setup connection and create indexes.
        """
        self.conn = get_es(urls=settings.ES_URLS)
        if not self.conn.indices.exists(index=settings.ES_INDEX):
            self.conn.indices.create(index=settings.ES_INDEX, body=ES_MAPPING)

    def mapping_exists(self, doc_type):
        return doc_type in ES_MAPPING['mappings']

    def _mongo_obj_to_es(self, mongo_obj):
        """
        Structure the mongo document for indexing into ES.
        """
        doc = mongo_obj
        id = str(doc._id)
        del doc['_id']
        doc['id'] = id
        return doc

    def create(self, doc_type, mongo_obj):
        """
        Create document in ES index.
        """
        doc = self._mongo_obj_to_es(mongo_obj)
        return self.conn.index(index=settings.ES_INDEX, doc_type=doc_type, body=doc, id=doc['id'])

    def update(self, id, doc_type, document):
        """
        Update document by ID and document type.
        """
        pass

    def read(self, id, doc_type):
        """
        Fetch document by ID and document type.
        """
        return self.conn.get(index=settings.ES_INDEX, doc_type=doc_type, id=id)

    def delete(self, id, doc_type):
        """
        Delete document by ID and document type.
        """
        return self.conn.delete(index=settings.ES_INDEX, doc_type=doc_type, id=id)

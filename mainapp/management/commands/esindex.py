from django.core.management.base import BaseCommand, CommandError
from pymongo import Connection
from mainapp.classes.es_connection import ESConnection


class Command(BaseCommand):
    help = 'Elastic Search Indexer'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Please provide collection name as argument.')
        if len(args) > 1:
            raise CommandError('Only one argument of collection name supported.')
        collection_name = args[0]
        mongo_conn = Connection()
        db = mongo_conn.foodtrade
        collection = db[collection_name]
        self.stdout.write('Collection "%s" as %d objects to index.' % (collection_name, collection.count()))
        es_conn = ESConnection()
        if not es_conn.mapping_exists(collection_name):
            raise CommandError('Mapping for collection "%s" missing.' % collection_name)
        for obj in collection.find():
            es_conn.create(collection_name, obj)
            self.stdout.write('Mongo object ID : %s indexed.' % obj['_id'])

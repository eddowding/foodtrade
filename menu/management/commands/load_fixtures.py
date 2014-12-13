from django.core.management.base import BaseCommand, CommandError
from menu.models import *
import csv ,os
import datetime


class Command(BaseCommand):
   # args = 'Entity type'

    def handle(self, *args, **options):
        type_match = False
        type_miss = False
        if (args and os.path.exists(args[0])):
            with open(args[0]) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for data in reader:
                    for item in data:
                        if len(args)>1:
                            if (args[1] == 'allergen'):
                                allergen = Allergen()
                                allergen.name = item
                                allergen.added_on = datetime.datetime.now()
                                allergen.save()
                                type_match = True
                            elif (args[1] == 'meat'):
                                meat = Meat()
                                meat.name = item
                                meat.added_on = datetime.datetime.now()
                                meat.save()
                                type_match = True
                            elif (args[1] == 'gluten'):
                                gluten = Gluten()
                                gluten.name = item
                                gluten.added_on = datetime.datetime.now()
                                gluten.save()
                                type_match = True
                            type_miss = True


        else:
            print 'File doesn\'t exist'

        if (not type_miss):
            print 'OOPS , you didnt provide the type!'
            if (not type_match):
                print 'Type doesn\'t match '
        else:
            print 'Successfully added'




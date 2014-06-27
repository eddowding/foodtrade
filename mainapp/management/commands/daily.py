#!/usr/bin/env python
# encoding: utf-8
# Create your views here.

from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    help = 'Sends weekly newsletter'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        import urllib2
        baseurl = "http://foodtrade.com/kpi/"
        response = urllib2.urlopen(baseurl)     
        from _newdaily import send_newsletter, trending_hash_tags
        trending_hash_tags()
        send_newsletter('Daily')
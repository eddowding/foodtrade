#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import MySQLdb

class MySQLConnect():
    def __init__(self):
        self.DB_USER_NAME = 'root'
        self.DB_USER_PASSWD = 'root'
        self.DB_NAME= 'foodtrade'
        self.HOST = 'localhost'

    def execute_sql(self, sql_query_text):
        connection = MySQLdb.connect(host=self.HOST, user=self.DB_USER_NAME, passwd=self.DB_USER_PASSWD,db=self.DB_NAME)
        from contextlib import closing
        with closing( connection.cursor() ) as cursor:
            cursor.execute(sql_query_text)
            res = cursor.fetchall()
        connection.close()
        return res

    def get_token(self, screen_name):
        auth_usr_id = self.execute_sql('Select id from auth_user where username =\'' + screen_name +'\';')[0][0]
        social_account_id = self.execute_sql('Select id from socialaccount_socialaccount where user_id =\'' + str(auth_usr_id) +'\';')[0][0]
        social_token = self.execute_sql('Select token,token_secret from socialaccount_socialtoken where account_id =\'' + str(social_account_id) +'\';')
        return social_token[0]

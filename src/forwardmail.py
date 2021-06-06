#!/usr/bin/python3

import sys
import email
import smtplib
import random
import sqlite3
import datetime

class database:   #move class to seperate file
    def __init__(self):
        self.conn = None
        self.dbFile = '/tmp/mailaddresses.sqlite3'   #pick better place
        self.maxAgeInDays = 30
        self.create_connection()

        sql_create_urls_table = """ CREATE TABLE IF NOT EXISTS mailAddresses (
                                        id integer PRIMARY KEY,
                                        mailAddress text NOT NULL,
                                        toMailaddress text NOT NULL,
                                        startDate text NOT NULL
                                    ); """
        self.create_table(sql_create_urls_table)


    def executeSql(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            if sql.startswith('INSERT'):
                self.conn.commit()
            elif sql.startswith('SELECT'):
                return cur.fetchall()
        except Exception:
            print("SQL EXCEPTION!")
            print(sql)


    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.dbFile)
            #print(sqlite3.version)
        except Error as e:
            print(e)
        #finally:
        #    if conn:
        #       conn.close()

    def create_table(self, createTableSql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cur = self.conn.cursor()
            cur.execute(createTableSql)
        except Error as e:
            print(e)

    def mailAddressExists(self, mailAddress):
        sql = 'SELECT mailAddress FROM mailAddresses WHERE mailAddress="%s"'%( mailAddress )
        rows = self.executeSql(sql)
        if len(rows)> 0:
            return True
        else:
            return False

    def addMailAddress(self, mailAddress, toMailAddress):
       sql = 'INSERT INTO mailAddresses(mailAddress, toMailAddress, startDate) VALUES("%s", "%s", datetime(\'now\'))'%( mailAddress, toMailAddress )
       self.executeSql(sql)

    def getToMailAddress(self, mailAddress):
        sql = 'SELECT toMailaddress, startDate FROM mailAddresses WHERE mailAddress="%s"'%( mailAddress )
        print(sql)
        rows = self.executeSql(sql)
        
        startDate = datetime.datetime.strptime(rows[0][1], '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        
        if (now - startDate).days > self.maxAgeInDays:
            return None
        else:
            if len(rows)> 0:
                return rows[0][0]
            else:
                return None


db = database()

full_msg = ""
for line in sys.stdin:
  full_msg += line

msg = email.message_from_string(full_msg)
msg['To']  = db.getToMailAddress(msg["to"])

if msg['To'] is not None:
    with smtplib.SMTP('localhost') as s:
      s.send_message(msg)

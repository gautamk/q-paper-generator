#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
try: 
  from xml.etree import ElementTree
except ImportError:  
  from elementtree import ElementTree
import gdata.auth
import gdata.docs.client
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template

SETTINGS = {
    'APP_NAME': 'Q-Paper-Generator',
    'CONSUMER_KEY': 'www.q-paper-generator.appspot.com',
    'CONSUMER_SECRET': 'zjbGcqnb9PTrlIBUDXso2HOY',
    'SCOPES': ['https://docs.google.com/feeds/']
    }
gdocs = gdata.docs.client.DocsClient(source = SETTINGS['APP_NAME'])
gd_client = gdata.spreadsheet.service.SpreadsheetsService() 
class GetSingleUseKey(webapp.RequestHandler):
    def get(self):
        import gdata.auth
        next = 'http://%s/GetSessionKey' % self.request.host
        scope = 'http://spreadsheets.google.com/feeds/'
        secure = False  # set secure=True to request secure AuthSub tokens
        session = True
        auth_sub_url = gdata.auth.GenerateAuthSubUrl(next, scope, secure=secure, session=session)
        self.redirect(auth_sub_url)

class GetSessionKey(webapp.RequestHandler):
    def get (self):
        token = gdata.auth.extract_auth_sub_token_from_url(
        url = self.request.host + self.request.path + "?token=" + self.request.get('token') )
        gd_client.token_store.add_token(token)
        #gd_client.GetAuthSubToken()
        gd_client.UpgradeToSessionToken(token)
        self.redirect('/GetSpreadSheetList')
        

class GetSpreadSheetList(webapp.RequestHandler):
    def get (self):
       feed = gd_client.GetSpreadsheetsFeed()
       self.response.out.write("""
       <form action="/GetWorksheetList" method="get" >
       """)
       i=0
       for entry in feed.entry:
           self.response.out.write("<p><label>%s:</label><input type='radio' value='%s' name='spreadsheetid' /> </p>\n" % (entry.title.text,str(i)) )
           i+=1
       self.response.out.write("""
        <button type="submit" >Get SpreadSheet</button>
        <form>
        """)

class GetWorksheetList(webapp.RequestHandler):
    def get (self):
        import string
        feed = gd_client.GetSpreadsheetsFeed()
        input = self.request.get('spreadsheetid')
        id_parts = feed.entry[string.atoi(input)].id.text.split('/')
        self.curr_key = id_parts[len(id_parts) - 1]
        feed = gd_client.GetWorksheetsFeed(self.curr_key)
        self.response.out.write("""
       <form action="/PrintWorkSheet" method="get" >
       <input type ='hidden' value = "%s" name="spreadsheetid"
       """ % input)
        i=0
        for entry in feed.entry:
           self.response.out.write("<p><label>%s:</label><input type='radio' value='%s' name='worksheetid' /> </p>\n" % (entry.title.text,str(i)) )
           i+=1
        self.response.out.write("""
        <button type="submit" >Get SpreadSheet</button>
        <form>
        """)

class PrintWorkSheet(webapp.RequestHandler):
    def get(self):
        print "Print WorkSheet"

def main():
    application = webapp.WSGIApplication([
    ('/GetSingleUseKey',GetSingleUseKey),
    
    ('/GetSessionKey',GetSessionKey),
    
    ('/GetSpreadSheetList',GetSpreadSheetList),
    
    ('/GetWorksheetList',GetWorksheetList),
    
    ('/PrintWorkSheet',PrintWorkSheet),
    
    ('/worksheet',GetSingleUseKey),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

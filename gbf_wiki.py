import requests
from bs4 import BeautifulSoup
import calendar
import time
from datetime import datetime
import math
import re
import titlecase

class GbfWiki:
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}
        self.url = 'https://gbf.wiki'
    
    def get_response():
        response = requests.get('https://gbf.wiki')
        page_content = response.content
        soup = BeautifulSoup(page_content, 'lxml')

        return soup

    # * Current Events *
    def cur_event():
        # Defines current time in form of Dynamic Timestamp
        gmt = time.gmtime()
        timestamp = calendar.timegm(gmt)
        
        soup = GbfWiki.get_response()
        # Find and print all current events
        for td in soup.findAll('td', {'style': 'vertical-align: top; text-align: center;'}):
            cur_evt_list = []
            for img in td.findAll('img'):
                evt = img.get('alt')

                # Prevents duplicate entries in case same event has multiple banners img
                if evt not in cur_evt_list:
                    cur_evt_list.append(evt)
            
            # Creates 2 lists that keeps track of start timestamps and end timestamps
            start_time = []
            end_time = []
            for span in td.findAll('span', {'class': 'localtime'}):
                start_time.append(span.get('data-start'))
                end_time.append(span.get('data-end'))

        return cur_evt_list, start_time, end_time, timestamp


    # * Upcoming Events *
    def up_event():
        
        soup = GbfWiki.get_response()
        # gbf.wiki's upcoming event td is identified with the last value of "style="vertical-align: top;""
        style_list = []

        # gbf.wiki's table format <td style="vertical-align: top;">
        for td in soup.find_all('td', {'style': 'vertical-align: top;'}):
            style_list.append(td)

        # Selects last td which contains upcoming event information as established previously 
        up_evt = style_list[len(style_list)- 1]
        up_evt_list = []
        
        # <a href="LINK TO NAME OF EVENT" title="NAME OF EVENT">
        for a in up_evt.findAll('img'):
            evt = a.get('alt')

            # Prevents duplicate entries in case same event has multiple banners img
            if evt not in up_evt_list:
                up_evt_list.append(evt)
        
        # Every odd entry is start time, even entry is end time
        time = []
        for span in up_evt.findAll('span', {'class': 'localtime'}):
            datetime = span.get('data-time')
            if datetime not in time:
                time.append(datetime)
        
        # Create a dictionary that uses event as key,
        # and a list of start and end date as values.
        up_evt_sch = {}
        for entry_name in up_evt_list:
            up_evt_time = []
            # First append/pop is Start date
            up_evt_time.append(time[0])
            time.pop(0)
            # Second append/pop is End date
            up_evt_time.append(time[0])
            time.pop(0)

            up_evt_sch[entry_name] = up_evt_time
            
        return up_evt_sch
    
    def search(user_input):
        search = re.sub("\s+", "%20", user_input)
        try:
            search_api = f"https://gbf.wiki/api.php?action=opensearch&format=json&search={search}&redirects=resolve"

            response = requests.get(search_api)
            responseData = response.json()
            return responseData[3][0]
        except:
            return "Try Again."
### This file scrapes the last 9 weeks of the billboard charts and saves the result as csv per week in billboards/###


import requests # to download html code
from bs4 import BeautifulSoup # to navigate through the html code
import pandas as pd
import numpy as np
import re
from datetime import datetime, date

website = 'https://www.billboard.com/charts/hot-100/' #Website to be scraped

# get dates of last 10 saturdays:

iso_date = datetime.now().isocalendar()
last10weeks = [date.fromisocalendar(iso_date.year, iso_date.week-i, 6) for i in range(0,9)]
last10sat = [f'{item.year}-{item.month:02d}-{item.day:02d}' for item in last10weeks]

# Selectors:

pos_selector = 'span.c-label.a-font-primary-bold-l.u-font-size-32\@tablet.u-letter-spacing-0080\@tablet'
week_selector = '#post-1479786 > div.pmc-paywall > div > div > div > div.lrv-u-flex.lrv-u-align-items-center.lrv-u-justify-content-space-between.lrv-u-padding-lr-075\@mobile-max.lrv-u-flex-direction-column\@mobile-max > p'
interpretor_selector_list = "ul > li.o-chart-results-list__item.\/\/.lrv-u-flex-grow-1.lrv-u-flex.lrv-u-flex-direction-column.lrv-u-justify-content-center.lrv-u-border-b-1.u-border-b-0\@mobile-max.lrv-u-border-color-grey-light.lrv-u-padding-l-1\@mobile-max > span"
title_selector_list = "ul > li.o-chart-results-list__item.\/\/.lrv-u-flex-grow-1.lrv-u-flex.lrv-u-flex-direction-column.lrv-u-justify-content-center.lrv-u-border-b-1.u-border-b-0\@mobile-max.lrv-u-border-color-grey-light.lrv-u-padding-l-1\@mobile-max > h3"
last_pos_selector = 'ul > li.lrv-u-width-100p > ul > li:nth-child(4) > span'


# loop to get last 10 weeks of billboard charts
for weeklychart in last10sat:
    url = website + weeklychart + '/'
    response = requests.get(url)
    print(response.status_code)
   

    soup = BeautifulSoup(response.text, 'html.parser')
    # Lists

    week =  soup.select(week_selector)[0].get_text().replace('Week of ', '')
    week_date = datetime.strptime(week, '%B %d, %Y')
    week_nr = week_date.isocalendar()[1]

    position = [elem.get_text().replace("\n","").replace("\t","") for elem in soup.select(pos_selector)]

    titles = [elem.get_text().replace("\n","").replace("\t","") for elem in soup.select(title_selector_list)]

    interprets = [elem.get_text().replace("\n","").replace("\t","") for elem in soup.select(interpretor_selector_list)]
    
    last_position = [elem.get_text().replace("\n","").replace("\t","") for elem in soup.select(last_pos_selector)]
    last_week_pos = last_position[0::2]
    peak_pos = last_position[1::2]

    song_prod_imp = [item.get_text().replace("\n","").replace("\t","") for item in soup.select('div div div h3#title-of-a-story, div div div h3#title-of-a-story + p')]
    item_before = str
    songwriter= []
    for item in song_prod_imp:
        if item_before == 'Songwriter(s):':
            songwriter.append(item)
        item_before = item
    
    producers= []
    for item in song_prod_imp:
        if item_before == 'Producer(s):':
            producers.append(item)
        item_before = item
    
    label= []
    for item in song_prod_imp:
        if item_before == 'Imprint/Promotion Label:':
            label.append(item)
        item_before = item

    # To Dataframe

    BillboardTop100df = pd.DataFrame({'position': position,\
                                      'interpret': interprets,\
                                      'title':titles,\
                                      'songwriters': songwriter[1:101],\
                                      'producers': producers[1:101],\
                                      'label': label[1:101],\
                                      'last_week':last_week_pos,\
                                      'peak':peak_pos,\
                                      'week_date': week_date,\
                                      'week_nr':week_nr
                                     })

    BillboardTop100df.to_csv(f'billboard/billboardTop100{weeklychart}.csv')

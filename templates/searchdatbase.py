
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week Three"""

#import needed libraries

import urllib2
import csv
from pprint import pprint
import re


def downloadData(url):
    """Downloads data from URL
    Args:
        url (string): string value for URL data fetch
    Returns:
        data: something to return
    """
    value = urllib2.Request(url)
    data = urllib2.urlopen(value)

    #print data.read()
    return data

def processData(fileContents):
    """Processes data passed in
    Args:
        fileContents (object): string value the data file
    Returns:
        full_database: something to return
    """

    #print fileContents.read()
    full_database = {}
    person_data = []

    reader = csv.reader(fileContents, delimiter=',')

    for row, item in enumerate(reader):
        full_database [row] = {
            'Path': item[0],
            'Accessed': item[1],
            'Browser': item[2],
            'Status': item[3],
            'file_Size': item[4]
        }

        #print row[1]

    #print 'Image requests account for 45.3% of all requests', img_hit_counter
    #print fileContents.read()

    return full_database

def calculateImageHits(dataDict):
    """Processes data passed in
    Args:
        dataDict (dict): Dictionry of data
    Returns:
        Image_Percentage: float value for image hit
    """

    img_hit_counter = 0
    r1 = re.compile("(?i)\.jpg$")
    r2 = re.compile("(?i)\.gif$")
    r3 = re.compile("(?i)\.png$")

    for key,value in dataDict.iteritems():
        if r1.search(dataDict[key]['Path']) or r2.search(dataDict[key]['Path']) or r3.search(dataDict[key]['Path']):
            img_hit_counter += 1

    # print row, item[0]
    #if r1.search(item[0]) or r2.search(item[0]) or r3.search(item[0]):
    #   img_hit_counter += 1

    Image_Percentage = 100 * float(img_hit_counter) / float(len(dataDict))
    #print img_hit_counter
    #print len(dataDict)
    #print Image_Percentage

    return Image_Percentage

def calculatePopularBrowser(dataDict):
    """Processes data passed in
    Args:
        dataDict (dict): Dictionry of data
    Returns:
        browser: string with Browser name
    """

    firefox_counter = 0
    chrome_counter = 0
    ie_counter = 0
    safari_counter = 0

    rf = re.compile("Firefox")
    rc = re.compile("Chrome")
    rs = re.compile("Safari")
    rie = re.compile("(?i)MSIE")

    for key,value in dataDict.iteritems():
        #print dataDict[key]['Browser']
        user_agent = dataDict[key]['Browser']
        #print 'Browser: ',user_agent

        if rf.search(user_agent):
            firefox_counter += 1
        elif rie.search(user_agent):
            ie_counter += 1
        elif rc.search(user_agent) and rs.search(user_agent):
            chrome_counter += 1
        else:
            safari_counter += 1
            #print dataDict[key]['Browser']

    browser_data = {}

    browser_data = {
        'Firefox': firefox_counter,
        'IE': ie_counter,
        'Chrome': chrome_counter,
        'Safari': safari_counter
    }

    browser = max(browser_data, key=browser_data.get)

    return browser

def main():
    url = args.url if args.url else raw_input("Please provide the URL for data retrieval: ")
    #url = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

    if url != '':
        print 'Processing url for data: ' +url
        try:
            csvData = downloadData(url)

            databaseData = processData(csvData)
            #pprint (databaseData)
            print 'Data has been added to database' , len(databaseData)
            percentResult = calculateImageHits(databaseData)
            print 'Image requests account for', percentResult,'% of all requests'
            popularBrowser = calculatePopularBrowser(databaseData)
            print 'Most Popular Browser: ', popularBrowser


        except ValueError:
            print 'There was an error processing the URL'

    else:
        print 'URL is required'





if __name__ == "__main__":
    main()

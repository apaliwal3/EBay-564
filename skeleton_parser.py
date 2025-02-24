
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import os
from collections import defaultdict

columnSeparator = "|"

def writeToFile(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def escape(s):
    return s.replace('"', '""').replace('\\', '\\\\') if s else ''

# Global sets to track unique entries
users_seen = set()
categories_seen = set()

def writeToFile(filename, data):
    with open(filename, 'a') as f:
        for line in data:
            f.write(line + '\n')

def processUser(user_data, location="", country=""):
    if not user_data['UserID'] in users_seen:
        users_seen.add(user_data['UserID'])
        return f"{escape(user_data['UserID'])}{columnSeparator}" + \
               f"{user_data['Rating']}{columnSeparator}" + \
               f"{escape(location)}{columnSeparator}" + \
               f"{escape(country)}"
    return None

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    # Initialize lists to store data for each table
    users_data = []
    items_data = []
    categories_data = []
    item_categories_data = []
    bids_data = []
    
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']
        
        for item in items:
            # Process Seller
            seller_data = processUser(item['Seller'], item['Location'], item['Country'])
            if seller_data:
                users_data.append(seller_data)
            
            # Process Item
            item_str = f"{item['ItemID']}{columnSeparator}" + \
                      f"{escape(item['Name'])}{columnSeparator}" + \
                      f"{transformDollar(item['Currently'])}{columnSeparator}" + \
                      f"{transformDollar(item.get('Buy_Price', ''))}{columnSeparator}" + \
                      f"{transformDollar(item['First_Bid'])}{columnSeparator}" + \
                      f"{item['Number_of_Bids']}{columnSeparator}" + \
                      f"{escape(item['Location'])}{columnSeparator}" + \
                      f"{escape(item['Country'])}{columnSeparator}" + \
                      f"{transformDttm(item['Started'])}{columnSeparator}" + \
                      f"{transformDttm(item['Ends'])}{columnSeparator}" + \
                      f"{escape(item['Seller']['UserID'])}{columnSeparator}" + \
                      f"{escape(item['Description'])}"
            items_data.append(item_str)
            
            # Process Categories
            for category in item['Category']:
                if category not in categories_seen:
                    categories_seen.add(category)
                    categories_data.append(escape(category))
                item_categories_data.append(f"{item['ItemID']}{columnSeparator}{escape(category)}")
            
            # Process Bids
            if item['Bids']:
                for bid in item['Bids']:
                    # Process Bidder
                    bidder = bid['Bid']['Bidder']
                    bidder_data = processUser(bidder, 
                                           bidder.get('Location', ''),
                                           bidder.get('Country', ''))
                    if bidder_data:
                        users_data.append(bidder_data)
                    
                    # Create Bid entry
                    bid_str = f"{item['ItemID']}{columnSeparator}" + \
                             f"{escape(bidder['UserID'])}{columnSeparator}" + \
                             f"{transformDttm(bid['Bid']['Time'])}{columnSeparator}" + \
                             f"{transformDollar(bid['Bid']['Amount'])}"
                    bids_data.append(bid_str)
    
    # Write all data to respective files
    writeToFile("User.dat", users_data)
    writeToFile("Item.dat", items_data)
    writeToFile("Category.dat", categories_data)
    writeToFile("Item_Category.dat", item_categories_data)
    writeToFile("Bid.dat", bids_data)


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)

    for filename in ["Item.dat", "User.dat", "Category.dat", "Item_Category.dat", "Bid.dat"]:
        if os.path.exists(filename):
            os.remove(filename)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
#!/bin/env python

# Script to extract list of KLSE stocks that give bonus and priced less than or equal to RM 1

# Copyright (c) 2015 Sharuzzaman Ahmat Raslan sharuzzaman@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
from BeautifulSoup import BeautifulSoup
import csv

# grab the HTML from the website
response = urllib2.urlopen('http://klse.i3investor.com/jsp/entann.jsp')
rawfile = response.read()

# create beautifulsoup object
soup = BeautifulSoup(rawfile)

# grab 6th table in the HTML
tables = soup('table')[6]

# grab the table header
thead = soup('table')[6].thead

# get the text of the table header
headers = [header.text for header in thead.findAll('th')]

# remove detail column
headers.pop(0)

rows = []

# get value for all column, except column 1
for row in tables.findAll('tr')[1:]:
  rows.append([val.text for val in row.findAll('td')[1:]])

# only select column 5 if the value is less than or equal to 1
data = [ x for x in rows if float(x[4]) <= 1 ]

# convert string to float in column 5
for i in data:
  i[4] = float(i[4])

# create a sorted list, sorted according to column 5
sorteddata = sorted(data, key=lambda v: v[4])

# write the data into CSV file
with open('bonus.csv', 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(headers)
  writer.writerows(sorteddata)

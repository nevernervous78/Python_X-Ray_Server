#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example Python script interfacing the GID_sl form on Sergey Stepanov's X-ray Server.

The GID_sl form is available here
https://x-server.gmca.aps.anl.gov/cgi/www_form.exe?template=GID_sl_multilay.htm&method=post

All input variables are contained in the "data" dict

"""

__author__ = "Daniele Pelliccia"
__copyright__ = "Copyright 2019, Instruments & Data Tools Pty Ltd"
__credits__ = ["Daniele Pelliccia", "Sergey Stepanov"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Daniele Pelliccia"
__email__ = "daniele@idtools.com.au"
__status__ = "Development"

import time

import urllib
import requests
from bs4 import BeautifulSoup

import numpy as np
import matplotlib.pyplot as plt


data = {
     'xway': '2',
     'wave': '35',
     'ipol':'1',
     'code': 'Silicon',
     'df1df2': '-1',
     'sigma': '0.',
     'w0': '1.',
     'wh': '1.',
     'i1': '3',
     'i2': '3',
     'i3': '3',
     'daa': '0.',
     'igie': '9',
     'fcentre': '0.5',
     'unic': '0',
     'n1': '0',
     'n2': '0',
     'n3': '0',
     'm1': '0',
     'm2': '0',
     'm3': '0',
     'miscut': '0.',
     'unim': '0',
     'axis': '4',
     'scanmin': '-0.1',
     'scanmax': '0.1',
     'unis': '2',
     'nscan': '401',
     'column': 'A',
     'alphamax': '1.E+8',
     'profile': '',
}

# Submit data to the server
response = requests.post('https://x-server.gmca.aps.anl.gov/cgi/gid_form.pl', data=data)

# Hang on a second
time.sleep(1)

# Scrape text from server response page
doc = BeautifulSoup(response.text, 'html.parser')

# Find the link to the file. The Job ID is going to be href[5]
href = doc.find_all('a', href=True)

# Open the result page
data_url = 'https://x-server.gmca.aps.anl.gov'+href[5]['href']

# Scrape rocking curve file
data_resp = urllib.request.urlopen(url=data_url)
data_soup = BeautifulSoup(data_resp, 'html.parser')

# Convert scraped data into string
data_string = data_soup.text.split('\n')[:-1]

# Define angle and intensity numpy arrays
theta = np.zeros(len(data_string))
intensity = np.zeros(len(data_string))

# Populate arrays
for i,j in enumerate(data_string):
    theta[i] = float(j.strip().split('  ')[0])
    intensity[i] = float(j.strip().split('  ')[-1])

# Open result file
tbl_url = 'https://x-server.gmca.aps.anl.gov'+href[4]['href']

# Scrape rocking curve data file
tbl_resp = urllib.request.urlopen(url=tbl_url)
tbl_soup = BeautifulSoup(tbl_resp, 'html.parser')

# Get relevant lines from result file
inc_angle = float(tbl_soup.text.split('\n')[15].split('|')[1].split('    ')[0])
ex_angle =  float(tbl_soup.text.split('\n')[15].split('|')[1].split('    ')[1])
bragg_angle = float(tbl_soup.text.split('\n')[14].split('|')[1].split('    ')[0])

# Example plot
plt.plot(bragg_angle + 180.*theta/np.pi, intensity)
plt.show()

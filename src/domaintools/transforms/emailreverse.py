#!/usr/bin/env python

from sploitego.maltego.utils import debug, progress
from sploitego.framework import configure
from sploitego.maltego.message import Website, EmailAddress, Label

from urllib import urlencode, urlopen
import lxml.html as html
import re

__author__ = 'leres'
__copyright__ = 'Copyright 2012, Domaintools Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'leres'
__email__ = 'twitleres@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
]

def scrape(page):
	doc = html.fromstring(page)
	xpath = doc.xpath("//p[@class='top-pad-10 clear reverse-whois-narrative']/text()")
	url = re.findall(r'([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', ''.join([str(x) for x in xpath]))
	return url 

@configure(
    label='Reverse email lookup at domaintools.com',
    description='Check if email address has any websites registered',
    uuids=[ 'domaintools.emailreverse' ],
    inputs=[ ( 'Domaintools', EmailAddress ) ],
    debug=True
)
def dotransform(request, response):
	r = urlopen(
		"http://reversewhois.domaintools.com",
	urlencode({'all[]' : request.value,
		  'none[]' : '' }))

	page = r.read()
	if page is not None and "There are no results" in page:
		return response
	else:
		url = scrape(page)
		if url:
			for u in url:	
				info = '<A href=http://reversewhois.domaintools.com/?all[]='+ request.value +'&none[]=> Here </a>'
				e = Website(u)
				e += Label('Additional information', info )
				response += e
        	return response

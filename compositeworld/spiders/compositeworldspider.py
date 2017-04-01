from __future__ import absolute_import
# -*- coding: utf-8 -*-

import scrapy



from compositeworld.items import CompositeworldItem






class Compositeworld(scrapy.Spider):
	# item = CompositeworldItem()
    name = "composite"

    start_urls = ['http://www.compositesworld.com/suppliers/',]
    us_states = {
        'AK':'Alaska',
        'AL':'Alabama',
        'AR':'Arkansas',
        'AS':'American Samoa',
        'AZ':'Arizona',
        'CA':'California',
        'CO':'Colorado',
        'CT':'Connecticut',
        'DC':'District of Columbia',
        'DE':'Delaware',
        'FL':'Florida',
        'GA':'Georgia',
        'GU':'Guam',
        'HI':'Hawaii',
        'IA':'Iowa',
        'ID':'Idaho',
        'IL':'Illinois',
        'IN':'Indiana',
        'KS':'Kansas',
        'KY':'Kentucky',
        'LA':'Louisiana',
        'MA':'Massachusetts',
        'MD':'Maryland',
        'ME':'Maine',
        'MI':'Michigan',
        'MN':'Minnesota',
        'MO':'Missouri',
        'MP':'Northern Mariana Islands',
        'MS':'Mississippi',
        'MT':'Montana',
        'NA':'National',
        'NC':'North Carolina',
        'ND':'North Dakota',
        'NE':'Nebraska',
        'NH':'New Hampshire',
        'NJ':'New Jersey',
        'NM':'New Mexico',
        'NV':'Nevada',
        'NY':'New York',
        'OH':'Ohio',
        'OK':'Oklahoma',
        'OR':'Oregon',
        'PA':'Pennsylvania',
        'PR':'Puerto Rico',
        'RI':'Rhode Island',
        'SC':'South Carolina',
        'SD':'South Dakota',
        'TN':'Tennessee',
        'TX':'Texas',
        'UT':'Utah',
        'VA':'Virginia',
        'VI':'Virgin Islands',
        'VT':'Vermont',
        'WA':'Washington',
        'WI':'Wisconsin',
        'WV':'West Virginia',
        'WY':'Wyoming'
}

    def parse(self, response):
    	blocks = response.css('li[class*=alpha]')
    	
    	linksAtoZ = blocks.css('a::attr(href)').extract()
    	links = []
    	for link in linksAtoZ:
			links.append(response.urljoin(link))
    	# print links

    	for next_page in links:
    		yield scrapy.Request(next_page, callback=self.parse_search_pages)  

    def parse_search_pages(self,response):
    	blocks = response.css('tbody > tr')
    	# print block.extract_first()
    	state_List = blocks.xpath('td[2]/text()').extract()
    	links = response.css('td > a::attr(href)').extract()
    	company_name = response.css('td > a::text').extract()

    	citys = []
    	states = []
    	#city,state format; CITY, STATE
    	for index, state in enumerate(state_List):
    		x = state.strip()
    		temp_state = x[-2:]
    		temp_city = x[0:x.index(',')]

    		if temp_state.isupper():
    			if self.check_if_from_US(temp_state):
    				item = CompositeworldItem()
    				item['city'] = temp_city
    				item['state'] = temp_state
    				item['company_name'] = company_name[index]
    				yield scrapy.Request(response.urljoin(links[index]), callback=self.parse_internal_page, meta={'item': item})

    def parse_internal_page(self,response):
		company_website = response.css('a[rel*=url]::attr(href)').extract()
		description = response.css('em::text').extract_first()
		product_name = response.css('div[class*=sr-category] > div[class*=sr-content]::text').extract_first().strip()
		item = response.meta['item']
		item['product'] = product_name
		item['description'] = description
		item['website_link'] = company_website
		yield item

    def check_if_from_US(self, string):
    	for key, value in self.us_states.items():
    				if string == key:
    					return True

import scrapy


class JACS_Vol_Iss_Spider(scrapy.Spider):
	name = "jacs_vol_iss"
	custom_settings = {
		'USER_AGENT': 'JACSPider, --------@gmail.com',
		'DOWNLOAD_DELAY': 2,
		'CONCURRENT_REQUESTS': 1
	}

	CURR_YEAR = 2020

	# JACS
	JOURNAL_START_YEAR = 1879
	start_urls = ['https://pubs.acs.org/loi/jacsat/group/d' + str(year-(year%10)) + '.y' + str(year) for year in range(JOURNAL_START_YEAR, CURR_YEAR+1)]

	# Inorg Chem
	# JOURNAL_START_YEAR = 1962
	# start_urls = ['https://pubs.acs.org/loi/inocaj/group/d' + str(year-(year%10)) + '.y' + str(year) for year in range(JOURNAL_START_YEAR, CURR_YEAR+1)]

	# Organometallics
	# JOURNAL_START_YEAR = 1982
	# start_urls = ['https://pubs.acs.org/loi/orgnd7/group/d' + str(year-(year%10)) + '.y' + str(year) for year in range(JOURNAL_START_YEAR, CURR_YEAR+1)]

	# Biochem
	# JOURNAL_START_YEAR = 1962 
	# start_urls = ['https://pubs.acs.org/loi/bichaw/group/d' + str(year-(year%10)) + '.y' + str(year) for year in range(JOURNAL_START_YEAR, CURR_YEAR+1)]

	# Chem Revs
	# JOURNAL_START_YEAR = 1924
	# start_urls = ['https://pubs.acs.org/loi/chreay/group/d' + str(year-(year%10)) + '.y' + str(year) for year in range(JOURNAL_START_YEAR, CURR_YEAR+1)]



	def parse(self, response):

		for i in response.css('div.parent-item'):
			volume, issue = i.css('a').attrib['href'].split('/')[-2:]
			yield {
				'volume': volume,
				'issue': issue
			}
import scrapy


class JACSpider(scrapy.Spider):
	name = "jacs"
	custom_settings = {
		'USER_AGENT': 'JACSPider, --------@gmail.com',
		'DOWNLOAD_DELAY': 2,
		'CONCURRENT_REQUESTS': 1
	}

	with open('jacs_vi.csv') as f:
		lines = f.readlines()
	lines = [line.strip().split(',') for line in lines[1:]]

	# JACS
	start_urls = ['https://pubs.acs.org/toc/jacsat/' + volume + '/' + issue for volume, issue in lines]

	# Inorg Chem
	# start_urls = ['https://pubs.acs.org/toc/inocaj/' + volume + '/' + issue for volume, issue in lines]

	# Organometallics
	# start_urls = ['https://pubs.acs.org/toc/orgnd7/' + volume + '/' + issue for volume, issue in lines]

	# Biochem
	# start_urls = ['https://pubs.acs.org/toc/bichaw/' + volume + '/' + issue for volume, issue in lines]

	# Chem Revs
	# start_urls = ['https://pubs.acs.org/toc/chreay/' + volume + '/' + issue for volume, issue in lines]



	def parse(self, response):

		for article in response.css('div.issue-item_metadata'):

			doi = article.css('span.hlFld-Title')[0].css('h5.issue-item_title')[0].css('a').attrib['href']
			title = ''.join(article.css('span.hlFld-Title')[0].css('h5.issue-item_title')[0].css('*::text').getall())
			authors = article.css('span.hlFld-ContribAuthor::text').getall()
			journal = article.css('span.issue-item_jour-name')[0].css('*::text').get()
			year = int(article.css('span.issue-item_year::text').get())
			volume = int(article.css('span.issue-item_vol-num::text').get())
			issue = int(article.css('span.issue-item_issue-num::text').get())

			page_range = article.css('span.issue-item_page-range::text').get()
			if '-' in page_range:
				page_start, page_end = page_range[2:].split('-') # correct for ',\xa010894-10898'
			else:
				page_start = page_range[2:]
				page_end = page_range[2:]
			if page_start.isdigit():
				page_start = int(page_start)
			if page_end.isdigit():
				page_end = int(page_end)

			article_type = article.css('span.issue-item_type::text').get()[2:-1]    # correct for ' (Article)'
			pub_date = article.css('span.pub-date-value::text').get()

			if article.css('span.hlFld-Abstract').get():
				abstract = article.css('span.hlFld-Abstract')[0].css('*::text').get()
			else:
				abstract = ''

			yield {
				'doi': doi,
				'title': title,
				'authors': authors,
				'journal': journal,
				'year': year,
				'volume': volume,
				'issue': issue,
				'page_start': page_start,
				'page_end': page_end,
				'article_type': article_type,
				'pub_date': pub_date,
				'abstract': abstract
			}

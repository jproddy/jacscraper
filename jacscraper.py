import time

import bs4 as bs
import requests


class JACScraper:
	''''
	Contains two scraping methods for various stages of the article scraping
	process.
	'''
	def __init__(self, print_progress=True):
		self.print_progress = True

	def scrape_volumes_and_issues(self, journal_id, start_year, end_year):
		'''
		Scrapes and returns a list of valid (volume, issue) tuples in the given
		journal	during the given timeframe. The most recent issue is omittied as
		it it usually (or always?) incomplete.
		'''
		volume_issue_pairs = []

		for year in range(start_year, end_year + 1):
			url = f'https://pubs.acs.org/loi/{journal_id}/group/d{year-(year%10)}.y{year}'
			soup = bs.BeautifulSoup(requests.get(url).content, 'lxml')

			for entry in soup.find_all('div', class_='parent-item'):
				*_, volume, issue = entry.a['href'].split('/')
				volume_issue_pairs.append((int(volume), int(issue)))

			if self.print_progress:
				print(journal_id, year)
			time.sleep(1.1)

		# remove the most recent issue
		volume_issue_pairs.remove(max(volume_issue_pairs))

		return volume_issue_pairs

	def scrape_articles(self, journal_id, volume, issue):
		'''
		Scrapes data from all articles in the given journal issue. Returns a
		dict mapping article doi to the rest of the data.
		'''
		url = f'https://pubs.acs.org/toc/{journal_id}/{volume}/{issue}'
		soup = bs.BeautifulSoup(requests.get(url).content, 'lxml')
		articles = {}

		for article in soup.find_all('div', class_='issue-item_metadata'):
			if 'SPONSORED CONTENT' in article.text:
				continue

			header = article.find(class_='issue-item_title')
			title = header.text
			# doi has form: xx.xxxx/xxxxxxxxxxx instead of: /doi/xx.xxxx/xxxxxxxxxxx
			doi = header.a['href'][5:]
			authors = [i.text for i in article.find_all(class_='hlFld-ContribAuthor')]
			journal = article.find(class_='issue-item_jour-name').text
			year = int(article.find(class_='issue-item_year').text)

			page_range = article.find(class_="issue-item_page-range").text
			page_range_split = page_range[2:].split('-')
			if len(page_range_split) == 1:
				page_start = page_range_split[0]
				page_end = page_range_split[0]
			elif len(page_range_split) == 2:
				page_start, page_end = page_range_split
			else:
				page_start = ''
				page_end = ''
			page_start = int(page_start) if page_start.isdigit() else None
			page_end = int(page_end) if page_end.isdigit() else None

			article_type = None
			for i in article.find_all(class_='issue-item_type'):
				if i.text:
					article_type = i.text[2:-1]
					break

			pub_date = article.find(class_='pub-date-value').text
			
			abstract_span = article.find(class_='hlFld-Abstract')
			abstract = abstract_span.text if abstract_span else None

			articles[doi] = {
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
				'abstract': abstract,
			}

		if self.print_progress:
			print(journal_id, volume, issue)
		return articles

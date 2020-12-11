import datetime
import json
import os
import sys
import time

from jacscraper import JACScraper


def add_journal():
	'''
	Prompts user for information to add new journal (title, id and start year).
	Only validates that year is a number and that the id is six chars long,
	allowing potentially invalid inputs. The inputted title does not impact
	functionality and is only used for record-keeping.
	'''
	with open('journal_data.json') as f:
		journal_data = json.load(f)

	print('currently available journals:')
	for journal_title in journal_data:
		print(f'\t{journal_title}')
	print()

	journal_title = input('new journal title:\n')
	journal_id = input('new journal id:\n')
	journal_start_year = input('new journal start year:\n')

	if len(journal_id) != 6 or not journal_start_year.isdigit() or journal_title in journal_data:
		print('invalid information. restart')
		quit()

	journal_start_year = int(journal_start_year)

	journal_data[journal_title] = {
		'journal_id': journal_id,
		'start_year': journal_start_year,
		'latest_issue': 0,
		'latest_volume': 0,
		'latest_year': 0
	}

	with open('journal_data.json', 'w') as f:
		json.dump(journal_data, f, indent='\t', sort_keys=True)

	print('journal added. restart to run')

def remove_journal():
	''''
	Prompts user for a journal title to remove. Removes data from
	journal_data.json, but previously downloaded data will remain in the jsons
	directory.
	'''
	with open('journal_data.json') as f:
		journal_data = json.load(f)

	print('currently available journals:')
	for journal_title in journal_data:
		print(f'\t{journal_title}')

	journal_title = input('journal to remove:\n')

	if journal_title not in journal_data:
		print('this journal does not exist')
		quit()

	journal_data.pop(journal_title)

	with open('journal_data.json', 'w') as f:
		json.dump(journal_data, f, indent='\t')

	print('journal removed. restart to run')

def run_scrapers():
	'''
	Loads journal_data.json to determine what data to collect the scrapes
	desired information using a JACScraper. Stores/updates downloaded data in
	the jsons directory and saves a undated record in journal_data.json.
	'''
	print('start', datetime.datetime.now())
	if not os.path.isdir('jsons'):
		os.mkdir('jsons')
	with open('journal_data.json') as f:
		journal_data = json.load(f)
	scraper = JACScraper()

	for title, data in journal_data.items():
		start_year = max(data['start_year'], data['latest_year'])
		end_year = datetime.datetime.now().year
		articles = {}
		volume_issue_pairs = scraper.scrape_volumes_and_issues(data['journal_id'], start_year, end_year)

		for volume, issue in volume_issue_pairs:
			if (volume > data['latest_volume']) or (
				volume == data['latest_volume'] and issue > data['latest_issue']
			):
				articles.update(scraper.scrape_articles(data['journal_id'], volume, issue))
				time.sleep(1.1)

		if not articles:
			print(f'{title} has no updates')
			continue

		path = os.path.join('jsons', f'{title.lower().replace(" ", "_")}.json')
		if os.path.isfile(path):
			with open(path) as f:
				journal_json = json.load(f)
			articles.update(journal_json)
		# sort by doi for fun
		articles = {k: v for k, v in sorted(articles.items(), key=lambda x: x[0])}
		with open(path, 'w') as f:
			json.dump(articles, f)

		journal_data[title]['latest_year'] = end_year
		journal_data[title]['latest_volume'], journal_data[title]['latest_issue'] = max(volume_issue_pairs)

	with open('journal_data.json', 'w') as f:
		json.dump(journal_data, f, indent='\t', sort_keys=True)

	print('end', datetime.datetime.now())


if __name__ == '__main__':
	if not os.path.isfile('journal_data.json'):
		with open('default_journal_data.json') as f:
			default_journal_json = json.load(f)
		with open('journal_data.json', 'w') as f:
			json.dump(default_journal_json, f, indent='\t')
		print('default journal data file created. restart to run')

	if len(sys.argv) == 2:
		if 'add-journal' in sys.argv:
			add_journal()
			quit()
		elif 'remove-journal' in sys.argv:
			remove_journal()
			quit()
		else:
			print('invalid args')
			quit()
	elif len(sys.argv) > 2:
		print('invalid args')
		quit()	

	run_scrapers()

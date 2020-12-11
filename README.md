JACScraper is designed to scrape American Chemical Scociety (ACS) journals and collect the following publically available information for each paper:

	DOI, title, authors, journal, year, volume, issue, page start, page end, article type, publication date, abstract

The datasets and sample cleaning and analysis are available on [Kaggle](https://www.kaggle.com/jroddy33/american-chemical-society-journals). Scraping does take a fair amount of time due to rate-limiting (1 request/s) so this is likely a better source for the data than re-scraping unless a different journal is needed.

The scraper can be run on the command line using:

	python scrape.py

This will create a default `journal_data.json` file that will allow for scraping the six journals listed below. The list can then be modified by rerunning the program with `add-journal` or `remove-journal` arguments and following the prompts. Running the script will create a `jsons` diretory in which the generated files will be saved.

This information will be used to trace various trends in chemical research. Other uses may include generating author connectivity graphs. Unfortunately there are a handful of limitations; articles published prior to 1996 (presumably when ACS embraced digitization?) are not accompanied by their abstracts. Many of the older papers have miscategorized article types and are plagued by typos. Finally, some of the entries are not true research articles but instead mastheads, book reviews, software reviews etc. However, the vast majority of these can be removed via fairly trivial data cleaning techniques.

It was used to scrape [JACS](https://pubs.acs.org/journal/jacsat), [Inorganic Chemistry](https://pubs.acs.org/journal/inocaj), [Organometallics](https://pubs.acs.org/journal/orgnd7), [Biochemistry](https://pubs.acs.org/journal/bichaw), [JOC](https://pubs.acs.org/journal/joceah) and [Chemical Reviews](https://pubs.acs.org/journal/chreay) as a representative sample of journals relevant to my former research.

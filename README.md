JACSpider has been designed using Scrapy to crawl through American Chemical Scociety (ACS) journals and collect the following publically available information for each paper:

	DOI, title, authors, journal, year, volume, issue, page start, page end, article type, publication date, abstract

The datasets and sample cleaning and analysis are available as data_analysis_iron_sulfur_clusters.ipynbh or on [Kaggle](https://www.kaggle.com/jroddy33/american-chemical-society-journals).

This information will be used to trace various trends in chemical research. Other uses may include generating author connectivity graphs. Unfortunately there are a handful of limitations; articles published prior to 1996 (presumably when ACS embraced digitization?) are not accompanied by their abstracts. Many of the older papers have miscategorized article types and are plagued by typos. Finally, some of the entries are not true research articles but instead mastheads, book reviews, software reviews etc. However, the vast majority of these can be removed via fairly trivial data cleaning techniques.

It was used to crawl [JACS](https://pubs.acs.org/journal/jacsat), [Inorganic Chemistry](https://pubs.acs.org/journal/inocaj), [Organometallics](https://pubs.acs.org/journal/orgnd7), [Biochemistry](https://pubs.acs.org/journal/bichaw) and [Chemical Reviews](https://pubs.acs.org/journal/chreay) as a representative example relevant to my former research.

This was done in two stages. First, a csv file containing all volume-issue pairs was collected from each journal's list of issues (e.g. [JACS](https://pubs.acs.org/loi/jacsat/group/d1990.y1999)). Each pair was necessarily collected and stored individually as there are missing issues and bizzare orderings in the early archives. The simple spider used to accomplish this is located in jacs_vol_iss, and the csv files generated are located in vol_iss_csv.

Armed with this information, the relevant data could be extracted from each volume/issue page (e.g. [JACS Volume 117, Issue 11](https://pubs.acs.org/toc/jacsat/117/11)). This spider can be found in the jacspider folder, and the resulting json files are in jacs_jsons.

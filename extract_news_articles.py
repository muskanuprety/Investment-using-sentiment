from requests_html import HTMLSession

def get_news(tickers):
	session = HTMLSession()
	url = "https://news.google.com/search?q="
	for ticker in tickers:
		url = url + ticker

		#use session to get the page
		r = session.get(url)

#render the html, sleep=1 to give it a second to finish before moving on. scrolldown= how many times to page down on the browser, to get more results. 5 was a good number here
r.html.render(sleep=1, scrolldown=1)

#find all the articles by using inspect element and create blank list
articles = r.html.find('article')
newslist = []

#loop through each article to find the title and link. try and except as repeated articles from other sources have different h tags.
for item in articles:
    try:
        newsitem = item.find('h3', first=True)
        title = newsitem.text
        # link = newsitem.absolute_links
        print(title)
    except:
       pass

#print the length of the list
print(len(newslist))
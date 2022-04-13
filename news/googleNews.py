# https://github.com/kumargopal/Google-News-Crawler/blob/master/Google%20News%20Crawler.ipynb

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import pandas as pd
from newspaper import Article
import nltk
from IPython.display import display, HTML
import warnings


class News():
    def __init__(self):
        self.base_url = "https://news.google.com"

    # Method for getting HTML content
    # Returns BeautifulSoup object

    def bs_html(self, url):
        response = requests.get(url)

        # HTML of the page
        html = response.text
        # BeautifulSoup object of the HTML
        bs_html = BeautifulSoup(html, features='lxml')

        return bs_html

    # Get article data using newspaper library

    def get_article_data(self, url):

        # en For English
        article = Article(url, language="en")
        try:
            article.download()
            article.parse()
            article.nlp()

            article_data = list()

            article_data.append(article.title)
            article_data.append(article.summary)
            article_data.append(article.publish_date)
            article_data.append(url)
        except:

            article_data = None

        return article_data

    # For getting all the aricles data using multiproccessing for better speed

    def multi_proccess_article_data(self, article_urls):

        n_articles = len(article_urls)

        with Pool(processes=20) as pool:
            all_articles_data = pool.map_async(
                self.get_article_data, article_urls, chunksize=1)

            while not all_articles_data.ready():
                all_articles_data.wait(timeout=1)

        return all_articles_data.get()

    # Return all the URLs from given BeautifulSoup object

    def get_urls(self, list_news):

        # Collects all the elements with 'a' tag
        list_news = [news.find('a') for news in list_news]

        news_urls = list()

        for news in list_news:

            # Extracting 'href' attribute
            sub_url = news['href']

            # Concatenating base and parital urls to make the URL complete
            n_url = self.base_url+sub_url.replace('.', '')

            news_urls.append(n_url)

        return (news_urls)

    def display_table(self, df, header):

        # Setting the indcies 1 to the length of the DatFrame
        df.index = range(1, len(df)+1)

        # Setting the url with 'a' for better convention
        if '<a href="' not in df['URL']:
            df['URL'] = df['URL'].apply(lambda x: x.replace(
                '<a href="', '').replace('">link</a>', ''))
            df['URL'] = df['URL'].apply(lambda x: '<a href="'+x+'">link</a>')

        # Converting the DataFrame into HTML and adding the title
        html_table = '<h1 align = "Center">{}</h1>'.format(
            header)+df.to_html(escape=False)

        # For shifting the header to the left
        html_table = html_table.replace(
            '<th>', '<th style="text-align: left;">')
        # FOr shifting the other strings to the left
        html_table = html_table.replace(
            '<td>', '<td style="text-align: left;">')

        # Displays the html by replacing '\\n' by '<br>' for new line
        display(HTML(html_table.replace('\\n', '<br>')))

    # Method to news related to give query from give DataFrame
    def search_query(self, dfs, query):

        matched_data = []
        for df in dfs:

            for i_row, row_data in enumerate(df['Title']):

                # Converting both the quey and row_data for matching all possible News
                if(query.lower() in row_data.lower()):
                    matched_data.append(df.iloc[i_row])

        return(matched_data)


# Url of the main news page
url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"

# Creating a News object
news_obj = News()

# getting the BeautiffulSoup object of the main news' page HTML
html = news_obj.bs_html(url)


# Extracting the main news URLS
main_news = html.find_all('h3', class_='ipQwMb ekueJc gEATFF RD0gLb')
main_news_urls = news_obj.get_urls(main_news)

# Extracting the sub news URLs
sub_news = html.find_all('div', class_="xrnccd F6Welf R7GTQ keNKEd j7vNaf")
sub_news = [news.find('h4') for news in sub_news]
sub_news_urls = news_obj.get_urls(sub_news)

# # %%time
# main_news_data = news_obj.multi_proccess_article_data(main_news_urls)
# sub_news_data = news_obj.multi_proccess_article_data(sub_news_urls)

# # Columns for the DataFrame of Articles data
# columns = ['Title', 'Summary', 'Published Date', 'URL']


# # Removing if there is None type data
# main_news_data = [data for data in main_news_data if data]

# # COnverting into pandas DataFrame with above defined columns
# df_main_news = pd.DataFrame(main_news_data, columns=columns)

# # Displays Main News
# news_obj.display_table(df_main_news.head(), header="Main News")


# # Remove the None type data
# sub_news_data = [data for data in sub_news_data if data]

# # Creating pandas DataFrame for Subnews aricles data
# df_sub_news = pd.DataFrame(sub_news_data, columns=columns)

# # Displays the Sub News articles data
# news_obj.display_table(df_sub_news.head(), header="Sub News")


# NEWS RELATED TO STOCK
query = 'Stock'
matches = news_obj.search_query([df_main_news, df_sub_news], query)
matches_df = pd.DataFrame(matches, columns=columns)
news_obj.display_table(matches_df, header='News related to '+query)

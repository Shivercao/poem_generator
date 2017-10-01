import urllib.request
from bs4 import BeautifulSoup
import re
import urllib.parse as urlparse
import os
import tempfile


"""
This script is used to scrape http://amediavoz.com/ website.
It is a spanish poetry website.
    
All poems of each author in the website are collected and saved
into text files, one for each author containing all of his, hers poems.

The script contains a get_links() function to get all links of
different author's poems htm pages.

Then this links are visited and the html is parsed to obtain the
poems inside them"""

def get_poems_from_website(int_dir):

    if not os.path.exists(int_dir):

        mega_poems = []

        # Function to get links for webpages for each author from index page.
        def get_links(home_url):
            links = []
            home_page = urllib.request.urlopen(home_url)

            text = home_page.read()
            soup = BeautifulSoup(text)

            for tag in soup.findAll('a', href=True):
                tag['href'] = urlparse.urljoin(home_url, tag['href'])
                links.append(tag['href'])
            return links

        links_AK = get_links('http://amediavoz.com/indice-A-K.htm')
        links_LZ = get_links('http://amediavoz.com/indice-L-Z.htm')

        # List with all of the links
        all_links = links_AK[8:-17]
        all_links.extend(links_LZ[8:-17])


        c = 1
        poem_counter = 0                    # each html page is obtained and parsed
        for html_page in all_links:         # to obtain the poems inside it.
            try:
                # Page to variable page
                page = urllib.request.urlopen(html_page)
                print('parsing ' + str(html_page))

                # Parsing
                soup = BeautifulSoup(page, 'html.parser')

                poems = []
                for i in range(0, len(soup.find_all('font'))):
                    text = soup.find_all('font')[i]
                    text = str(text)
                    text = re.sub('<(.*)>','',text)
                    text = re.sub('\n', ' ', text)
                    text = re.sub('\t', ' ', text)
                    text = re.sub(' +',' ',text)
                    text = re.sub('\xa0', ' ', text)
                    text = re.sub('\xad', ' ', text)

                    if len(text) > 60:
                        poems.append(text)

                poemas = poems[3:-3]

                # Poems by author are saved into the Temp directory.
                os.makedirs(int_dir)
                dir = os.path.join(int_dir, r'author_' + str(c) + '.txt')

                with open(dir,'w') as f:
                    f.writelines(poemas)

                mega_poems.append(poemas)

                print(str(len(poemas)) + ' poems extracted')
                c +=1
                poem_counter += len(poemas)
            except:
                print('An error ocurred here skipping this one ...')


        print(str(poem_counter) + ' poems extracted total.')
    else:
        print('Poems are already extracted and stored.\n')



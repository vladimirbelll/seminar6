from urllib.request import urlopen
from urllib.parse import urldefrag, urlparse, urljoin

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/')
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

desires = 5
file = open(f'wiki_parse_{desires}.txt', 'w')

def download_from_the_internet(url):
    try:
        return urlopen(url).read()
    except:
        return None

    
starter_url = 'https://simple.wikipedia.org/wiki/Main_Page'
html = download_from_the_internet(starter_url)
parser = BeautifulSoup(html, features="html.parser")

all_visited_links = []
def recursive_calls(current_link, depth, desired_depth, visited_links):
    if depth >= desired_depth:
        all_visited_links.extend(list(set(visited_links)))
    else:
        html = download_from_the_internet(current_link)
        parser = BeautifulSoup(html, features="html.parser")
        for link in parser.find_all('a'):
            href = link.get('href')
            parsed_href = urlparse(href)
            if parsed_href.netloc == 'simple.wikipedia.org' or not parsed_href.netloc:
                clean_link = urljoin(starter_url, parsed_href.path)
                if clean_link not in visited_links:
                    visited_links.append(clean_link)
                    recursive_calls(clean_link, depth+1, desired_depth, visited_links)

recursive_calls(starter_url, 0, desires, [])

all_visited_links = set(all_visited_links)
file.write(f'This is how many links there are for depth {str(desires)} = {len(all_visited_links)} \n')
file.write('\n'.join(all_visited_links))
file.close()
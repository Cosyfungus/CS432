from bs4 import BeautifulSoup
import requests
import re

#target url to crawl
# commented out urls are my 'history'
# url = "https://www.reddit.com/"
# url = "https://www.toyota.com/"
# url = "https://kbdfans.com/collections/keycaps"
# url = "https://en.wikipedia.org/wiki/1996_Men%27s_Ice_Hockey_World_Championships"
# url = "https://www.youtube.com"
# url = "https://en.wikipedia.org/wiki/Web_science" 
# url = "https://github.com/VAST-AI-Research/TripoSR"
# url = "https://www.chevrolet.com"
# url = "https://www.samsung.com/us/"
# url = "https://www.aliexpress.us"
# url = "https://zoom.us"
# url = "https://portal.odu.edu"


# create an html document from the requested url
# with a timeout of 5 seconds
html_doc = requests.get(url, timeout=5).text

# create a BeatifulSoup object
soup = BeautifulSoup(html_doc, 'html.parser')

# find all 'a' sections in the html code followed by 'href'
# pull the uri from each found segment
# append uris to links.txt
for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
    print(link.get('href'))

    #False = link is not in links.txt, True = already exists
    exists = False

    # append links to end of links.txt
    fileLinks = open ("links.txt", "a+")
    
    #loops through links.txt to check if current link already exists
    for line in fileLinks : 
        if line == link.get('href') :
            exists = True
    #only appends to file if link is unique
    if exists == False :       
        fileLinks.write(link.get('href'))
        fileLinks.write("\n")
    fileLinks.close()


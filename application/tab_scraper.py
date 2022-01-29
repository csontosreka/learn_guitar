from bs4 import BeautifulSoup
import requests


#TODO
def get_tab_search_results(artist, song):
    html_text = requests.get('https://www.guitartabs.cc/search.php?tabtype=any&band=' + artist.lower() + '&song=' + song.lower())
    soup = BeautifulSoup(html_text.text, 'lxml')

    search_results = soup.find_all('table', class_='tabslist fs-12')
    rows = search_results[0].find_all('tr')

    tabs = []
    for row in rows[1:]:
        id = row.find('td', class_="serial").text
        artist = row.find('td', text=id).find_next_sibling("td").find_next_sibling("td").text
        title = row.find('a', class_="ryzh22").text 
        tab_type = row.find('td', class_="tabrat t_title").text
        tab_link = row.find('a', class_="ryzh22", href=True)['href']

        tabs.append([id, artist, title, tab_type, tab_link])
    
    return tabs

#TODO there are still some bugs
def get_tab(tab_url):
    url = 'https://www.guitartabs.cc' + tab_url
    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.text, 'lxml')

    tab_first_part = soup.find_all('pre')[1].contents[0]
    tab_second_part = soup.find_all('pre')[1].contents[2]
    tab = tab_first_part + tab_second_part

    title = soup.find('h3', class_="content_h").text

    return (title, tab)


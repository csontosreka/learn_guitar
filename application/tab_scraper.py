from bs4 import BeautifulSoup
import requests

def get_tab_search_results():
    html_text = requests.get('https://www.guitartabs.cc/search.php?tabtype=any&band=a+day+to+remember&song=all+i+want')
    soup = BeautifulSoup(html_text.text, 'lxml')

    search_results = soup.find_all('table', class_='tabslist fs-12')
    rows = search_results[0].find_all('tr')
    print(rows)

    tabs = []
    for row in rows[1:]:
        id = row.find('td', class_="serial").text
        artist = row.find('td', text=id).find_next_sibling("td").find_next_sibling("td").text
        title = row.find('a', class_="ryzh22").text 
        tab_type = row.find('td', class_="tabrat t_title").text
        tab_link = row.find('a', class_="ryzh22", href=True)['href']

        tabs.append([id, artist, title, tab_type, tab_link])
    
    return tabs


def get_tab():
    html_text = requests.get('https://www.guitartabs.cc/tabs/a/a_day_to_remember/all_i_want_tab.html')
    soup = BeautifulSoup(html_text.text, 'lxml')

    tab = soup.find_all('pre')
    return tab


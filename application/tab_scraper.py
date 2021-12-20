from bs4 import BeautifulSoup
import requests

def get_tab_search_results():
    html_text = requests.get('https://www.guitartabs.cc/search.php?tabtype=any&band=a+day+to+remember&song=all+i+want')
    soup = BeautifulSoup(html_text.text, 'lxml')

    search_results = soup.find_all('table', class_='tabslist fs-12')
    return search_results

def get_tab():
    html_text = requests.get('https://www.guitartabs.cc/tabs/a/a_day_to_remember/all_i_want_tab.html')
    soup = BeautifulSoup(html_text.text, 'lxml')

    tab = soup.find_all('pre')
    return tab
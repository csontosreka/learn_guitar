from bs4 import BeautifulSoup
import requests


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

        tabs_dict = {
            "id": id,
            "artist": artist,
            "title": title,
            "tab_type": tab_type,
            "tab_link": tab_link
        }

        tabs.append(tabs_dict)
    
    return tabs


def get_tab(tab_url):
    url = 'https://www.guitartabs.cc' + tab_url
    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.text, 'lxml')

    tab = ''

    for content in enumerate(soup.find_all('pre')[1]):
        if content[0] % 2 == 0:
            tab += content[1] 
        if content[1].name == 'a':
            tab += content[1].text

    title = soup.find('h3', class_="content_h").text

    tuning = get_tuning(tab)

    if 'Chords' in title:
        chord_list = get_chords(tab)
    else:
        chord_list = []

    tab_dict = {
        "title": title,
        "tab": tab,
        "chord_list": chord_list,
        "tuning": tuning
    }

    return tab_dict


def get_chords(tab):
    chords = ['A', 'Am', 'A#', 'A#m', 'A7',
                'B', 'Bm', 'B#', 'B#m', 'B7',
                'C', 'Cm', 'C#', 'C#m', 'C7',
                'D', 'Dm', 'D#', 'D#m', 'D7',
                'E', 'Em', 'E#', 'E#m', 'E7',
                'F', 'Fm', 'F#', 'F#m', 'F7',
                'G', 'Gm', 'G#', 'G#m', 'G7']

    chord_list = []
    for chord in chords:
        if f' {chord} ' in tab:
            chord_list.append(chord)
    
    return chord_list


def get_tuning(tab):
    tunings = ['Standard', 'Drop D ', 'Drop C#', 'Drop C ', 'Drop B ', 'Drop A#', 'Drop A ' ]

    for tuning in tunings:
        if tuning in tab:
            result = tuning
    
    return result
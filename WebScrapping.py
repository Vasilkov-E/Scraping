import requests
from bs4 import BeautifulSoup

URL = 'https://4pda.ru/page/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*'}

LIST = ['смартфон']

def get_html(url, params=None):
    if params:
        u = url + f'{int(params["page"])}/'
    else:
        u = url
    r = requests.get(u, headers=HEADERS, params=params)
    return r


def get_content(r):
    soup = BeautifulSoup(r, "html.parser")
    a = []
    items = soup.find_all('article', class_='post')
    for item in items:
        g = item.find('h2', class_="list-post-title")
        h = item.find('a', rel="bookmark")
        if g:
            u = g.get_text()
            href = h.get('href')
        else:
            u = 'There is no'
            href = 'There is no'
        for l in LIST:
            if u.lower().find(str(l)) != -1:
                a.append({
                    'title': u,
                    'href': href,
                })
    return a


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('ul', class_="page-nav").find_all('a')[-2]
    if pages:
        return int(pages.get_text())
    else:
        return 1


def parse():
    html = get_html(URL)
    print(html)
    if html.status_code == 200:
        pages = get_pages_count(html.text)
        titles = []
        for page in range(1, pages + 1):
            html = get_html(URL, params={'page': page})
            titles.append(get_content(html.text))


        for el in titles:
            for e in range(0, len(el)):
                print(el[e]['title'])
                print(el[e]['href'])
                print("")



if __name__ == '__main__':
    parse()


import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import unquote


def FoxtrotParser(searchQuery):
    url = 'https://www.foxtrot.com.ua/ru/search?query='+searchQuery
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
               'Connection': 'keep-alive',
               'DNT': '1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    r = requests.get(url, headers=headers)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    searchList = soup.find('div', {'class': 'listing-container'})
    items = searchList.find_all('div', {'class': 'listing-item'})
    searchData = []
    for item in items:

        name = item.find(
            'p', {'class': 'info'}).text

        price = item.find('span', {'class': 'numb'}).text

        reviewsCount = item.find(
            'span', {'class': 'review-number'}).text
        reviewsWord = item.find(
            'span', {'class': 'review-text'}).text
        reviews = reviewsCount+' '+reviewsWord

        img = item.find('img')
        src = img['src']

        link = item.find(
            'a', {'class': 'detail-link'}).get('href')
        link = 'https://www.foxtrot.com.ua'+link

        reviewsLink = item.find(
            'a', {'class': 'reviews-link'}).get('href')
        reviewsLink = 'https://www.foxtrot.com.ua'+reviewsLink

        status = item.find('span', {'class': 'able-text'}).text

        searchData.append({
            'name': name.strip(),
            'price': price.strip(),
            'reviews': reviews.strip(),
            'src': src.strip(),
            'link': link.strip(),
            'reviewsLink': reviewsLink.strip(),
            'status': status.strip()
        })
    return searchData


print(FoxtrotParser('видеокарта'))
